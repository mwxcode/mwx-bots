# 🌾 Farm · Registro de farm com análise

Fim das planilhas manuais: o membro registra, a equipe confere e o ranking sai sozinho.

![Farm](../../assets/telas/farm-card.png)

## Funções

- `/farm-setup` cria a categoria 🌾 FARM com avisos, painel, registros e log, já com as permissões certas.
- Membro registra **material, quantidade e print** pelo painel. Nome e ID vêm do registro.
- Equipe **aceita, recusa ou corrige** a quantidade. O membro recebe DM com o resultado.
- Materiais em menu (ex.: Pólvora, Cobre, Plástico).
- Metas semanais com cargo "Meta concluída" e reset automático.
- **TOP do mês** publicado sozinho na virada, com pódio.
- **Planilha .xlsx** com registros, totais por jogador e ranking.
- "Meus farms" para o membro acompanhar o que já enviou.

## Comandos

| Comando | Para quê |
|---|---|
| `/farm-setup` | Cria ou atualiza canais, permissões e painel |
| `/config-farm ver\|canais\|analisadores\|membros\|lideranca\|categoria-logs\|materiais\|top\|reenviar-painel` | Configuração |
| `/painelfarm` | Reenvia o painel |
| `/farm-planilha` | Planilha do mês |

## Requisitos

Node.js 20+. Sem banco de dados. Intent: Server Members.
