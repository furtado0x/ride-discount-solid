# Sistema de Descontos para Corridas - Demonstracao Open/Closed Principle

## Card do Jira

---

### [RIDE-1234] Implementar Sistema de Calculo de Descontos

**Tipo:** Story
**Prioridade:** Alta
**Sprint:** 14
**Story Points:** 8
**Assignee:** Voce

#### Descricao

Preciso que voce implemente um sistema de calculo de descontos para nossa plataforma de corridas. O sistema deve aplicar diferentes tipos de descontos baseados em regras de negocio especificas.

#### Criterios de Aceitacao

1. O sistema deve aplicar desconto progressivo por frequencia de uso (baseado em numero total de corridas)
2. O sistema deve aplicar desconto proporcional a distancia percorrida
3. O sistema deve aplicar desconto por horario off-peak (madrugada e meio-dia)
4. Os descontos devem ser acumulativos com limite maximo de 50%
5. **IMPORTANTE:** O sistema deve ser facilmente extensivel para novos tipos de desconto sem modificar codigo existente
6. **IMPORTANTE:** Nao usar valores hardcoded - todos os descontos devem ser baseados em calculos

#### Comentario do Tech Lead

"Galera, esse sistema vai crescer MUITO. Hoje sao 3 tipos de desconto, mas ja temos no roadmap: desconto de milestone, happy hour, primeira corrida do dia, parceiros corporativos, etc. Preciso que seja facil adicionar novos descontos sem quebrar o que ja existe. E, por favor, sem valores hardcoded! Usem formulas e calculos. Lembrem-se dos principios SOLID, especialmente o Open/Closed!"

---

## O Principio Open/Closed (O do SOLID)

### Definicao

> **"Software entities should be OPEN for extension, but CLOSED for modification"**
> *"Entidades de software devem estar ABERTAS para extensao, mas FECHADAS para modificacao"*
> — Bertrand Meyer

### O que isso significa na pratica?

- **ABERTO para extensao:** Voce deve conseguir adicionar novos comportamentos e funcionalidades
- **FECHADO para modificacao:** Sem alterar o codigo que ja existe e esta funcionando

### Por que e importante?

1. **Reduz bugs:** Nao mexer em codigo funcionando = menos chance de quebrar algo
2. **Facilita manutencao:** Adicionar features vira apenas criar codigo novo
3. **Melhora testabilidade:** Testes existentes continuam passando
4. **Acelera desenvolvimento:** Time pode trabalhar em paralelo sem conflitos

## As Regras de Desconto (Baseadas em Calculos)

### 1. Desconto por Frequencia de Uso

**Como funciona:**
- A cada 10 corridas completadas, o cliente ganha 1% de desconto
- O desconto cresce progressivamente com o uso do app
- Limite maximo de 15% para evitar prejuizo

**Formula Matematica:**
```
desconto = min(total_corridas / 10, 15)
```

**Exemplos Praticos:**
- Cliente novo (5 corridas) = 0% desconto
- Cliente regular (30 corridas) = 3% desconto
- Cliente frequente (75 corridas) = 7% desconto
- Cliente fiel (150+ corridas) = 15% desconto (maximo)

**Por que essa abordagem?**
- Incentiva fidelidade de forma progressiva
- Sem necessidade de criar "tiers" artificiais (Bronze, Silver, Gold)
- Escala automaticamente com o comportamento do usuario

### 2. Desconto por Distancia Percorrida

**Como funciona:**
- Primeiros 5km nao tem desconto (distancia base)
- A partir do 6º km, cada quilometro adicional gera 0.5% de desconto
- Limite maximo de 20% para viagens muito longas

**Formula Matematica:**
```
se distancia > 5km:
    desconto = min((distancia - 5) x 0.5, 20)
senao:
    desconto = 0
```

**Exemplos Praticos:**
- Corrida curta (3km) = 0% desconto
- Corrida media (10km) = 2.5% desconto
- Corrida longa (25km) = 10% desconto
- Corrida muito longa (45km+) = 20% desconto (maximo)

**Por que essa abordagem?**
- Incentiva corridas mais longas (maior receita)
- Progressao suave sem "saltos" abruptos de desconto
- Compensa o cliente pelo tempo gasto no carro

### 3. Desconto por Horario Off-Peak

**Como funciona:**
- Sistema verifica o horario atual da corrida
- Aplica desconto em horarios de menor demanda
- Ajuda a distribuir melhor a demanda ao longo do dia

**Regras de Horario:**
- **Madrugada (0h as 6h):** 20% de desconto
  - Compensa motoristas por trabalhar de madrugada
  - Incentiva uso em horario de baixissima demanda

