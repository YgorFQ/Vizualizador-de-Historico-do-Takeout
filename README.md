# 📼 YouTube Takeout Viewer

Transforme seu histórico do YouTube (Google Takeout) em uma galeria visual navegável — com thumbnails, busca, scroll infinito e restauração de sessão.

🔗 **[Ver demo →](https://SEU-USUARIO.github.io/SEU-REPOSITORIO)**

---

## ✨ Funcionalidades

- 🎬 Grade de thumbnails no estilo YouTube
- 🔍 Busca por título em tempo real
- 🔃 Ordenação: mais recentes, mais antigos, A–Z, Z–A
- ♾️ Scroll infinito (40 vídeos por vez)
- 💾 Restauração de sessão — volta exatamente de onde parou
- 🚀 Parse de arquivos gigantes sem travar memória (chunks de 8 MB)
- 🖱️ Clique abre o vídeo direto no YouTube

---

## 🚀 Como subir no GitHub Pages

### 1. Baixe seu histórico

Acesse [Google Takeout](https://takeout.google.com), selecione apenas **YouTube e YouTube Music → Histórico → Histórico de exibição**.

O arquivo se chama `watch-history.html`.

### 2. Gere o videos.json

```bash
python parse.py watch-history.html
```

Saída esperada:
```
Arquivo: watch-history.html (312.4 MB)
Lendo em chunks (sem carregar tudo na memória)...
  Progresso: 100%  (14832 vídeos encontrados)
Salvo em: videos.json
```

### 3. Suba para o GitHub

```bash
git init
git add index.html parse.py README.md .nojekyll .gitignore videos.json
git commit -m "primeiro commit"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
git push -u origin main
```

> ⚠️ O `watch-history.html` está no `.gitignore` — ele é grande demais e tem dados brutos. Só o `videos.json` vai para o repositório.

### 4. Ative o GitHub Pages

1. No repositório → **Settings → Pages**
2. Em **Source**, selecione `Deploy from a branch`
3. Branch: `main` / pasta: `/ (root)`
4. Clique em **Save**

Em ~1 minuto seu site estará em:
```
https://SEU-USUARIO.github.io/SEU-REPOSITORIO
```

---

## 💻 Rodando localmente

```bash
python -m http.server 8000
```

Acesse: `http://localhost:8000`

> O terminal vai parecer "travado" — isso é normal. O servidor está rodando. Não feche.

---

## 🗂️ Estrutura

```
youtube-takeout-viewer/
├── index.html          # App web
├── parse.py            # Script de parse
├── videos.json         # Gerado pelo parse.py — versionar para o GitHub Pages
├── .nojekyll           # Diz ao GitHub Pages para não processar com Jekyll
├── .gitignore
└── README.md
```

---

## ⚙️ Por que leitura em chunks?

O `watch-history.html` pode ter centenas de MB em **uma única linha**. VS Code trava ao tentar abrir. O `parse.py` lê em pedaços de 8 MB mantendo um buffer inteligente para não perder entradas na fronteira entre chunks.

---

## 🛠️ Tecnologias

| Parte | Tecnologia |
|---|---|
| Parse | Python puro (sem dependências externas) |
| Frontend | HTML + CSS + JS vanilla (zero frameworks, zero build) |
| Sessão | `localStorage` com hash de integridade |
| Thumbnails | `i.ytimg.com` — gratuito por video ID |

---

## 📄 Licença

MIT
