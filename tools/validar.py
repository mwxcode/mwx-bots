#!/usr/bin/env python3
"""Validação da vitrine MWX.

Confere:
- Markdown/HTML: arquivos referenciados, âncoras internas, imagens sem alt,
  marcas de conflito de merge e tags HTML principais sem fechamento.
- PNG: decodificação completa (Pillow), dimensões e arquivo truncado.
- SVG: XML válido, raiz <svg>, viewBox, dimensões, IDs duplicados,
  referências url(#id) / href="#id" sem destino e dependências externas.
- Arquivos vazios em assets/.
- Dados comerciais (dados/comercial.json): economia de cada plano igual à soma
  dos sistemas individuais menos o valor do plano, e os mesmos valores no README,
  em docs/planos.md e nos cards de plano (SVG e texto alternativo).
- Recursos em assets/ que nenhuma página usa, arquivos temporários e padrões
  de credenciais (tokens do Discord e do GitHub, chaves, URLs de banco com senha).

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


# ---------------------------------------------------------------- dados comerciais
def centavos(v):
    return int(v.replace(",", ""))


def reais(c):
    return f"{c // 100},{c % 100:02d}"


def validar_comercial(erros):
    """Confere dados/comercial.json contra as páginas e os cards de plano."""
    if not os.path.exists("dados/comercial.json"):
        return
    import json
    dados = json.load(open("dados/comercial.json", encoding="utf-8"))
    sistemas = {s["id"]: s for s in dados["sistemas"]}
    permitidos = {s["valor"] for s in sistemas.values()}
    for p in dados["planos"]:
        permitidos |= {p["valor"], p["economia"]}
        soma = sum(centavos(sistemas[i]["valor"]) for i in p["sistemas"])
        economia = soma - centavos(p["valor"])
        if economia <= 0:
            erros.append(f"comercial: {p['nome']} não é mais barato que os sistemas individuais")
        if economia != centavos(p["economia"]):
            erros.append(f"comercial: economia do {p['nome']} deveria ser R$ {reais(economia)} (soma R$ {reais(soma)} − R$ {p['valor']}), está R$ {p['economia']}")
        svg = f"assets/plans/plano-{p['id']}.svg"
        if os.path.exists(svg):
            texto = re.sub(r"<[^>]+>", " ", open(svg, encoding="utf-8").read())
            texto = re.sub(r"\s+", " ", texto)
            for trecho in (f"R$ {p['valor']}", f"Economize R$ {p['economia']}/mês"):
                if trecho not in texto:
                    erros.append(f"{svg}: falta '{trecho}' (dados/comercial.json)")
            for i in p["sistemas"]:
                if sistemas[i]["rotulo"] not in texto:
                    erros.append(f"{svg}: falta o sistema '{sistemas[i]['rotulo']}'")
    for md in ("README.md", "docs/planos.md"):
        if not os.path.exists(md):
            continue
        texto = open(md, encoding="utf-8").read()
        linhas = texto.splitlines()
        for p in dados["planos"]:
            linha = next((l for l in linhas if re.match(rf"\|\s*(\*\*)?{re.escape(p['nome'])}(\*\*)?\s*\|", l)), None)
            if linha is None:
                erros.append(f"{md}: plano {p['nome']} fora da tabela")
            elif f"R$ {p['valor']}" not in linha or f"R$ {p['economia']}" not in linha:
                erros.append(f"{md}: valores do {p['nome']} diferentes de dados/comercial.json")
            for alt in re.findall(rf'src="[^"]*plano-{p["id"]}\.svg"[^>]*alt="([^"]*)"|alt="([^"]*)"[^>]*src="[^"]*plano-{p["id"]}\.svg"', texto):
                alt = "".join(alt)
                if f"R$ {p['valor']}" not in alt:
                    erros.append(f"{md}: texto alternativo do card {p['id']} sem R$ {p['valor']}")
        for s_ in sistemas.values():
            linha = next((l for l in linhas if l.startswith("|") and f"{s_['nome']}]" in l), None)
            if linha is None:
                erros.append(f"{md}: sistema {s_['nome']} fora da tabela de sistemas individuais")
            elif f"R$ {s_['valor']}" not in linha:
                erros.append(f"{md}: valor do {s_['nome']} diferente de dados/comercial.json")
    for md in sorted(glob.glob("**/*.md", recursive=True)):
        for v in re.findall(r"R\$ ?(\d+,\d{2})", open(md, encoding="utf-8").read()):
            if v not in permitidos:
                erros.append(f"{md}: valor R$ {v} não cadastrado em dados/comercial.json")


# ---------------------------------------------------------------- higiene do repositório
FONTES_DA_MARCA = ("assets/branding/marca/",)  # vetores oficiais: origem das artes, não aparecem nas páginas
TEMPORARIOS = re.compile(r"(~$|\.(tmp|temp|bak|orig|rej|swp|log)$|^\.DS_Store$|^Thumbs\.db$|^desktop\.ini$)", re.I)
SEGREDOS = {
    "token do Discord": r"\b[MN][A-Za-z\d_-]{23,25}\.[A-Za-z\d_-]{6}\.[A-Za-z\d_-]{27,38}\b",
    "token do GitHub": r"\b(gh[pousr]_[A-Za-z\d]{36}|github_pat_[A-Za-z\d_]{40,})\b",
    "chave AWS": r"\bAKIA[0-9A-Z]{16}\b",
    "chave Google": r"\bAIza[\dA-Za-z_-]{35}\b",
    "chave privada": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "URL de banco com senha": r"\b(postgres(ql)?|mysql|mongodb(\+srv)?)://[^\s:/@]+:[^\s@/]+@(?!HOST\b)",
    "webhook do Discord": r"discord(app)?\.com/api/webhooks/\d+/[\w-]{20,}",
}
TEXTO = (".md", ".json", ".svg", ".yml", ".yaml", ".py", ".txt", ".js", ".ts", ".env", "")


def validar_higiene(erros):
    corpo = ""
    for md in glob.glob("**/*.md", recursive=True):
        corpo += open(md, encoding="utf-8").read()
    for f in sorted(glob.glob("assets/**/*", recursive=True)):
        if os.path.isfile(f) and not f.startswith(FONTES_DA_MARCA) and os.path.basename(f) not in corpo:
            erros.append(f"{f}: recurso não utilizado por nenhuma página")
    for pasta, dirs, arquivos in os.walk("."):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
        for a in arquivos:
            f = os.path.relpath(os.path.join(pasta, a))
            if TEMPORARIOS.search(a):
                erros.append(f"{f}: arquivo temporário")
            if os.path.splitext(a)[1].lower() in TEXTO and os.path.getsize(f) < 2_000_000:
                texto = open(f, encoding="utf-8", errors="ignore").read()
                for nome, padrao in SEGREDOS.items():
                    if re.search(padrao, texto):
                        erros.append(f"{f}: possível credencial exposta ({nome})")


def validar(raiz):
    anterior = os.getcwd()
    os.chdir(raiz)
    try:
        erros = []
        paginas = validar_md(erros)
        recursos = validar_assets(erros)
        validar_comercial(erros)
        validar_higiene(erros)
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
        os.makedirs(os.path.join(tmp, "dados"))
        escrever("dados/comercial.json", '{"sistemas": [{"id": "a", "nome": "MWX A", "rotulo": "A", "valor": "10,00"},'
                 ' {"id": "b", "nome": "MWX B", "rotulo": "B", "valor": "20,00"}],'
                 ' "planos": [{"id": "ab", "nome": "MWX AB", "sistemas": ["a", "b"], "valor": "25,00", "economia": "4,00"}]}')
        escrever("precos.md", "| MWX AB | A · B | R$ 25,00 | R$ 4,00/mês |\n\nPromoção: R$ 19,99\n")
        escrever("notas.md~", "rascunho")
        escrever("config.md", "DISCORD_TOKEN=" + "M" + "A" * 23 + "." + "B" * 6 + "." + "C" * 27 + "\n")
        escrever("assets/orfao.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"/>')
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
            "economia que não fecha com a soma": "economia do MWX AB deveria ser R$ 5,00",
            "preço fora dos dados comerciais": "valor R$ 19,99 não cadastrado",
            "arquivo temporário": "notas.md~: arquivo temporário",
            "credencial exposta": "config.md: possível credencial exposta (token do Discord)",
            "recurso não utilizado": "orfao.svg: recurso não utilizado",
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
