# 🛡️ Management · Administração e moderação

O "braço direito" da liderança: modera o chat, guarda o histórico de cada membro e organiza o servidor.

![Log de moderação](../../assets/telas/management-log.png)

## Funções

**Moderação**
- Advertências com cargos (ADV 1, ADV 2, ADV 3) e ação automática ao atingir o limite (castigo, expulsão ou banimento).
- Advertências que expiram sozinhas depois de um prazo configurável.
- Castigo, expulsão, banimento e desbanimento com motivo, registrados em log.
- Limpar mensagens, trancar canal e modo lento.

**Filtros automáticos**
- Bloqueio de convites de outros servidores, links e palavrões, com castigo após repetição.
- Filtro de **ofensas graves** (racismo, homofobia etc.) que vale até para a staff, com castigo imediato.
- Detecção de disfarces ("p.a.l.a.v.r.a", letras trocadas) sem bloquear palavras inocentes.
- Filtro de nomes e apelidos proibidos.
- Anti-flood.

**Registro de membros**
- Painel "Registre-se" com nome, sobrenome e ID do jogo.
- Apelido automático no formato `Nome Sobrenome | ID`.
- Liberação automática ou aprovação pela staff, com cargo dado e cargo removido.
- Busca de membro por ID.

**Ausências**
- Painel para pedir ausência com motivo e período.
- Aprovação por cargo responsável, cargo de ausente e fim automático na data marcada.

**Comunicação**
- `/anuncio` com janela de texto e **prévia** antes de publicar.
- Painel de booster.
- Boas-vindas, despedidas e cargo automático ao entrar.

**Estrutura do servidor**
- `/setup-servidor` monta cargos, categorias e canais a partir de um modelo, com prévia e confirmação. Não duplica o que já existe.

**Logs**
- Moderação, mensagens apagadas e editadas, entradas e saídas, auto-moderação.

## Comandos

| Grupo | Comandos |
|---|---|
| Moderação | `/advertir` `/advertencias` `/remover-advertencia` `/castigo` `/remover-castigo` `/expulsar` `/banir` `/desbanir` |
| Administração | `/limpar` `/cargo adicionar\|remover` `/apelido` |
| Canais | `/trancar` `/destrancar` `/modo-lento` |
| Comunicação | `/anuncio` `/painel-booster` |
| Informações | `/usuario-info` `/servidor-info` |
| Registro | `/registro painel\|config\|ver-config\|consultar\|buscar-id\|resetar` |
| Ausência | `/ausencia solicitar\|status\|painel\|lista\|encerrar` |
| Filtros | `/filtro palavra` `/filtro site` `/filtro ignorar` |
| Configuração | `/config-management` `/setup-servidor` `/ajuda-management` |

## Requisitos

Node.js 20+. Sem banco de dados (arquivo JSON). Intents: Server Members e Message Content.
