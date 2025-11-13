# Regra de Desconto de Final de Semana

## Descrição e Objetivo

A regra de desconto de final de semana tem como objetivo incentivar o uso do serviço de corridas durante os sábados e domingos, período em que tipicamente há menor demanda de transporte profissional (commuting para trabalho).

Esta regra complementa o sistema de descontos existente, focando em padrões de uso semanal, diferentemente da regra de off-peak que foca em horários específicos do dia.

## Como Funciona a Lógica

A regra verifica o dia da semana em que a corrida está sendo solicitada através do `ride_datetime`:

- **Sábado (weekday = 5)** ou **Domingo (weekday = 6)**: Aplica desconto de **10%**
- **Dias úteis (Segunda a Sexta)**: Nenhum desconto aplicado por esta regra

