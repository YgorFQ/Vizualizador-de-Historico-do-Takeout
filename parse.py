"""
parse.py — Converte o histórico do YouTube (Google Takeout) em videos.json

Lê o arquivo em chunks para não explodir a memória,
mesmo que seja um arquivo gigante em uma única linha.

Uso: python parse.py watch-history.html
"""

import sys
import json
import re
from pathlib import Path

# Tamanho de cada chunk lido do arquivo (8 MB)
CHUNK_SIZE = 8 * 1024 * 1024

# Regex para encontrar blocos de entrada do histórico
# Cada entrada fica dentro de um <div class="content-cell ...">...</div>
RE_CELL = re.compile(
    r'<div[^>]+class="[^"]*content-cell[^"]*"[^>]*>(.*?)</div>',
    re.DOTALL
)

# Extrai href de um <a href="...">
RE_HREF = re.compile(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL)

# Extrai video id de URLs do YouTube
RE_VID = re.compile(r'(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})')

# Data no formato do Google Takeout em PT-BR
RE_DATE = re.compile(
    r'(\d{1,2}\s+de\s+\w+\.?\s+de\s+\d{4}[,\s]*[\d:]*\s*\w*)'
)

# Strip tags HTML simples
RE_TAGS = re.compile(r'<[^>]+>')


def strip_tags(html):
    return RE_TAGS.sub("", html).strip()


def parse_stream(html_path):
    """
    Lê o arquivo em chunks de CHUNK_SIZE bytes.
    Mantém um buffer para não perder células que ficam na fronteira entre chunks.
    """
    videos = []
    seen_ids = set()
    buffer = ""

    path = Path(html_path)
    file_size = path.stat().st_size
    bytes_read = 0

    with path.open("r", encoding="utf-8", errors="replace") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break

            bytes_read += len(chunk.encode("utf-8", errors="replace"))
            buffer += chunk

            # Processa todas as células completas que já estão no buffer
            last_end = 0
            for m in RE_CELL.finditer(buffer):
                last_end = m.end()
                cell_html = m.group(1)

                # Busca todos os links dentro da célula
                for link_m in RE_HREF.finditer(cell_html):
                    href = link_m.group(1)
                    link_text = strip_tags(link_m.group(2))

                    if "youtube.com/watch" not in href and "youtu.be/" not in href:
                        continue

                    vid_m = RE_VID.search(href)
                    if not vid_m:
                        continue

                    video_id = vid_m.group(1)
                    if video_id in seen_ids:
                        continue
                    seen_ids.add(video_id)

                    title = link_text if link_text and link_text != href else f"Vídeo {video_id}"

                    # Data: busca no texto da célula toda
                    cell_text = strip_tags(cell_html)
                    date_m = RE_DATE.search(cell_text)
                    date_str = date_m.group(1).strip() if date_m else ""

                    videos.append({
                        "id": video_id,
                        "title": title,
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                        "date": date_str,
                    })

            # Mantém no buffer apenas o trecho após a última célula completa
            # (para não perder células que cruzam a fronteira do chunk)
            if last_end > 0:
                buffer = buffer[last_end:]

            pct = min(100, int(bytes_read / file_size * 100))
            print(f"\r  Progresso: {pct}%  ({len(videos)} vídeos encontrados)", end="", flush=True)

    # Processa o que sobrou no buffer
    for m in RE_CELL.finditer(buffer):
        cell_html = m.group(1)
        for link_m in RE_HREF.finditer(cell_html):
            href = link_m.group(1)
            link_text = strip_tags(link_m.group(2))
            if "youtube.com/watch" not in href and "youtu.be/" not in href:
                continue
            vid_m = RE_VID.search(href)
            if not vid_m:
                continue
            video_id = vid_m.group(1)
            if video_id in seen_ids:
                continue
            seen_ids.add(video_id)
            title = link_text if link_text and link_text != href else f"Vídeo {video_id}"
            cell_text = strip_tags(cell_html)
            date_m = RE_DATE.search(cell_text)
            date_str = date_m.group(1).strip() if date_m else ""
            videos.append({
                "id": video_id,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                "date": date_str,
            })

    print()  # nova linha após o progresso
    return videos


def main():
    if len(sys.argv) < 2:
        print("Uso: python parse.py <caminho-do-historico.html>")
        sys.exit(1)

    html_path = sys.argv[1]
    if not Path(html_path).exists():
        print(f"Arquivo não encontrado: {html_path}")
        sys.exit(1)

    size_mb = Path(html_path).stat().st_size / 1024 / 1024
    print(f"Arquivo: {html_path} ({size_mb:.1f} MB)")
    print("Lendo em chunks (sem carregar tudo na memória)...")

    videos = parse_stream(html_path)

    print(f"Total: {len(videos)} vídeos únicos encontrados.")

    out = Path(html_path).parent / "videos.json"
    out.write_text(json.dumps(videos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Salvo em: {out.resolve()}")


if __name__ == "__main__":
    main()
