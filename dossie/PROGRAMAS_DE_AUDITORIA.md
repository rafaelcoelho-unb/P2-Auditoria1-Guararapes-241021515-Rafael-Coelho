# Programas de Auditoria por Ciclo – Guararapes (exercício 2025)
Classificação: **[RP]** realizado com evidência pública · **[PL]** planejado por falta de acesso · **[SI]** simulado. Valores em R$ mil, consolidado (F01). PM 33.700 · PE 25.275 · trivial 1.685.

## PA-REC – Receitas (receita líquida 10.497.046)
**Riscos:** R2★ (fraude presumida), CO, R1 (receita de crédito). **Afirmações:** ocorrência, corte, acurácia, classificação.
| # | Procedimento | Estado |
|---|---|---|
| 1 | Conciliar receita bruta → líquida (NE 33: 13.948.204 − 3.451.158 = 10.497.046 ✓) e com segmentos (NE 6 ✓) | [RP] |
| 2 | Analíticos de receita, margem bruta (60,81% × 58,98%), devoluções (3,02% × 2,77%) e receita de crédito → PT 520 | [RP] |
| 3 | Revisar política de reconhecimento (CPC 47; loja física, e-commerce na entrega, juros pro rata, suspensão > 90 dias) | [RP] |
| 4 | Corte: 100% das vendas/recebíveis de dez/jan | [SI] (T-03) / [PL] real |
| 5 | Lançamentos manuais, fim de semana, valores redondos | [SI] (T-08) / [PL] real |
| 6 | Testar controles de faturamento, devoluções, descontos e campanhas; amostra de notas fiscais e recebimentos | [PL] |
| 7 | Receitas com seguros/assistências (212.659) – contratos com seguradoras | [PL] |
| 8 | Vendas intragrupo (2.041.380) – eliminação e preços de transferência | [RP] parcial (NE 32) / [PL] |

## PA-DIS – Disponibilidades e aplicações (caixa 1.415.443; aplicações 895.398)
| # | Procedimento | Estado |
|---|---|---|
| 1 | Conciliar caixa e aplicações: balanço × DFC × NE 10/12 (✓; caixa final DFC = 1.415.443) | [RP] |
| 2 | Confirmação com bancos e custodiantes (Selic); extratos e conciliações bancárias de 31/12 e itens em trânsito | [PL] (→ PT 505) |
| 3 | Recomputo de rendimentos e MTM (NE 12: juros/MTM 62.227; LFT valor justo nível 2 – ANBIMA) | [RP] parcial / [PL] |
| 4 | Classificação caixa × aplicações (vencimento ≤ 90 dias – NE 10, 12) e restrições | [PL] |
| 5 | Corte de recebimentos e pagamentos; análise de transferências incomuns (PAA de tesouraria) | [PL] |

## PA-EST – Estoques (1.609.563; provisão 143.085)
| # | Procedimento | Estado |
|---|---|---|
| 1 | Recomputo da movimentação da provisão e conciliação com DFC (PT 501) | [RP] |
| 2 | Observação de inventário (fábrica, 3 CDs, lojas), corte e importações em andamento (129.042) | [PL] |
| 3 | Teste de custo médio (matéria-prima, mão de obra, rateio), capacidade ociosa (11.247) | [PL] |
| 4 | VRL e obsolescência: giro, margens, vendas posteriores | [PL] / [RP] analítico |
| 5 | Lucros não realizados em estoques (42.524) | [RP] valor / [PL] cálculo |

## PA-IMO – Imobilizado, direito de uso e intangível (1.473.044 / 943.833 / 970.240)
| # | Procedimento | Estado |
|---|---|---|
| 1 | Roll-forward: saldo inicial + adições − baixas − depreciação (NE 17: 1.406.227 + 249.085 + 17.129 − 10.294 − 189.103 = **1.473.044** ✓) | [RP] |
| 2 | Teste de adições (249.085) e capitalizações do intangível (322.746; projetos de tecnologia) – documentos, aprovações | [PL] |
| 3 | Recomputo de depreciação e vida útil (NE 17); depreciação DFC 491.475 × NE | [RP] parcial |
| 4 | Impairment por loja (UGC), indicadores e premissas; nenhuma perda reconhecida | [PL] |
| 5 | Arrendamentos: recálculo amostral de contratos, taxas, prazos; confronto com Ofício-Circular CVM (passivo +162.175 pela metodologia CVM) | [PL] / [RP] leitura |
| 6 | Ativos mantidos para venda (17.234) e baixas (Midway Mall) | [RP] / [PL] |

## PA-PAS – Passivos (fornecedores, dívida, impostos, provisões)
| # | Procedimento | Estado |
|---|---|---|
| 1 | Fornecedores (1.206.661): completude (pagamentos posteriores, notas não registradas), estrangeiros e câmbio (330.422), antecipação (58.352) | [PL] |
| 2 | Dívida: conciliar saldos NE 21/22 ao balanço ✓; confirmar termos, covenants (0,1 × 3,0), classificação; GUAR17 (1.450.000) | [RP] / [PL] |
| 3 | Obrigações com administradoras (2.718.238) – conciliação de liquidação | [PL] |
| 4 | Impostos (613.922) – conciliar IR/CS a pagar (329.862) com NE 29b | [RP] parcial |
| 5 | Provisões e contingências (217.721; possível 1.199.097) → PT 501/250 | [RP]/[PL] |
| 6 | Obrigações trabalhistas (433.563): recomputo de PLR e férias | [PL] |

## PA-EST-CONT – Estimativas
| Estimativa | Saldo | Procedimentos | Estado |
|---|---:|---|---|
| **ECL** | 1.587.015 | Sensibilidade (PT 540); base sintética T-05/T-06/MUS; reperformance do modelo; retrospectiva | [RP]/[SI]/[PL] |
| **IR/CS diferido ativo** | 1.148.797 líquido | Projeção de lucro tributável 6–8 anos; consumo 158.253; novo crédito 97.966 | [PL] |
| **Impairment** | – | Premissas por UGC | [PL] |
| **Perdas em estoques** | 143.085 | Recomputo e giro | [RP]/[PL] |
| **Provisões judiciais** | 217.721 | Prognóstico e jurisprudência | [PL] |
| **Arrendamentos** | 1.069.523 | Taxa/prazo | [PL] |

**Preparado por:** matrícula 241021515 – 25/10/2026 | **Revisão:** ________ (em branco; sem revisão simulada)
