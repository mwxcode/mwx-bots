#!/usr/bin/env python3
"""Validação leve da vitrine MWX (só biblioteca padrão do Python).

Confere: arquivos referenciados, âncoras internas, imagens sem texto alternativo,
SVGs com XML válido, PNGs com assinatura válida, arquivos vazios e marcas de conflito.
Uso: python3 tools/validar.py   (sai com código 1 se encontrar problema)
"""
import glob, os, re, sys
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)
erros = []


def slug(titulo):
    t = re.sub(r"<[^>]+>", "", titulo).strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def ancoras(md):
    texto = open(md, encoding="utf-8").read()
    return {slug(h) for h in re.findall(r"^#+\s+(.*)$", texto, re.M)} | set(re.findall(r'<a name="([^"]+)"', texto))


mds = [f for f in glob.glob("**/*.md", recursive=True) if not f.startswith("node_modules")]
for md in mds:
    texto = open(md, encoding="utf-8").read()
    if re.search(r"^(<{7}|>{7}|={7})( |$)", texto, re.M):
        erros.append(f"{md}: marca de conflito de merge")
    corpo = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    pasta = os.path.dirname(md)
    for tag in re.findall(r"<img\b[^>]*>", corpo):
        if "alt=" not in tag:
            erros.append(f"{md}: imagem sem alt: {tag[:80]}")
    refs = re.findall(r'(?:href|src|srcset)="([^"]+)"', corpo) + re.findall(r"\]\(([^)\s]+)\)", corpo)
    for ref in refs:
        if ref.startswith(("http://", "https://", "mailto:")):
            continue
        caminho, _, ancora = ref.partition("#")
        alvo = os.path.normpath(os.path.join(pasta, caminho)) if caminho else md
        if caminho and not os.path.exists(alvo):
            erros.append(f"{md}: arquivo não encontrado: {ref}")
        elif ancora and alvo.endswith(".md") and ancora not in ancoras(alvo):
            erros.append(f"{md}: âncora não encontrada: {ref}")

for f in glob.glob("assets/**/*", recursive=True):
    if not os.path.isfile(f):
        continue
    if os.path.getsize(f) == 0:
        erros.append(f"{f}: arquivo vazio")
    if f.endswith(".svg"):
        try:
            ET.parse(f)
        except ET.ParseError as e:
            erros.append(f"{f}: SVG inválido ({e})")
    if f.endswith(".png"):
        with open(f, "rb") as fh:
            if fh.read(8) != b"\x89PNG\r\n\x1a\n":
                erros.append(f"{f}: PNG inválido")

if erros:
    print("\n".join(erros))
    print(f"\n{len(erros)} problema(s) encontrado(s).")
    sys.exit(1)
print(f"OK: {len(mds)} páginas e {len(glob.glob('assets/**/*.*', recursive=True))} recursos verificados.")
