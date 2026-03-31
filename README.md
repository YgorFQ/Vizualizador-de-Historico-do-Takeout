# 📼 YouTube Takeout Viewer

Transforme seu histórico do YouTube (Google Takeout) em uma galeria visual navegável — com thumbnails, busca e scroll infinito, igual ao YouTube.

---

## ✨ O que faz

- 🎬 Exibe todos os vídeos que você assistiu em uma grade de thumbnails
- 🔍 Busca por título em tempo real
- 🔃 Ordenação: mais recentes, mais antigos, A–Z, Z–A
- ♾️ Scroll infinito (40 vídeos por vez, sem travar)
- 🚀 Lê arquivos gigantes sem travar memória (leitura em chunks de 8 MB)
- 🖱️ Clique em qualquer vídeo abre direto no YouTube

---

## 📋 Pré-requisitos

- Python 3.8+

> Não precisa instalar nada além do Python. O `parse.py` usa apenas bibliotecas padrão (regex, json, pathlib).

---

## 🚀 Como usar

### 1. Baixe seu histórico do YouTube

Acesse [Google Takeout](https://takeout.google.com), selecione apenas **YouTube e YouTube Music** → **Histórico** → **Histórico de exibição**.

O arquivo que você precisa se chama `watch-history.html`.

### 2. Organize os arquivos

```
youtube-takeout-viewer/
├── parse.py
├── index.html
└── watch-history.html   ← coloque aqui
```

### 3. Gere o JSON

```bash
python parse.py watch-history.html
```

Você verá o progresso em tempo real:

```
Arquivo: watch-history.html (312.4 MB)
Lendo em chunks (sem carregar tudo na memória)...
  Progresso: 100%  (14832 vídeos encontrados)
Total: 14832 vídeos únicos encontrados.
Salvo em: /seu/caminho/videos.json
```

### 4. Suba um servidor local

O navegador bloqueia `fetch()` de arquivos locais por segurança, então você precisa de um servidor simples:

```bash
python -m http.server 8000
```

> ⚠️ O terminal vai parecer "travado" — isso é **normal**. O servidor está rodando e esperando requisições.  
> **Não feche o terminal.**

### 5. Abra no navegador

```
http://localhost:8000
```

---

## 🗂️ Estrutura do projeto

```
youtube-takeout-viewer/
├── parse.py            # Faz o parse do HTML e gera videos.json
├── index.html          # Galeria web (abre no navegador)
├── videos.json         # Gerado pelo parse.py (não versionar)
└── watch-history.html  # Seu arquivo do Google Takeout (não versionar)
```

---

## ⚙️ Por que leitura em chunks?

O arquivo `watch-history.html` do Google Takeout pode ter **centenas de MB** e vem todo em **uma única linha**. Editores como VS Code travam ao tentar abrir. O `parse.py` resolve isso lendo o arquivo em pedaços de 8 MB por vez, mantendo um buffer inteligente para não perder entradas que ficam na fronteira entre dois chunks.

---

## 🛠️ Tecnologias

| Parte | Tecnologia |
|---|---|
| Parse | Python puro (regex, sem BeautifulSoup) |
| Frontend | HTML + CSS + JS vanilla (zero frameworks) |
| Thumbnails | `i.ytimg.com` — serve grátis por video ID |

---

## 📄 Licença

MIT
