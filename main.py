import markdown
import http.server
import socketserver
import sys
import os
import re

PORT = 7000 # Máximo permitido é 65535.
MAX_ATTEMPTS = 5  # Número máximo de portas para tentar

def get_title(md_content, md_file):
    """Extrai o título do Markdown ou usa o nome do arquivo."""
    match = re.search(r'^# (.+)', md_content, re.MULTILINE)
    return match.group(1) if match else os.path.basename(md_file).replace(".md", "").capitalize()

def generate_html(title, html_content):
    """Gera a estrutura do HTML com base no conteúdo do Markdown."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            max-width: 900px;
            margin: auto;
            padding: 20px;
            line-height: 1.8;
            background-color: #f4f4f4;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #222;
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }}
        a {{
            color: #007bff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        nav {{
            background: rgba(51, 51, 51, 0.9);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            color: white;
            padding: 10px;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            text-align: center;
            font-size: 18px;
            z-index: 1000;
        }}
        nav a {{
            color: white;
            margin: 0 15px;
            text-decoration: none;
            font-weight: bold;
        }}
        nav a:hover {{
            text-decoration: underline;
        }}
        pre {{
            background: #0d1117;
            color: #c9d1d9;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
        }}
        table {{
            display: block;
            overflow-x: auto;
            white-space: nowrap;
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}
        table, th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #007bff;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #f2f2f2;
        }}
    </style>
</head>
<body>

<nav>
    <a href="#">Início</a>
    <a href="#conteudo">Conteúdo</a>
    <a href="#tabelas">Tabelas</a>
    <a href="#codigo">Código</a>
</nav>

<div style="margin-top: 60px;">
    {html_content}
</div>

</body>
</html>
    """

def convert_markdown_to_html(md_file):
    """Converte um arquivo Markdown em HTML e o salva como index.html."""
    try:
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo Markdown: {e}")
        sys.exit(1)

    html_content = markdown.markdown(md_content, extensions=['extra', 'tables', 'fenced_code'])
    title = get_title(md_content, md_file)
    html_output = generate_html(title, html_content)

    try:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_output)
        print("✅ Arquivo HTML gerado com sucesso: index.html")
    except Exception as e:
        print(f"❌ Erro ao escrever o arquivo HTML: {e}")
        sys.exit(1)

def run_server(port=PORT):
    """Inicia um servidor HTTP local e tenta portas alternativas se necessário."""
    handler = http.server.SimpleHTTPRequestHandler

    for attempt in range(MAX_ATTEMPTS):
        try:
            with socketserver.TCPServer(("", port), handler) as httpd:
                print(f"🚀 Servidor rodando em http://localhost:{port}")
                httpd.serve_forever()
        except OSError:
            print(f"⚠️ Porta {port} ocupada, tentando {port+1}...")
            port += 1

    print("❌ Não foi possível iniciar o servidor após várias tentativas.")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🛑 Uso: python script.py arquivo.md")
        sys.exit(1)

    md_file = sys.argv[1]

    if not os.path.exists(md_file):
        print("🛑 Arquivo Markdown não encontrado.")
        sys.exit(1)

    convert_markdown_to_html(md_file)
    run_server()
