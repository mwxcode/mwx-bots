# ⚙️ Requisitos e instalação

## O que é preciso

| Item | Detalhe |
|---|---|
| Node.js | 20 ou mais novo |
| Banco | PostgreSQL 14+ só para **Bate-Ponto** e **Encomendas** (os dois podem dividir o mesmo banco). Os demais usam arquivo JSON. |
| Hospedagem | PC ligado 24h, VPS ou painel de hospedagem de bots (ex.: Pterodactyl). 512 MB de RAM por bot é suficiente. |
| Discord | Um aplicativo no Developer Portal para cada bot |

## Passo a passo (resumo)

1. Criar o aplicativo no Discord Developer Portal e ativar os intents indicados na página de cada bot.
2. Colocar o token no arquivo `.env` (nunca compartilhe esse arquivo).
3. Instalar e ligar (`npm install`, `npm run build`, `npm start`).
4. No Discord, rodar o comando `/config-…` do bot e escolher canais e cargos.
5. Publicar os painéis.

O cliente recebe um guia detalhado para cada bot junto com o pacote.

## Integrações entre os bots

- **Atendimento + Management:** filtro de palavrões no assunto do ticket e nome/ID do registro no recrutamento.
- **Farm + Management:** nome e ID preenchidos a partir do registro.
- **Atendimento + Encomendas:** opção "Encomendas" dentro do painel de tickets.

## Segurança

- Nenhum ID de servidor, token ou senha fica no código.
- Dados gravados de forma segura (sem corromper se o bot cair no meio).
- Backup simples: pasta `data/` e banco PostgreSQL.
