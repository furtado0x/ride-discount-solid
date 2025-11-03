# Arquitetura do Projeto - Clean Architecture

Este documento descreve a arquitetura do sistema de descontos de corridas após a refatoração para Clean Architecture.

## 📁 Estrutura do Projeto

```
o_solid/
├── src/
│   └── ride_discount/              # Pacote principal
│       ├── domain/                 # Camada de Domínio
│       │   ├── entities.py         # Entidades de domínio (Customer)
│       │   ├── value_objects.py    # Value Objects (DiscountResult)
│       │   └── rules/              # Regras de negócio
│       │       ├── base.py         # ABC + Auto-registro
│       │       ├── frequency.py    # Regra de frequência
│       │       ├── distance.py     # Regra de distância
│       │       └── offpeak.py      # Regra de horários
│       ├── application/            # Camada de Aplicação
│       │   ├── dtos.py             # DTOs (RideContext)
│       │   └── use_cases/          # Casos de uso
│       │       └── calculate_ride_discount.py
│       └── protocols.py            # Protocols para type hints
├── tests/                          # Testes (espelham a estrutura)
│   ├── conftest.py                 # Fixtures compartilhadas
│   ├── domain/
│   └── application/
├── examples/                       # Versões antigas (comparação)
│   ├── 1_junior_version.py
│   ├── 2_mid_level_version.py
│   └── 3_senior_version.py
├── demo.py                         # Script de demonstração
├── pyproject.toml                  # Configuração moderna
└── README.md                       # Documentação original
```

## 🏗️ Camadas da Clean Architecture

### 1. Domain Layer (Camada de Domínio)

**Responsabilidade:** Regras de negócio puras, sem dependências externas.

#### Entities (`entities.py`)
- `Customer`: Entidade de domínio representando um cliente
- Características:
  - Imutável (`frozen=True`)
  - Validação de invariantes no `__post_init__`
  - Não depende de nenhuma outra camada

#### Value Objects (`value_objects.py`)
- `DiscountResult`: Objeto de valor representando um desconto
- Características:
  - Imutável (`frozen=True`)
  - Sem identidade própria
  - Validação de regras de negócio (0-100%)

#### Domain Rules (`rules/`)
- `DiscountRule` (ABC): Interface base com auto-registro
- Implementações:
  - `RideFrequencyDiscountRule`: 1% por 10 corridas, máx 15%
  - `ProportionalDistanceDiscountRule`: 0.5% por km acima de 5km, máx 20%
  - `OffPeakDiscountRule`: 20% (noite) ou 10% (meio-dia útil)

**Padrões aplicados:**
- Strategy Pattern (cada regra é uma estratégia)
- Open/Closed Principle (adicione novas regras sem modificar código existente)
- Single Responsibility (uma regra = uma classe)

### 2. Application Layer (Camada de Aplicação)

**Responsabilidade:** Orquestração de casos de uso e coordenação do domínio.

#### DTOs (`dtos.py`)
- `RideContext`: DTO de entrada contendo todas as informações da corrida
- Características:
  - Imutável (`frozen=True`)
  - Validação básica de dados
  - Separa formato de entrada da lógica de domínio

#### Use Cases (`use_cases/`)
- `CalculateRideDiscountUseCase`: Orquestra o cálculo de descontos
- Responsabilidades:
  - Iterar sobre todas as regras registradas
  - Aplicar cap de 50% no desconto total
  - Calcular preço final
  - Retornar resultado estruturado

### 3. Infrastructure Layer (Não implementada)

Neste projeto educacional, não há camada de infraestrutura pois:
- Sem persistência (banco de dados)
- Sem APIs externas
- Sem frameworks web
- Foco em lógica de negócio pura

**Extensões futuras:**
- `infrastructure/repositories/`: Repositórios para persistência
- `infrastructure/adapters/`: Adaptadores para APIs externas

### 4. Presentation Layer (Não implementada)

Não há camada de apresentação, mas poderia incluir:
- `presentation/cli/`: Interface de linha de comando
- `presentation/api/`: REST API (FastAPI, Flask)
- `presentation/web/`: Interface web

## 🎯 Princípios SOLID Aplicados

### Single Responsibility Principle (SRP)
- Cada classe tem uma única responsabilidade
- `Customer` apenas representa dados do cliente
- Cada regra calcula apenas um tipo de desconto
- Use case apenas orquestra o fluxo

