# Sistema de Descontos para Corridas (UBER)
## Demonstração Prática do Open/Closed Principle (SOLID)

> 🎯 **Objetivo:** Simular como desenvolvedores Junior, Pleno e Senior resolveriam a mesma task,
> mostrando a evolução da aplicação com princípios SOLID na prática.

---

## 📋 O Card/Task do Jira

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                          🎫 JIRA TICKET                                   ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ID: RIDE-1234                                    Type: 📖 Story          ║
║  Title: Implementar Sistema de Calculo de Descontos                       ║
║                                                                           ║
║  Priority: 🔴 Alta            Sprint: 14           Points: 8              ║
║  Assignee: Voce              Status: 📝 To Do                             ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  📝 DESCRICAO                                                             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  Preciso que voce implemente um sistema de calculo de descontos para      ║
║  nossa plataforma de corridas. O sistema deve aplicar diferentes tipos    ║
║  de descontos baseados em regras de negocio especificas.                  ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  ✅ CRITERIOS DE ACEITACAO                                                ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  [ ] Aplicar desconto progressivo por frequencia de uso                   ║
║  [ ] Aplicar desconto proporcional a distancia percorrida                 ║
║  [ ] Aplicar desconto por horario off-peak (madrugada e meio-dia)         ║
║  [ ] Descontos acumulativos com limite maximo de 50%                      ║
║  [ ] Sistema extensivel para novos descontos SEM modificar codigo         ║
║  [ ] Usar calculos dinamicos (NAO usar valores hardcoded)                 ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  💬 COMENTARIOS                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  👨‍💼 Tech Lead (hoje as 09:23):                                            ║
║                                                                           ║
║  "Galera, esse sistema vai crescer MUITO. Hoje sao 3 tipos de desconto,   ║
║   mas ja temos no roadmap: desconto de milestone, happy hour, primeira    ║
║   corrida do dia, parceiros corporativos, etc.                            ║
║                                                                           ║
║                                                                           ║
║   Lembrem-se dos principios SOLID, especialmente o Open/Closed!"          ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 📐 As Regras de Negócio (Entendendo o Problema)

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

---

## 🎓 O Princípio Open/Closed (O do SOLID)

### Definição

> **"Software entities should be OPEN for extension, but CLOSED for modification"**
>
> *"Entidades de software devem estar ABERTAS para extensão, mas FECHADAS para modificação"*
>
> — Bertrand Meyer

### O que isso significa na prática?

- **ABERTO para extensão:** Você deve conseguir adicionar novos comportamentos e funcionalidades
- **FECHADO para modificação:** Sem alterar o código que já existe e está funcionando

### Por que é importante?

1. **Reduz bugs:** Não mexer em código funcionando = menos chance de quebrar algo
2. **Facilita manutenção:** Adicionar features vira apenas criar código novo
3. **Melhora testabilidade:** Testes existentes continuam passando
4. **Acelera desenvolvimento:** Time pode trabalhar em paralelo sem conflitos

---

## 👨‍💻 Simulação: Como Cada Perfil Resolveria a Task

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
*"O Tech Lead ja avisou que vao vir muitos tipos de desconto. Vou implementar o Open/Closed Principle com auto-registro de regras. Assim, adicionar novo desconto e so criar uma classe nova, sem tocar em NADA do que ja existe. Todas as regras aplicaveis serao executadas e seus descontos agregados."*

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

