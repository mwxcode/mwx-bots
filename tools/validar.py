#!/usr/bin/env python3
"""Validação da vitrine MWX.

Confere:
- Markdown/HTML: arquivos referenciados, âncoras internas, imagens sem alt,
  marcas de conflito de merge e tags HTML principais sem fechamento.
- PNG: decodificação completa (Pillow), dimensões e arquivo truncado.
- SVG: XML válido, raiz <svg>, viewBox, dimensões, IDs duplicados,
  referências url(#id) / href="#id" sem destino e dependências externas.
- Arquivos vazios em assets/.

Uso:
  python3 tools/validar.py              validação local (sai com 1 se houver problema)
  python3 tools/validar.py --autoteste  cria casos inválidos temporários e confere se são detectados
  python3 tools/validar.py --externos   classifica os links externos (só informa, nunca falha)
"""
import glob, os, re, shutil, sys, tempfile
import xml.etree.ElementTree as ET

try:
    from PIL import Image
except ImportError:  # sem Pillow cai para a checagem de assinatura
    Image = None

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PNG_SIG = b"\x89PNG\r\n\x1a\n"
SVG_NS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
TAGS_PAREADAS = ("details", "summary", "picture", "p", "a", "h1", "h2", "h3", "table", "sub")


def slug(titulo):
    t = re.sub(r"<[^>]+>", "", titulo).strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def ancoras(md):
    texto = open(md, encoding="utf-8").read()
    return {slug(h) for h in re.findall(r"^#+\s+(.*)$", texto, re.M)} | set(re.findall(r'<a name="([^"]+)"', texto))


def links_md(raiz):
    """Lista (arquivo, link) de todos os links e imagens das páginas."""
    saida = []
    for md in sorted(glob.glob("**/*.md", recursive=True)):
        corpo = re.sub(r"<!--.*?-->", "", open(md, encoding="utf-8").read(), flags=re.S)
        for ref in re.findall(r'(?:href|src|srcset)="([^"]+)"', corpo) + re.findall(r"\]\(([^)\s]+)\)", corpo):
            saida.append((md, ref))
    return saida


def validar_md(erros):
    mds = sorted(glob.glob("**/*.md", recursive=True))
    for md in mds:
        texto = open(md, encoding="utf-8").read()
        if not texto.strip():
            erros.append(f"{md}: arquivo vazio")
        if re.search(r"^(<{7}|>{7}|={7})( |$)", texto, re.M):
            erros.append(f"{md}: marca de conflito de merge")
        corpo = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
        corpo_html = re.sub(r"`[^`\n]*`", "", corpo)
        for tag in TAGS_PAREADAS:
            abre = len(re.findall(rf"<{tag}(?:\s[^>]*)?>", corpo_html))
            fecha = len(re.findall(rf"</{tag}>", corpo_html))
            if abre != fecha:
                erros.append(f"{md}: <{tag}> abertas {abre}, fechadas {fecha}")
        for tag in re.findall(r"<img\b[^>]*>", corpo):
            if "alt=" not in tag:
                erros.append(f"{md}: imagem sem alt: {tag[:80]}")
    for md, ref in links_md(RAIZ):
        if ref.startswith(("http://", "https://", "mailto:")):
            continue
        pasta = os.path.dirname(md)
        caminho, _, ancora = ref.partition("#")
        alvo = os.path.normpath(os.path.join(pasta, caminho)) if caminho else md
        if caminho and not os.path.exists(alvo):
            erros.append(f"{md}: arquivo não encontrado: {ref}")
        elif ancora and alvo.endswith(".md") and ancora not in ancoras(alvo):
            erros.append(f"{md}: âncora não encontrada: {ref}")
    return len(mds)


def validar_png(f, erros):
    with open(f, "rb") as fh:
        if fh.read(8) != PNG_SIG:
            erros.append(f"{f}: PNG inválido (assinatura)")
            return
    if Image is None:
        return
    try:
        with Image.open(f) as im:
            im.verify()  # estrutura e CRC dos blocos
        with Image.open(f) as im:
            im.load()  # decodifica todos os pixels; acusa arquivo truncado
            w, h = im.size
        if w < 1 or h < 1 or w > 8000 or h > 8000:
            erros.append(f"{f}: dimensões fora do esperado ({w}x{h})")
    except Exception as e:  # noqa: BLE001 - qualquer falha de decodificação é erro
        erros.append(f"{f}: PNG não decodifica ({type(e).__name__}: {e})")