- **Meio-dia em dias uteis (10h as 16h):** 10% de desconto
  - Segunda a sexta-feira apenas
  - Horario entre rush matinal e vespertino
  - Nao se aplica em fins de semana (alta demanda de lazer)

**Exemplos Praticos:**
- Corrida as 3h (madrugada) = 20% desconto
- Corrida as 14h30 numa terca = 10% desconto
- Corrida as 14h30 num sabado = 0% desconto
- Corrida as 18h (rush) = 0% desconto

**Por que essa abordagem?**
- Baseado em dados reais de demanda
- Nao precisa de codigos promocionais
- Ajusta automaticamente com dia da semana

## Como Cada Desenvolvedor Abordaria o Problema

### Desenvolvedor Junior - "Vou fazer funcionar!"

**Arquivo:** `1_junior_version.py`

**Pensamento:**
*"Beleza, preciso fazer um calculo de desconto. Vou criar uma funcao que recebe os dados e calcula tudo com if/else. Simples e direto!"*

**Abordagem:**
```python
def calculate_ride_price(total_rides, distance_km, base_price, ride_datetime):
    # Desconto por frequencia
    if total_rides > 0:
        frequency_discount = min(total_rides // 10, 15)
        total_discount += frequency_discount

    # Desconto por distancia
    if distance_km > 5:
        distance_discount = min((distance_km - 5) * 0.5, 20)
        total_discount += distance_discount

    # Desconto off-peak
    current_hour = ride_datetime.hour
    if 0 <= current_hour < 6:
        total_discount += 20
    # ... mais ifs
```

**Problemas:**
- Para adicionar novo desconto = modificar a funcao inteira
- Funcao gigante com multiplas responsabilidades
- Dificil de testar cada regra isoladamente
- Alto risco de quebrar descontos existentes

**Quando o Tech Lead pede desconto de milestone:**
*"Ah, e so adicionar mais um if ne?"* - Adiciona mais um if no meio de 50 linhas de codigo...

### Desenvolvedor Pleno - "Vou organizar melhor!"

**Arquivo:** `2_mid_level_version.py`

**Pensamento:**
*"Essa funcao unica nao escala. Vou criar uma classe com metodos separados para cada tipo de desconto. Assim fica mais organizado!"*

**Abordagem:**
```python
class RideDiscountCalculator:
    def calculate_frequency_discount(self, ride):
        total_rides = ride.customer.total_rides
        return min(total_rides // 10, 15) if total_rides > 0 else 0

    def calculate_distance_discount(self, ride):
        if ride.distance_km > 5:
            return min((ride.distance_km - 5) * 0.5, 20)
        return 0

    def calculate_final_price(self, ride):
        frequency = self.calculate_frequency_discount(ride)
        distance = self.calculate_distance_discount(ride)
        offpeak = self.calculate_offpeak_discount(ride)
        # ... combina todos
```

**Melhorias:**
- Codigo mais organizado e legivel
- Usa dataclasses para modelagem
- Metodos com responsabilidade unica
- Usa calculos em vez de valores hardcoded
- Ainda viola Open/Closed
- Precisa modificar `calculate_final_price()` para novos descontos

**Quando o Tech Lead pede desconto de milestone:**
*"Ok, vou adicionar um novo metodo e alterar o calculate_final_price..."* - Ainda precisa modificar codigo existente.

### Desenvolvedor Senior - "Vou fazer extensivel!"

**Arquivo:** `3_senior_version.py`

**Pensamento:**
*"O Tech Lead ja avisou que vao vir muitos tipos de desconto. Vou usar o padrao Strategy com auto-registro. Assim, adicionar novo desconto e so criar uma classe nova, sem tocar em NADA do que ja existe."*

**Abordagem:**
```python
class DiscountRule(ABC):
    registered_rules = []

    def __init_subclass__(cls):
        DiscountRule.registered_rules.append(cls)

    @abstractmethod
    def calculate_discount(self, context):
        pass

class RideFrequencyDiscountRule(DiscountRule):
    def calculate_discount(self, context):
        total_rides = context.customer.total_rides
        if total_rides == 0:
            return None

        discount = min(total_rides // 10, 15)
        if discount > 0:
            return DiscountResult(discount, f"Frequency discount ({total_rides} rides)")

# Auto-registrado! Calculator aplica todas as regras automaticamente
```

**Vantagens:**
- Totalmente aderente ao Open/Closed
- Cada regra e uma classe independente (testavel isoladamente)
- Auto-registro = zero configuracao
- Novos descontos = nova classe, so isso!
- Impossivel quebrar descontos existentes
- Usa calculos, nao valores hardcoded

