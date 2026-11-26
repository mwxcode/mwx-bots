<picture>
  <source media="(max-width: 1103px)" srcset="../../assets/banners/doc-farm-mobile.svg">
  <img src="../../assets/banners/doc-farm.svg" alt="MWX Farm: registro de farm com análise, metas e TOP do mês" width="100%">
</picture>

<p align="center"><a href="../../README.md#nossos-sistemas">Catálogo</a> · <a href="../../docs/comandos.md">Comandos</a> · <a href="../../docs/planos.md">Planos</a> · <a href="../../README.md#contato">Contato</a></p>

## Apresentação

O MWX Farm acaba com as planilhas manuais: o membro registra com prova, a equipe confere e o ranking sai sozinho.

<br>

<img src="../../assets/branding/secao-funcionalidades.svg" alt="" width="100%">

## Funcionalidades

### Estrutura

- `/farm-setup` cria a categoria do farm com avisos, painel, registros e log, já com as permissões
- Materiais em menu (por exemplo Pólvora, Cobre, Plástico)

### Registro e análise

- Registro de material, quantidade e print pelo painel
- Equipe aceita, recusa ou corrige a quantidade
- Membro recebe DM com o resultado
- Consulta dos próprios registros pelo membro

### Metas e ranking

- Metas semanais com cargo de meta concluída e reset automático
- TOP do mês publicado na virada, com pódio
- Planilha .xlsx com registros, totais por jogador e ranking

## Benefícios

- Produção comprovada por print e conferida pela equipe
- Metas acompanhadas sem conta manual
- Reconhecimento mensal automático dos que mais produzem

## Demonstrações

<img src="../../assets/telas/farm-card.png" alt="Card de registro de farm em análise" width="100%">

<sub>Cada registro chega com prova e progresso da meta para a equipe conferir.</sub>

<sub>Imagens ilustrativas da interface, com dados fictícios.</sub>

<br>

<img src="../../assets/branding/secao-comandos.svg" alt="" width="100%">

## Comandos

| Comando | Para quê |
|---|---|
| `/farm-setup` | Cria ou atualiza canais, permissões e painel |
| `/config-farm ver\|canais\|analisadores\|membros\|lideranca\|categoria-logs\|materiais\|top\|reenviar-painel` | Configuração |
| `/painelfarm` | Reenvia o painel |
| `/farm-planilha` | Planilha do mês |

<br>

<img src="../../assets/branding/secao-requisitos.svg" alt="" width="100%">

## Requisitos técnicos

- Node.js 20 ou mais novo
- Sem banco de dados: dados em arquivo JSON
- Intent privilegiado: Server Members

## Integrações

- Com o [MWX Management](management.md): nome e ID preenchidos a partir do registro

<br>

<img src="../../assets/branding/divisor.svg" alt="" width="100%">

<p align="center"><a href="../../README.md#nossos-sistemas"><b>← Voltar ao catálogo</b></a> · <a href="../../docs/planos.md">Conhecer os planos</a> · <a href="../../README.md#contato">Falar com a MWX</a></p>

<p align="center"><sub>© 2026 MWX Systems · Sua organização. Nossa tecnologia.</sub></p>