def validar_svg(f, erros):
    try:
        raiz = ET.parse(f).getroot()
    except ET.ParseError as e:
        erros.append(f"{f}: SVG inválido ({e})")
        return
    if raiz.tag not in ("svg", SVG_NS + "svg"):
        erros.append(f"{f}: raiz não é <svg> ({raiz.tag})")
        return
    vb = raiz.get("viewBox")
    nums = re.findall(r"-?[\d.]+", vb or "")
    if len(nums) != 4 or float(nums[2]) <= 0 or float(nums[3]) <= 0:
        erros.append(f"{f}: viewBox ausente ou inválido ({vb})")
    for dim in ("width", "height"):
        v = raiz.get(dim)
        if v is not None and not re.fullmatch(r"[\d.]+(px|%)?", v):
            erros.append(f"{f}: {dim} inválido ({v})")
    ids, refs = [], set()
    for el in raiz.iter():
        if el.get("id"):
            ids.append(el.get("id"))
        for nome, valor in el.attrib.items():
            refs.update(re.findall(r"url\(\s*#([^)\s]+)\s*\)", valor))
            if nome in ("href", XLINK):
                if valor.startswith("#"):
                    refs.add(valor[1:])
                elif valor.strip():
                    erros.append(f"{f}: dependência externa em href ({valor[:60]})")
        if el.tag in ("style", SVG_NS + "style") and el.text:
            refs.update(re.findall(r"url\(\s*#([^)\s]+)\s*\)", el.text))
            if re.search(r"@import|url\(\s*['\"]?(https?:|//)", el.text):
                erros.append(f"{f}: dependência externa em <style>")
    duplicados = sorted({i for i in ids if ids.count(i) > 1})
    if duplicados:
        erros.append(f"{f}: IDs duplicados {duplicados}")
    faltando = sorted(refs - set(ids))
    if faltando:
        erros.append(f"{f}: referências sem destino {faltando}")


def validar_assets(erros):
    total = 0
    for f in sorted(glob.glob("assets/**/*", recursive=True)):
        if not os.path.isfile(f):
            continue
        total += 1
        if os.path.getsize(f) == 0:
            erros.append(f"{f}: arquivo vazio")
            continue
        if f.endswith(".svg"):
            validar_svg(f, erros)
        elif f.endswith(".png"):
            validar_png(f, erros)
    return total


def validar(raiz):
    anterior = os.getcwd()
    os.chdir(raiz)
    try:
        erros = []
        paginas = validar_md(erros)
        recursos = validar_assets(erros)
        return erros, paginas, recursos
    finally:
        os.chdir(anterior)


