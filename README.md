# MarkHTM
Script de automação para facilitar a visualização de arquivos Markdown transformando em HTML

# Instalação
```bash
git clone https://github.com/Zer0G0ld/MarkHTM.git
cd MarkHTM
sudo apt update -y && sudo apt upgrade -y
sudo apt install python3-markdown
sudo apt install python3.11-venv
python3 -m venv venv
source venv/bin/activate
pip install markdown
```
# Como rodar 
```bash
python3 main.py README.md
```

você precisará passar o caminho do seu arquivo md como exemplo esse `README.md` isso abrirá um caminho no seu navegador esta configurado para a porta `7000` mas pode ser alterada por padrão será essa acesse `localhost:7000` e verá o arquivo impresso.

# Licença
Projeto sob a [Licença](LICENSE).
