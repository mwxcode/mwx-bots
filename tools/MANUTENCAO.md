# Guia de manutenção da vitrine

Guia interno para atualizar a vitrine sem criar divergências. Antes de abrir um PR, rode sempre:

```
python3 tools/validar.py --autoteste
python3 tools/validar.py
python3 tools/validar.py --externos   # opcional, só informa
```

O GitHub Actions roda os mesmos passos em todo push e pull request (`.github/workflows/validar.yml`).

## Regras que não mudam

- A vitrine não contém código-fonte dos sistemas.
- Nenhum token, `.env`, ID de servidor de cliente, dado de membro ou banco de dados entra no repositório. O validador procura padrões de credenciais, mas não substitui a revisão.
- A `main` só recebe alterações por pull request, com aprovação da MWX.
- Preços e condições comerciais só mudam com aprovação da MWX.

## Atualizar preços

A fonte dos valores é `dados/comercial.json`. Ao mudar um valor:

1. Atualize `dados/comercial.json`. A `economia` de cada plano é a soma dos sistemas individuais menos o valor do plano.
2. Atualize as tabelas em `README.md` (seção Planos) e em `docs/planos.md`.
3. Atualize o card do plano em `assets/plans/plano-<id>.svg`: o valor (`R$` seguido do preço), a linha `Economize R$ …/mês` e o atributo `aria-label`/`<title>`.
4. Atualize o texto alternativo (`alt`) dos cards no `README.md` e em `docs/planos.md`.
5. Rode o validador. Ele aponta:
   - economia que não fecha com a soma;
   - valor diferente entre o JSON, as tabelas e os cards;
   - qualquer `R$` nas páginas que não esteja cadastrado no JSON.

## Adicionar ou mudar um sistema ou plano

1. Cadastre o sistema ou plano em `dados/comercial.json`.
2. Crie ou atualize a página em `docs/bots/<sistema>.md` com o que está de fato implementado. Confira no código antes de publicar uma funcionalidade.
3. Atualize os cards (`assets/cards/sistema-<id>.svg`, `assets/plans/plano-<id>.svg`), a tabela de comandos (`docs/comandos.md`) e a tabela de dados em `docs/privacidade-e-dados.md`.
4. Rode o validador.

## Políticas comerciais e privacidade

- `docs/politicas-comerciais.md` só traz condições aprovadas. O que ainda não foi definido fica na seção "Condições combinadas na contratação". Quando a MWX aprovar uma regra, mova o item dessa lista para uma seção própria.
- `docs/privacidade-e-dados.md` descreve o que os sistemas guardam, conforme a implementação. Não declare backup automático, criptografia, prazos de retenção ou conformidade com a LGPD sem que existam de fato.

## Artes

- Identidade: fundo `#0A1628` / `#0D1B2E`, borda `#1D3859`, título `#F1F5F9`, texto `#B0C0D4`, destaque `#38BDF8`, azul `#2563EB`. Sem trilhas de circuito.
- Símbolo X e logotipo: use só os vetores oficiais em `assets/branding/marca/`.
- O banner principal (`assets/banners/banner-principal.png` e `banner-mobile.png`) é arte da MWX e não deve ser refeito.
- Cada arte larga tem uma versão `-mobile.svg`, usada até 1103 px de largura de tela. Ao criar uma arte nova para o README ou para as docs, crie as duas versões.
- Texto dentro de SVG precisa de contraste de pelo menos 4,5:1 com o fundo.
- Toda imagem precisa de `alt`. Imagens decorativas usam `alt=""` e ficam dentro de `<picture>`, para o GitHub não criar um link sem nome.
- Recursos que nenhuma página usa são apontados pelo validador. Os vetores de `assets/branding/marca/` são a exceção, porque são a origem das artes.

## Demonstrações

- As telas em `assets/telas/` são ilustrativas, com dados fictícios, e estão marcadas como tal no README.
- Capturas reais devem vir de um servidor de testes, com dados fictícios, sem tokens, webhooks, IDs de clientes ou dados de membros visíveis.
- Prefira imagens leves. Vídeos longos devem ficar hospedados fora do repositório e ser apenas linkados.