# Auto-registrado! Calculator itera por TODAS as regras e agrega os descontos
```

**Vantagens:**
- Totalmente aderente ao Open/Closed Principle
- TODAS as regras sao avaliadas e descontos agregados automaticamente
- Cada regra e uma classe independente (testavel isoladamente)
- Auto-registro = zero configuracao
- Novos descontos = nova classe, so isso!
- Impossivel quebrar descontos existentes
- Usa calculos, nao valores hardcoded
- Multiplos descontos podem ser aplicados simultaneamente (acumulativos)

**Quando o Tech Lead pede desconto de milestone:**
*"Sem problemas!"* - Cria `MilestoneDiscountRule`, commita, deploya. Fim.

---

## 🔄 Implementações Reais: O Código Já Está Pronto!

Este repositório já contém as **três implementações completas**, demonstrando a evolução da qualidade do código:

### 📁 Estrutura dos Arquivos

```
o_solid/
├── src/
│   └── ride_discount/
│       ├── domain/              # Implementação SENIOR (Open/Closed)
│       │   ├── models/          # Entidades de domínio
│       │   └── rules/           # Regras de desconto extensíveis
│       │       ├── base.py      # Classe abstrata com auto-registro
│       │       ├── frequency.py # Regra de frequência
│       │       ├── distance.py  # Regra de distância
│       │       └── offpeak.py   # Regra de horário off-peak
│       │
│       ├── junior_version.py    # Implementação JUNIOR (funcional mas difícil de manter)
│       └── mid_level_version.py # Implementação PLENO (organizada mas ainda viola Open/Closed)
│
├── tests/                       # Testes completos de todas as versões
└── examples/                    # Exemplos de uso
```

### ✅ O Que Já Foi Implementado

#### 1. **Versão Junior** (`junior_version.py`)
- ✅ Todas as regras funcionando
- ✅ Usa cálculos (não hardcoded)
- ❌ Função gigante com múltiplas responsabilidades
- ❌ Difícil de testar isoladamente
- ❌ Adicionar novo desconto = modificar código existente

#### 2. **Versão Pleno** (`mid_level_version.py`)
- ✅ Código organizado em classe
- ✅ Métodos separados por responsabilidade
- ✅ Usa dataclasses para modelagem
- ✅ Mais fácil de testar
- ⚠️ Ainda precisa modificar `calculate_final_price()` para novos descontos

#### 3. **Versão Senior** (`domain/`)
- ✅ **Totalmente aderente ao Open/Closed Principle**
- ✅ Auto-registro de regras (zero configuração)
- ✅ Cada regra é independente e testável
- ✅ Adicionar novo desconto = criar nova classe, **sem tocar em nada**
- ✅ Arquitetura limpa (Domain-Driven Design)
- ✅ Documentação completa com docstrings

---

## 🎯 Demonstração Prática: Adicionando Novo Desconto

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

---

## 📊 Comparação de Impacto: Dados Concretos

### Tabela Comparativa

| 📏 Métrica | 🟢 Junior | 🟡 Pleno | 🔵 Senior |
|------------|-----------|----------|-----------|
| **Linhas modificadas** para adicionar desconto | ~10-15 | ~5-8 | **0** ✨ |
| **Risco** de quebrar funcionalidade existente | 🔴 Alto | 🟡 Médio | 🟢 Zero |
| **Facilidade** para testar nova regra | 🔴 Difícil | 🟡 Médio | 🟢 Fácil |
| **Pode dar conflito** no Git? | ✅ Sim | ✅ Sim | ❌ Não |
| **Precisa de regressão** completa? | ✅ Sim | ✅ Sim | ❌ Não |
| **Usa valores hardcoded?** | ❌ Não* | ❌ Não | ❌ Não |
| **Tempo para adicionar** novo desconto | ~2-3h | ~1-2h | **~30min** |
| **Desenvolvedores podem trabalhar** em paralelo? | ❌ Não | ❌ Não | ✅ Sim |

*Junior usa cálculos mas ainda mistura tudo na mesma função

### 💰 Impacto no Negócio

#### Cenário: 5 desenvolvedores adicionando 10 novos descontos em 1 sprint

| Abordagem | Tempo Total | Conflitos Git | Bugs Introduzidos | ROI |
|-----------|-------------|---------------|-------------------|-----|
| Junior | ~150h | ~15 conflitos | ~8 bugs | 😰 Baixo |
| Pleno | ~75h | ~8 conflitos | ~3 bugs | 😐 Médio |
| Senior | **~25h** | **0 conflitos** | **0 bugs** | 🚀 **Alto** |

**Economia de tempo:** 83% (Junior → Senior) | 67% (Pleno → Senior)

---

## 💡 Lições Aprendidas

### 1. 🎯 Open/Closed não é sobre "nunca modificar código"
É sobre **estruturar seu código** de forma que novos requisitos sejam implementados através de **ADIÇÃO**, não **MODIFICAÇÃO**.

### 2. 🔑 Abstração é a chave
Classes abstratas e interfaces permitem que você defina **contratos** que novas implementações podem seguir sem quebrar o existente.

### 3. ⚡ Auto-registro é poderoso
O padrão usado no código senior (`__init_subclass__`) remove até a necessidade de registrar manualmente. **Zero configuração!**

### 4. ✨ Clean Code + SOLID = Excelência
Não basta seguir SOLID, o código deve ser limpo:
- ❌ Sem valores hardcoded
- ✅ Fórmulas e cálculos dinâmicos
- ✅ Código auto-documentado

### 5. 📈 Evolução natural
Não precisa começar com a solução mais complexa, mas **reconheça quando é hora de evoluir**:
- Junior → Pleno: Organize o código em responsabilidades
- Pleno → Senior: Aplique princípios SOLID para extensibilidade

---

## 🚀 Como Executar e Testar

### Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd o_solid

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências (se houver)
pip install -r requirements.txt
```

