# Skills

Skills que uso nos agentes (Cursor / Claude / Codex). Cada pasta tem um `SKILL.md`.

---

## Telas

Pra inventar e fechar a cara de um app antes de gerar mock.

- [`plan-screen`](./plan-screen): conversa, uma tela ou fluxo com wireframes ASCII tipados por padrão (SVG sob pedido), depois PNGs em `mocks/`

## Design system

Quando quero tirar a linguagem visual de uma referência e deixar pronta pra implementar.

- [`extract-ds`](./extract-ds): site pronto → cópia funcional preservando o runtime ou convertida para `file://`, com aprovação de Overview e Components
- [`img-to-html`](./img-to-html): mock → **wireframe ASCII tipado + plano** → **aprovação** → `index.html` + `assets/styles.css` (sem framework): fundo completo (CSS/imagens) → componentes com fontes → assets restantes → revisão final, cada etapa aplicável com gate
- [`img2html`](./img2html): mock → plano de camadas de trás para a frente → **aprovação** → página inteira construída de uma vez com auto-revisão → **aprovação** (dois gates, sem wireframe)

## Imagem

Gerar, converter, brincar com PNG.

- [`to-img`](./to-img): qualquer pedido → n PNGs em paralelo (OpenRouter, gpt2 @ 1K) em `mocks/`
- [`to-wireframe`](./to-wireframe): imagem ou brief de tela → wireframe **tipado** e aninhado em SVG ou ASCII (`format=svg|ascii`)
- [`draw-wireframe`](./draw-wireframe): conversa, brief ou imagem → wireframe **visual** em cinza (dashboard, site ou app) desenhado por script, sem API de imagem; cru ou com texto real para testar tipografia
- [`openrouter-img`](./openrouter-img): CLI dos modelos de imagem do OpenRouter
- [`nano-banana-pro`](./nano-banana-pro): gerar/editar imagem com Nano Banana Pro (Gemini)
- [`fal-ai`](./fal-ai): fal.ai Model API (auth/upload/subscribe) + Moondream detect/query/point/caption/segment

## Motion e mídia

Mexer em animação, áudio e vídeo.

- [`animate`](./animate): serve e mantém um catálogo local de componentes animados e backgrounds, com IDs estáveis e caminhos copiáveis
- [`video2html`](./video2html): vídeo curto de UI + imagem → HTML vivo (HTML/CSS/SVG, GSAP, shaders, Three.js), com o elemento mais arriscado aprovado antes do resto
- [`video2html-backup`](./video2html-backup): primeira versão da `video2html`, só por invocação explícita
- [`mediabunny`](./mediabunny): áudio/vídeo com a lib Mediabunny

## Planejamento e entrega

Afiando ideia, quebrando em tickets, passando o bastão.

- [`grill-me`](./grill-me): entrevista dura pra afiar plano ou design
- [`to-tickets`](./to-tickets): plano/spec/conversa → tickets com dependências
- [`handoff`](./handoff): compacta a conversa pra outro agente continuar
- [`improve-codebase-architecture`](./improve-codebase-architecture): procura refactors que aprofundam módulos rasos, gera relatório HTML e entrevista sobre o escolhido

## Utilitários

Coisas soltas que salvam tempo.

- [`context7-mcp`](./context7-mcp): puxa docs atuais de libs via Context7 (em vez de chutar de memória)