**Quando o Tech Lead pede desconto de milestone:**
*"Sem problemas!"* - Cria `MilestoneDiscountRule`, commita, deploya. Fim.

## Demonstracao Pratica

### Adicionando Novo Desconto de Milestone (bonus ao completar 10, 25, 50, 100... corridas)

**Junior:** Modifica funcao de 100 linhas, reza para nao quebrar nada
```python
# Dentro da funcao gigante...
milestones = [10, 25, 50, 100, 250, 500]
if total_rides in milestones:
    total_discount += 5  # Novo if no meio do codigo
```

**Pleno:** Adiciona metodo + modifica metodo principal
```python
def calculate_milestone_discount(self, ride):  # Novo metodo
    milestones = [10, 25, 50, 100, 250, 500]
    return 5 if ride.customer.total_rides in milestones else 0

def calculate_final_price(self, ride):
    # ...
    milestone = self.calculate_milestone_discount(ride)  # Modifica aqui
    # ...
```

**Senior:** So cria nova classe
```python
class MilestoneDiscountRule(DiscountRule):
    def calculate_discount(self, context):
        milestones = [10, 25, 50, 100, 250, 500]
        if context.customer.total_rides in milestones:
            return DiscountResult(
                Decimal("5"),
                f"Milestone bonus! {context.customer.total_rides}th ride"
            )
# Pronto! Auto-registrado e funcionando!
```

## Comparacao de Impacto

| Metrica | Junior | Pleno | Senior |
|---------|--------|-------|--------|
| Linhas modificadas para adicionar desconto | ~10-15 | ~5-8 | 0 |
| Risco de quebrar funcionalidade existente | Alto | Medio | Zero |
| Facilidade para testar nova regra | Dificil | Medio | Facil |
| Pode dar conflito no Git? | Sim | Sim | Nao |
| Precisa de regressao completa? | Sim | Sim | Nao |
| Usa valores hardcoded? | Nao* | Nao | Nao |

*Junior usa calculos mas ainda mistura tudo na mesma funcao

## Licoes Aprendidas

1. **Open/Closed nao e sobre "nunca modificar codigo"**
   E sobre estruturar seu codigo de forma que novos requisitos sejam implementados atraves de ADICAO, nao MODIFICACAO

2. **Abstracao e a chave**
   Classes abstratas e interfaces permitem que voce defina contratos que novas implementacoes podem seguir

3. **Auto-registro e poderoso**
   O padrao usado no codigo senior (`__init_subclass__`) remove ate a necessidade de registrar manualmente

4. **Clean Code + SOLID = Excelencia**
   Nao basta seguir SOLID, o codigo deve ser limpo (sem hardcoded values)

5. **Evolucao natural**
   Nao precisa comecar com a solucao mais complexa, mas reconheca quando e hora de evoluir

## Como Executar

```bash
# Testar versao junior
python 1_junior_version.py

# Testar versao pleno
python 2_mid_level_version.py

# Testar versao senior
python 3_senior_version.py

# Ver comparacao evolutiva
python evolution_comparison.py

# Demonstrar Open/Closed com versao senior
python example_usage.py

# Testar com dados personalizados
python test_senior.py
```

### Resultado Esperado

Com os dados de exemplo (75 corridas, 25km, 14:30h em dia util):

```
Desconto por Frequencia: 7% (75 / 10 = 7.5, arredonda para 7)
Desconto por Distancia: 10% ((25 - 5) x 0.5 = 10)
Desconto Off-Peak: 10% (14:30 esta entre 10h e 16h)
---------------------------------------------------
Total de Descontos: 27%
Preco Original: $45.00
Desconto: $12.15
Preco Final: $32.85
```

## Conclusao

O principio Open/Closed nao e apenas uma boa pratica teorica - e uma necessidade pratica em sistemas que evoluem. A diferenca entre as implementacoes nao esta na funcionalidade (todas calculam o mesmo desconto), mas na **manutenibilidade** e **extensibilidade** do codigo.

Alem disso, usar **calculos em vez de valores hardcoded** torna o sistema ainda mais flexivel e profissional. As regras de negocio mudam, mas as formulas permanecem!

### Pontos-Chave para Lembrar:

- **Hoje** voce tem 3 tipos de desconto
- **Amanha** podem ser 30
- **Preparar o codigo para o futuro** economiza tempo e dinheiro
- **Formulas > Valores Hardcoded** sempre!

---

*"Um bom desenvolvedor resolve o problema de hoje. Um excelente desenvolvedor resolve o problema de hoje pensando no amanha, e um desenvolvedor excepcional faz isso sem valores hardcoded!"*