### Open/Closed Principle (OCP) ⭐
- **Principal foco do projeto**
- Adicionar nova regra = criar nova classe
- Sistema fechado para modificação, aberto para extensão
- Auto-registro automático via `__init_subclass__`

### Liskov Substitution Principle (LSP)
- Todas as regras implementam `DiscountRule`
- Podem ser substituídas sem quebrar o sistema
- Interface consistente: `calculate_discount(context) -> DiscountResult | None`

### Interface Segregation Principle (ISP)
- Interfaces pequenas e focadas
- `DiscountRule` tem apenas um método
- DTOs não expõem métodos desnecessários

### Dependency Inversion Principle (DIP)
- Domínio não depende de aplicação
- Uso de `TYPE_CHECKING` para evitar imports circulares
- Inversão de controle via abstrações (`DiscountRule`)

## 🧪 Estratégia de Testes

### Estrutura de Testes
```
tests/
├── conftest.py           # Fixtures reutilizáveis
├── domain/               # Testes unitários puros
│   ├── test_entities.py
│   ├── test_value_objects.py
│   └── test_rules/       # Cada regra isolada
└── application/          # Testes de integração
    ├── test_dtos.py
    └── test_use_cases/
```

### Fixtures (`conftest.py`)
- Customers variados (0, 25, 75, 150 rides)
- Distâncias variadas (curta, média, longa)
- Horários variados (rush hour, meio-dia, noite)
- Contexts pré-configurados

### Parametrização
- `@pytest.mark.parametrize` para testar múltiplos cenários
- Boundary testing (valores limite)
- Edge cases (0 rides, 1000 rides, etc)

### Cobertura
- **95%** de cobertura de código
- 94 testes passando
- Testes de domínio: 100% isolados
- Testes de aplicação: integração entre regras

## 🔧 Ferramentas e Configuração

### Type Checking (mypy)
- Modo strict habilitado
- Type hints completos em todas as funções
- Protocols para structural typing
- Compatibilidade com Python 3.10+

### Linting (ruff)
- Substituição moderna do flake8, isort, etc
- Regras: pycodestyle, pyflakes, pyupgrade, bugbear
- Auto-fix habilitado
- Import sorting automático

### Testing (pytest)
- Coverage report (HTML + terminal)
- Fixtures reutilizáveis
- Parametrização para DRY
- Branch coverage habilitado

## 📊 Comparação com Versões Anteriores

| Aspecto | Junior | Mid-Level | Senior (Clean Arch) |
|---------|--------|-----------|---------------------|
| **Arquitetura** | Procedural | OOP básico | Clean Architecture |
| **Separação** | Nenhuma | Classes | Camadas (domain/app) |
| **Testabilidade** | Baixa | Média | Alta |
| **Extensibilidade** | Modificação | Modificação | Extensão |
| **Type hints** | Alguns | Completos | Completos + Protocols |
| **Imutabilidade** | Não | Parcial | Total (`frozen=True`) |
| **Validação** | Runtime | Runtime | Design time + Runtime |
| **Linhas de código** | ~60 | ~90 | ~300 (com testes: ~800) |

## 🚀 Como Usar

### Executar testes
```bash
PYTHONPATH=src pytest tests/ -v --cov
```

### Type checking
```bash
mypy --explicit-package-bases src/ride_discount
```

### Linting
```bash
ruff check src/ tests/
```

### Demo
```bash
python3 demo.py
```

### Adicionar nova regra de desconto

1. Crie um novo arquivo em `src/ride_discount/domain/rules/`
2. Implemente a classe herdando de `DiscountRule`
3. Importe no `__init__.py` para ativar auto-registro
4. Pronto! Sem modificar código existente

**Exemplo:**
```python
# src/ride_discount/domain/rules/weekend.py
from decimal import Decimal
from ride_discount.application.dtos import RideContext
from ride_discount.domain.rules.base import DiscountRule
from ride_discount.domain.value_objects import DiscountResult

class WeekendDiscountRule(DiscountRule):
    def calculate_discount(self, context: RideContext) -> DiscountResult | None:
        if context.ride_datetime.weekday() >= 5:
            return DiscountResult(
                discount_percentage=Decimal("15"),
                reason="Weekend special discount"
            )
        return None
```

## 📚 Referências

- Clean Architecture (Robert C. Martin)
- SOLID Principles
- Domain-Driven Design (DDD)
- Python Type Hints (PEP 484, 544)
- Strategy Pattern (Gang of Four)
