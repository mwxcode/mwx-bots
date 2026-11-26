# ⏱️ Bate-Ponto · Controle de expediente

Para polícia, hospital, mecânica, facção ou empresa: quem está em serviço, por quanto tempo e quem mais trabalhou.

![Bate-ponto](../../assets/telas/ponto-painel.png)

## Funções

- Painel fixo com botões **Iniciar**, **Pausar / Retornar** e **Encerrar**.
- Cargo "🟢 Em serviço" dado e tirado sozinho.
- Calls de expediente opcionais (ponto ligado à categoria de voz).
- Log em tempo real de cada início, pausa e fim.
- Tempo com o bot fora do ar **não conta**: o expediente é pausado e o membro é avisado.
- **Ranking** de horas (TOP 10) por semana, mês ou período.
- Consulta de horas por membro com **planilha .xlsx**.
- Relatórios, histórico e revisão de pontos pelo cargo revisor.
- Reset por período com confirmação.
- Vários servidores no mesmo bot.

## Comandos

| Comando | Para quê |
|---|---|
| `/config-ponto` | Cargo em serviço, logs, admin, revisor, nome, banner, cor |
| `/painel-ponto` | Publica o painel com os botões |
| `/horas-ponto` | Horas por membro e período, com planilha |
| `/ranking-ponto` `/relatorio-ponto` `/historico-ponto` | Consultas |
| `/resetar-ponto` | Zera um período (com confirmação) |
| `/reiniciar-ponto` | Reinício pelo Discord (admin) |

## Requisitos

Node.js 20+ e PostgreSQL 14+ (pode ser o mesmo banco das Encomendas).