### Executando as Diferentes Versões

```bash
# 🟢 Versão Junior - Funcional mas difícil de manter
python src/ride_discount/junior_version.py

# 🟡 Versão Pleno - Organizada mas ainda viola Open/Closed
python src/ride_discount/mid_level_version.py

# 🔵 Versão Senior - Open/Closed Principle aplicado
python -m src.ride_discount.domain.calculator

# 🧪 Executar todos os testes
pytest tests/ -v

# 📊 Ver comparação lado a lado
python examples/compare_versions.py
```

### 📈 Resultado Esperado

Com os dados de exemplo (75 corridas, 25km, 14:30h em dia útil):

```
╔═══════════════════════════════════════════════════════════════╗
║                   CÁLCULO DE DESCONTO                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Cliente: Usuario Teste (75 corridas completadas)            ║
║  Distância: 25.0 km                                           ║
║  Horário: 14:30 (Terça-feira)                                 ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  DESCONTOS APLICADOS                                          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ✓ Frequência:  7.0%  (75 corridas ÷ 10)                     ║
║  ✓ Distância:  10.0%  ((25 - 5) × 0.5)                       ║
║  ✓ Off-Peak:   10.0%  (Meio-dia em dia útil)                 ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║  RESUMO FINANCEIRO                                            ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Preço Base:        $ 45.00                                   ║
║  Total Descontos:     27.0%                                   ║
║  Valor Descontado:  $ 12.15                                   ║
║                                                               ║
║  💰 PREÇO FINAL:    $ 32.85                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 🎬 Conclusão

O princípio **Open/Closed** não é apenas uma boa prática teórica - é uma **necessidade prática** em sistemas que evoluem.

### 🔍 Insight Principal

A diferença entre as implementações **não está na funcionalidade** (todas calculam o mesmo desconto), mas na:
- ✨ **Manutenibilidade:** Facilidade de manter o código ao longo do tempo
- 🚀 **Extensibilidade:** Capacidade de adicionar features sem quebrar o existente
- 🧪 **Testabilidade:** Facilidade de testar cada componente isoladamente
- 👥 **Colaboração:** Múltiplos devs trabalhando sem conflitos

### 📌 Pontos-Chave para Lembrar

| Aspecto | Realidade |
|---------|-----------|
| **Hoje** | 3 tipos de desconto |
| **Amanhã** | Podem ser 30+ tipos |
| **Preparação** | Economiza tempo e dinheiro |
| **Fórmulas** | Sempre > Valores Hardcoded |
| **Investimento** | Pensar no futuro desde o início |

### 🎯 Quando Aplicar Open/Closed?

✅ **Use quando:**
- O sistema tende a crescer com novas funcionalidades
- Múltiplos desenvolvedores trabalham no mesmo módulo
- Mudanças frequentes são esperadas
- Estabilidade é crítica

❌ **Não exagere quando:**
- Protótipos ou MVPs rápidos
- Código que dificilmente mudará
- Over-engineering prejudicaria a entrega

---

### 💬 Citação Final

> *"Um bom desenvolvedor resolve o problema de hoje.*
>
> *Um excelente desenvolvedor resolve o problema de hoje pensando no amanhã.*
>
> *Um desenvolvedor excepcional faz isso sem valores hardcoded e seguindo SOLID!"*

---

## 📚 Próximos Passos

Quer aprender mais sobre SOLID? Explore os outros princípios:

- **S** - Single Responsibility Principle
- **O** - Open/Closed Principle ← **Você está aqui!**
- **L** - Liskov Substitution Principle
- **I** - Interface Segregation Principle
- **D** - Dependency Inversion Principle

---

**📧 Feedback e Contribuições**

Encontrou algum problema ou tem sugestões? Abra uma issue ou pull request!

**⭐ Gostou?** Dê uma estrela no repositório e compartilhe com sua equipe!
