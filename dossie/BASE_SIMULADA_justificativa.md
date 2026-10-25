# Base de dados simulada – Contas a receber de clientes (SINTÉTICA)

**Preparado por:** matrícula 241021515 | **Data:** 25/10/2026 | **Revisão:** ________ (em branco)

> **Aviso.** Todos os registros desta base são **SINTÉTICOS** (`fonte = SINTETICO`). Nenhuma linha representa cliente, contrato ou saldo real da Guararapes. Somente os **totais de calibração** vêm das Notas Explicativas 2025 (dados reais, R$ mil).

## 1. Justificativa da conta e da materialidade
Ativo consolidado 31/12/2025 (NE 6): **R$ 14.872.670 mil**. Maiores contas do ativo (NE 4.1, 10, 12, 13, 14, 15, 17, 18, 23, 29):

| Conta (consolidado) | R$ mil | % do ativo |
|---|---:|---:|
| **Contas a receber de clientes, líquido (NE 13)** | **5.478.486** | **36,8%** |
| Estoques (NE 14) | 1.609.563 | 10,8% |
| Imobilizado (NE 17) | 1.473.044 | 9,9% |
| Caixa e equivalentes (NE 10) | 1.415.443 | 9,5% |
| IR/CS diferidos ativos (NE 29) | 1.221.968 | 8,2% |
| Intangível (NE 18) | 970.240 | 6,5% |
| Direito de uso (NE 23) | 943.833 | 6,3% |

A conta escolhida é a de maior materialidade e também a de maior risco: carteira bruta de R$ 7.065.501 mil, perdas esperadas de R$ 1.587.015 mil (22,5% do bruto), estimativa classificada pela própria administração como crítica (NE 3.10 e NE 13) e variações relevantes no ano (vencidos +120%, baixas −72%).

## 2. Premissas e método de geração (`codigo/01_gerar_base.py`, semente = 241021515)
- **P1.** Os dois ajustes negativos da NE 13(a) (−34.104 e −4.368) são linhas `AJUSTE` alocadas à faixa "a vencer".
- **P2.** As NE 13(d) (aging) e 13(g) (estágios) só fecham simultaneamente se parte do estágio 3 tiver atraso ≤ 90 dias (renegociados/período de cura): R$ 132.978 mil. A base modela esse grupo com `flag_renegociado = 1`.
- **P3.** Apenas a carteira da Midway Financeira (cartão Riachuelo e crédito pessoal) tem atraso; terceiros, FIDC e outros estão "a vencer".
- **P4.** Cada linha é uma **conta/contrato sintético**: 520.002 linhas representam uma carteira que, na realidade, tem número de contas não divulgado. Ticket médio por linha ≈ R$ 13,6 mil. O fator de escala **não é verificável** com fontes públicas.
- **P5.** Valores por linha seguem distribuição lognormal; contagem de linhas proporcional ao valor por célula; provisão proporcional a uma taxa relativa por faixa, reescalada para fechar a NE 13(g) por estágio.
- Total: **522.622 linhas** (520.002 da base legítima + 2.620 inseridas pelos testes). Arquivo: `dados/base_contas_receber_sintetica.csv.gz` (~22 MB). SHA-256 do CSV descomprimido: `ed6b2fb119b136d104b30983f92ac9a5d6f232469f6ba87bac4d8dfbed296b5f` (Python 3.12.3, numpy 2.4.4, pandas 3.0.2).
- Dicionário de variáveis: `dados/dicionario_variaveis.csv`.

## 3. Erros inseridos (gabarito: `dados/registro_erros_inseridos.csv`)
| Id | Natureza | Linhas | Distorção líquida (R$ mil) |
|---|---|---:|---:|
| E01 | Corte: recebíveis de jan/2026 no saldo de dez/2025 | 1.100 | 14.800,0 |
| E02 | Estágio 3 (91–360 dias) classificado como estágio 1, provisão ~4,5% | 2.500 | 25.667,3 |
| E03 | Estágio 3 > 180 dias sem provisão | 600 | 7.195,9 |
| E04 | Duplicidade de contrato | 660 | 9.131,2 |
| E05 | Vencimento anterior à origem (qualidade de dados) | 400 | 0,0 |
| E06 | Título > 541 dias não baixado (política da NE 13) | 800 | 540,0 (bruto 10.800) |
| E07 | Lançamento manual, valor redondo, fim de semana de fim de período | 60 | 9.200,0 |
| | **Total** | **6.120** | **66.534,4** |

A "distorção correta" de E02/E03 usa a cobertura média do estágio 3 (75,28%) como referência; é uma escolha do cenário.

## 4. Conciliação com a NE 13 (R$ mil) – `resultados/T01_conciliacao_NE13.csv`
| Item | NE 13 (real) | Base sintética | Diferença |
|---|---:|---:|---:|
| Saldo bruto | 7.065.501 | 7.109.893,6 | +44.392,6 |
| Provisão (ECL) | 1.587.015 | 1.565.037,6 | −21.977,4 |
| Saldo líquido | 5.478.486 | 5.544.855,9 | +66.369,9 |

- A diferença **bruta** é integralmente explicada pelas linhas inseridas (E01+E04+E06+E07 = 44.392,6).
- A diferença de **provisão** resulta de +10.260 de provisão sobre E06 e da redução de provisão em E02/E03.
- O líquido difere do gabarito (66.534,4) em 164,5 (0,25%) porque a provisão "correta" de E02/E03 usa a taxa média do estágio 3 e não a taxa original de cada linha. Sem os erros, a base fecha com a NE 13 (por produto, aging e estágio) por construção.

## 5. Procedimentos executados com a base (todos **[SI]**)
Testes T-02 a T-08 (`02_testes_auditoria.py`), analíticos T-09 e amostragem MUS (`03_amostragem_mus.py`) → PT 450, 520, 530 e 240. **Resultado:** os 7 testes identificaram 100% das linhas inseridas, com 660 "falsos positivos" apenas no T-04 (o teste sinaliza os dois lados de cada par duplicado; o original não é distinguível do duplicado).

## 6. Limitações
A base não valida o saldo real; a estrutura interna da carteira é hipótese; a identificação de 100% dos erros é esperada porque os testes foram desenhados para as regras inseridas (circularidade do exercício didático).
