<p align="center">
  <img src="assets/banner-v2.png" alt="MWX Bots" width="100%">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/apresentacao-escura.png">
    <img src="assets/apresentacao-clara.png" alt="MWX BOTS · Tecnologia que transforma a gestão do seu Roleplay. Atendimento, Recrutamento, Bate-ponto, Controle de farm, Encomendas e Moderação." width="100%">
  </picture>
</p>

---

> **Este repositório é uma vitrine.** Aqui você vê o que cada bot faz, os comandos e as telas.
> O código-fonte é entregue somente aos clientes, sob licença de uso. Veja [Planos](docs/planos.md).

## Por que usar

- **Tudo em português**, com textos pensados para RP: cidadão, recrutamento, cúpula, farm, expediente.
- **Configurado pelo próprio Discord.** Nenhum ID fixo no código: canais, cargos e categorias são escolhidos por comandos `/config-*`.
- **Visual padronizado.** Painéis com o ícone do seu servidor, sua cor e seu nome no rodapé.
- **Prova de tudo.** Logs de cada ação, transcript HTML dos tickets e planilhas `.xlsx` de horas e farm.
- **Estável.** Travas contra clique duplo, gravação segura dos dados, religamento automático e testes automatizados.
- **Modular.** Compre só o que precisa. Os bots conversam entre si quando instalados juntos.

## Os bots

| | Bot | O que resolve | Banco |
|---|---|---|---|
| 🛡️ | [**Management**](docs/bots/management.md) | Moderação, advertências, filtros, registro de membros, ausências, anúncios e estrutura do servidor | Arquivo JSON |
| 🎫 | [**Atendimento**](docs/bots/atendimento.md) | Tickets por assunto com transcript HTML e **recrutamento** com perguntas, prova e entrevista | Arquivo JSON |
| ⏱️ | [**Bate-Ponto**](docs/bots/ponto.md) | Expediente com iniciar/pausar/encerrar, cargo em serviço, ranking e planilha de horas | PostgreSQL |
| 🌾 | [**Farm**](docs/bots/farm.md) | Registro de farm com print, análise da equipe, metas e TOP do mês com planilha | Arquivo JSON |
| 📦 | [**Encomendas**](docs/bots/encomendas.md) | Catálogo, carrinho, valor total, ticket automático e entrega acompanhada | PostgreSQL |
| 🚨 | [**Denúncias**](docs/bots/denuncias.md) | Denúncias com protocolo, prova, análise da staff e resposta por DM | Arquivo JSON |

Também sob encomenda: **Controle de Efetivo**, **Confirmação de presença por DM**, **DM em massa** e **Desligamento de membros**. Veja [Módulos extras](docs/bots/extras.md).

## Telas

<table>
  <tr>
    <td width="50%"><img src="assets/telas/atendimento-painel.png" alt="Painel de atendimento"><br><sub>Painel de atendimento</sub></td>
    <td width="50%"><img src="assets/telas/recrutamento-card.png" alt="Card de recrutamento"><br><sub>Recrutamento com nota da prova</sub></td>
  </tr>
  <tr>
    <td><img src="assets/telas/ponto-painel.png" alt="Bate-ponto"><br><sub>Bate-ponto e ranking de horas</sub></td>
    <td><img src="assets/telas/farm-card.png" alt="Farm"><br><sub>Registro e análise de farm</sub></td>
  </tr>
  <tr>
    <td><img src="assets/telas/encomenda-resumo.png" alt="Encomendas"><br><sub>Resumo de encomenda</sub></td>
    <td><img src="assets/telas/management-log.png" alt="Moderação"><br><sub>Log de moderação</sub></td>
  </tr>
</table>

<sub>Telas com dados fictícios. Cores, nome e ícone mudam conforme o seu servidor.</sub>

## Comandos

A lista completa, bot por bot, está em [docs/comandos.md](docs/comandos.md). Um resumo:

| Bot | Principais comandos |
|---|---|
| Management | `/advertir` `/castigo` `/banir` `/registro` `/ausencia` `/anuncio` `/filtro` `/setup-servidor` |
| Atendimento | `/config-ticket` `/config-recrutamento` `/tickets-painel` `/ticket-assumir` `/ticket-fechar` |
| Bate-Ponto | `/config-ponto` `/painel-ponto` `/horas-ponto` `/ranking-ponto` `/relatorio-ponto` |
| Farm | `/farm-setup` `/config-farm` `/painelfarm` `/farm-planilha` |
| Encomendas | `/config-encomenda` `/produtos-encomenda` `/painel-encomenda` |

## Como funciona a contratação

1. **Conversa:** você diz qual organização é e quais bots quer.
2. **Instalação:** colocamos os bots no seu servidor (ou entregamos o pacote para você hospedar).
3. **Configuração:** canais, cargos, cores e textos ajustados ao seu RP.
4. **Suporte:** ajustes e atualizações conforme o plano.

Detalhes técnicos em [docs/instalacao.md](docs/instalacao.md) e dúvidas em [docs/faq.md](docs/faq.md).

## Planos

| Plano | Para quem | Valor |
|---|---|---|
| **Bot avulso** | Precisa de um sistema só | `R$ ___` |
| **Pacote completo** | Os 6 bots, configurados | `R$ ___` |
| **Aluguel mensal** | Hospedagem + suporte inclusos | `R$ ___ /mês` |

Comparativo completo em [docs/planos.md](docs/planos.md).

## Contato

- **Discord:** `SEU_USUARIO` · servidor de suporte: `https://discord.gg/SEU_CONVITE`
- **E-mail / WhatsApp:** `SEU_CONTATO`

---

<p align="center"><sub>© MWX Bots. Todos os direitos reservados. Discord é marca da Discord Inc.; este projeto não é afiliado ao Discord.</sub></p>
