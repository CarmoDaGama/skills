#!/usr/bin/env python3
"""Start, inspect, or stop Animate's local HTTP server."""

from __future__ import annotations

import argparse
import http.server
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = Path(tempfile.gettempdir()) / 'animate-server.json'
LOG = Path(tempfile.gettempdir()) / 'animate-server.log'
HOST = '127.0.0.1'
DEFAULT_PORT = 4173
WINDOWS = os.name == 'nt'


def read_state() -> dict | None:
    try:
        return json.loads(STATE.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def pid_alive(pid: int) -> bool:
    if not isinstance(pid, int):
        return False
    if WINDOWS:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        code = ctypes.c_ulong()
        ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
        kernel32.CloseHandle(handle)
        return bool(ok) and code.value == 259
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, TypeError):
        return False


def responds(port: int) -> bool:
    try:
        with urllib.request.urlopen(f'http://{HOST}:{port}/index.html', timeout=0.8) as response:
            return response.status == 200
    except Exception:
        return False


def active_state() -> dict | None:
    state = read_state()
    if not state:
        return None
    if pid_alive(state.get('pid')) and responds(state.get('port')):
        return state
    try:
        STATE.unlink()
    except FileNotFoundError:
        pass
    return None


def available_port() -> int:
    for port in range(DEFAULT_PORT, DEFAULT_PORT + 50):
        with socket.socket() as sock:
            try:
                sock.bind((HOST, port))
                return port
            except OSError:
                continue
    raise RuntimeError('No free local port found between 4173 and 4222.')


def start() -> int:
    state = active_state()
    if state:
        print(state['url'])
        return 0

    port = available_port()
    detach = (
        {'creationflags': subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP}
        if WINDOWS else {'start_new_session': True}
    )
    with LOG.open('ab') as log:
        process = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), 'run', '--port', str(port)],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=log,
            **detach,
        )

    url = f'http://{HOST}:{port}/'
    for _ in range(40):
        if responds(port):
            print(url)
            return 0
        if process.poll() is not None:
            break
        time.sleep(0.1)
    print(f'Animate server failed to start. See {LOG}.', file=sys.stderr)
    return 1


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != '/__root':
            super().do_GET()
            return
        body = ROOT.as_posix().encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(port: int) -> int:
    os.chdir(ROOT)
    server = http.server.ThreadingHTTPServer((HOST, port), Handler)
    STATE.write_text(json.dumps({
        'pid': os.getpid(),
        'port': port,
        'url': f'http://{HOST}:{port}/',
        'root': str(ROOT),
    }, indent=2) + '\n')

    def shutdown(_signum, _frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, shutdown)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        state = read_state()
        if state and state.get('pid') == os.getpid():
            STATE.unlink(missing_ok=True)
    return 0


def status() -> int:
    state = active_state()
    if state:
        print(state['url'])
        return 0
    print('stopped')
    return 1


def stop() -> int:
    state = read_state()
    if not state or not pid_alive(state.get('pid')):
        STATE.unlink(missing_ok=True)
        print('stopped')
        return 0
    os.kill(state['pid'], signal.SIGTERM)
    for _ in range(30):
        if not pid_alive(state['pid']):
            break
        time.sleep(0.1)
    STATE.unlink(missing_ok=True)
    print('stopped')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)
    subparsers.add_parser('start')
    subparsers.add_parser('status')
    subparsers.add_parser('stop')
    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    if args.command == 'start':
        return start()
    if args.command == 'status':
        return status()
    if args.command == 'stop':
        return stop()
    return run(args.port)


if __name__ == '__main__':
    raise SystemExit(main())
