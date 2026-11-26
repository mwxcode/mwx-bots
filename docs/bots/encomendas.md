# 📦 Encomendas · Pedidos com catálogo

Loja da organização dentro do Discord: o cliente escolhe, vê o total e a equipe acompanha até a entrega.

![Encomendas](../../assets/telas/encomenda-resumo.png)

## Funções

- Painel fixo com botão **Realizar encomenda**.
- Catálogo com preço, menu de produtos e quantidades.
- **Resumo com valor total** antes de confirmar.
- Ticket do pedido aberto sozinho, numerado (ex.: `📦・0012-colete`).
- Canal de pedidos para a equipe **aceitar, negar e concluir** a entrega, com aviso ao cliente.
- Limites de quantidade por produto.
- Pode aparecer como opção dentro do painel do Atendimento.

## Comandos

| Comando | Para quê |
|---|---|
| `/config-encomenda` | Categoria, canal de pedidos, cargos, nome, cor e aparência do bot |
| `/produtos-encomenda adicionar\|editar\|remover\|listar\|padrao` | Catálogo |
| `/painel-encomenda` | Publica o painel |
| `/reiniciar-encomenda` | Reinício pelo Discord (admin) |

## Requisitos

Node.js 20+ e PostgreSQL 14+.