def autoteste():
    """Cria um repositório temporário com um caso inválido de cada tipo e confere a detecção."""
    tmp = tempfile.mkdtemp(prefix="mwx-validar-")
    try:
        os.makedirs(os.path.join(tmp, "assets"))
        ok_png = os.path.join(RAIZ, "assets", "telas", "farm-card.png")
        dados = open(ok_png, "rb").read()
        escrever = lambda nome, conteudo, modo="w": open(os.path.join(tmp, nome), modo).write(conteudo)
        escrever("README.md", "# Teste\n\n[falta](nao-existe.md)\n[ancora](#nao-existe)\n<img src=\"assets/ok.svg\">\n<details>\n\n<<<<<<< HEAD\n")
        escrever("vazio.md", "")
        escrever("assets/truncado.png", dados[: len(dados) // 2], "wb")
        escrever("assets/assinatura.png", b"nao e png", "wb")
        escrever("assets/quebrado.svg", "<svg><g></svg>")
        escrever("assets/raiz.svg", "<html/>")
        escrever("assets/ok.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"/>')
        escrever("assets/sem-viewbox.svg", '<svg xmlns="http://www.w3.org/2000/svg" width="10"/>')
        escrever("assets/ids.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><g id="a"/><g id="a"/><rect fill="url(#nada)"/></svg>')
        escrever("assets/externo.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><image href="https://exemplo.com/x.png"/></svg>')
        escrever("assets/vazio.svg", "")
        erros, _, _ = validar(tmp)
        texto = "\n".join(erros)
        esperados = {
            "referência ausente": "arquivo não encontrado: nao-existe.md",
            "âncora inválida": "âncora não encontrada: #nao-existe",
            "imagem sem alt": "imagem sem alt",
            "tag sem fechamento": "<details> abertas 1, fechadas 0",
            "marca de conflito": "marca de conflito",
            "markdown vazio": "vazio.md: arquivo vazio",
            "PNG truncado": "truncado.png: PNG não decodifica",
            "PNG com assinatura errada": "assinatura.png: PNG inválido",
            "SVG malformado": "quebrado.svg: SVG inválido",
            "raiz errada": "raiz.svg: raiz não é <svg>",
            "viewBox ausente": "sem-viewbox.svg: viewBox ausente",
            "ID duplicado": "ids.svg: IDs duplicados",
            "url(#id) sem destino": "ids.svg: referências sem destino",
            "dependência externa": "externo.svg: dependência externa",
            "SVG vazio": "vazio.svg: arquivo vazio",
        }
        falhas = [n for n, trecho in esperados.items() if trecho not in texto]
        falsos = [e for e in erros if "ok.svg:" in e]
        for nome in esperados:
            print(("FALHOU " if nome in falhas else "detectado ") + nome)
        if falsos:
            print("falso positivo:", falsos)
        if falhas or falsos:
            sys.exit(1)
        print(f"OK: autoteste detectou os {len(esperados)} casos inválidos.")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # nada fica no repositório


def externos():
    """Classifica links externos. Só informa: rede instável não deve quebrar a CI."""
    import urllib.request, urllib.error

    class SemRedirecionar(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    os.chdir(RAIZ)
    abrir = urllib.request.build_opener(SemRedirecionar).open
    vistos = {}
    for md, ref in links_md(RAIZ):
        if ref.startswith("mailto:"):
            ok = re.fullmatch(r"mailto:[^@\s]+@[^@\s]+\.[a-z]{2,}", ref)
            vistos.setdefault(ref, "válido (sintaxe de e-mail)" if ok else "QUEBRADO (e-mail malformado)")
        elif ref.startswith(("http://", "https://")) and ref not in vistos:
            req = urllib.request.Request(ref, headers={"User-Agent": "mwx-vitrine-validador"})
            try:
                with abrir(req, timeout=15) as r:
                    vistos[ref] = f"válido ({r.status})"
            except urllib.error.HTTPError as e:
                c = e.code
                if c in (301, 302, 303, 307, 308):
                    vistos[ref] = f"redirecionamento ({c} → {e.headers.get('Location', '?')})"
                elif c in (401, 403):
                    vistos[ref] = f"requer autenticação ou bloqueado pelo site ({c})"
                elif c == 429 or c >= 500:
                    vistos[ref] = f"temporariamente indisponível ({c})"
                elif c in (404, 410):
                    vistos[ref] = f"QUEBRADO ({c})"
                else:
                    vistos[ref] = f"resposta inesperada ({c})"
            except Exception as e:  # noqa: BLE001
                vistos[ref] = f"bloqueado pelo ambiente ou sem rede ({type(e).__name__})"
    for ref, estado in sorted(vistos.items()):
        print(f"{estado:55} {ref}")
    quebrados = [r for r, s in vistos.items() if s.startswith("QUEBRADO")]
    print(f"\n{len(vistos)} links externos; {len(quebrados)} quebrado(s).")


if __name__ == "__main__":
    if "--autoteste" in sys.argv:
        autoteste()
    elif "--externos" in sys.argv:
        externos()
    else:
        if Image is None:
            print("Aviso: Pillow não instalado; PNG verificado só pela assinatura.")
        erros, paginas, recursos = validar(RAIZ)
        if erros:
            print("\n".join(erros))
            print(f"\n{len(erros)} problema(s) encontrado(s).")
            sys.exit(1)
        print(f"OK: {paginas} páginas e {recursos} recursos verificados.")
