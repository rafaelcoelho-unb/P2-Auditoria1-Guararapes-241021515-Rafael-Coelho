# PT 530 – Amostragem de Auditoria
**Norma:** NBC TA 530 (versão aplicável ao exercício 2025, conferida na lista do CFC em 25/10/2026 – F08: Res. CFC 1.222/09) – itens 6–15. **Base:** exclusivamente a **base sintética [SI]**. Código: `codigo/03_amostragem_mus.py`; amostra: `resultados/PT530_amostra_selecionada.csv`; resultado: `resultados/PT530_resultado.json`.

## 1. Planejamento
| Item | Definição |
|---|---|
| Objetivo / afirmação | Valorização e existência do saldo líquido de contas a receber (R1) |
| População / unidade | 522.620 recebíveis; **unidade monetária** (R$ 1) do saldo bruto; valor contábil R$ 7.148.365,5 mil (inclui linhas com erro inserido) |
| Método | **MUS** (probabilidade proporcional ao valor), intervalo sistemático com partida aleatória (semente 241021515) |
| Erro tolerável (TM) | = PE = R$ 25.275 mil |
| Risco de aceitação incorreta | 5% (fator Poisson 3,0 para zero erros) |
| Erro esperado | 10% do TM; fator de expansão 1,6 |
| Intervalo | (25.275 − 0,10 × 25.275 × 1,6) / 3,0 = **R$ 7.077 mil** |
| Tamanho | 7.148.366 / 7.077 = 1.010,1 → **1.010 itens** |
| Estratificação | Itens ≥ intervalo seriam 100%: nenhum encontrado |

## 2. Execução
Para cada item selecionado, o valor líquido registrado foi comparado ao **valor correto do gabarito** (`verdade_terreno_valores_corretos.csv.gz`). Isso substitui, na simulação, a inspeção de documentos, que não é possível sem acesso interno. **[SI]**

## 3. Resultados
| Medida | R$ mil |
|---|---:|
| Itens com distorção | 17 de 1.010 |
| Distorção projetada (taint × intervalo) | 93.866,4 |
| Limite superior de distorção (Stringer, Poisson 95%) | 148.273,7 |
| Distorção real inserida (gabarito) | 66.534,4 |
| Erro tolerável | 25.275 |
| **Conclusão** | **Rejeitar:** limite superior > erro tolerável |

A projeção supera o valor real em 41%: é variabilidade amostral usual com poucas distorções de valores altos; o limite de Stringer é conservador. O limite inclui E07 (valores redondos altos).

## 4. Tratamento das distorções
Cada distorção é classificada (PT 450); causa (cut-off, duplicidade, estágio, provisão, baixa, lançamento manual) analisada; a projeção é aplicada ao restante da população; procedimentos adicionais seriam exigidos (ampliar a amostra ou testar 100% dos atributos de risco – feito pelos testes T-02 a T-08 → `resultados/comparacao_inseridos_x_identificados.csv`).

## 5. Comparação de erros inseridos × identificados (100% da base)
| Id | Teste | Inseridos | Identificados | Falsos positivos |
|---|---|---:|---:|---:|
| E05 | T-02 vencimento < origem | 400 | 400 | 0 |
| E01 | T-03 origem > 31/12/2025 | 1.100 | 1.100 | 0 |
| E04 | T-04 duplicidade de contrato | 660 | 660 | 660 (lado "original" dos pares) |
| E02 | T-05 estágio × dias de atraso | 2.500 | 2.500 | 0 |
| E03 | T-06 estágio 3 com provisão < 20% | 600 | 600 | 0 |
| E06 | T-07 atraso > 541 dias | 800 | 800 | 0 |
| E07 | T-08 manual, redondo, fim de semana | 60 | 60 | 0 |

## 6. Limitações
Resultados dependem do desenho da simulação (os erros e os testes foram construídos em conjunto → recall de 100% é esperado, não demonstra eficácia em dados reais). MUS testa superavaliação; subavaliação não coberta.

**Preparado por:** matrícula 241021515 – 25/10/2026 | **Revisão:** ________ (em branco; sem revisão simulada)
