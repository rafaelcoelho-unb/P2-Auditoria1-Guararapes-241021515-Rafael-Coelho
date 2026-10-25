# PT 510 – Trabalho Inicial de Auditoria – Saldos Iniciais
**Norma:** NBC TA 510 (R1) (versão aplicável ao exercício 2025, conferida na lista do CFC em 25/10/2026 – F08: DOU 05/09/16) – itens 6–9. **Premissa didática:** o trabalho é tratado como **auditoria inicial** (o aluno não auditou 2024). **Fontes:** F04 – DFP 2024 completa (PDF fornecido em 25/10/2026; 116 págs.; rodapé 'de 108') e comparativos de 2024 da DFP 2025 (F01) [RP]. Comparação automatizada: `codigo/07_comparar_dfp2024_2025.py` → `resultados/comparativos_DFP2024_vs_DFP2025.csv`.

## 1. Saldos de abertura × demonstrações originalmente publicadas
| Teste | Resultado |
|---|---|
| Colunas de 2024 da DFP 2025 × DFP 2024 original, **consolidado**: balanço (79 contas), DRE (25) e DFC (53) | **0 divergências** em 157 linhas ✓ [RP] |
| Totais-chave 2024: ativo 13.633.267; clientes 5.111.727; estoques 1.461.441; caixa 1.158.206; IR/CS diferido ativo 1.157.516; PL 5.403.620; lucro 235.138 | Iguais nas duas DFPs ✓ |
| Caixa inicial 2025 (1.158.206) = caixa final 2024; investimentos 5.244.677; roll-forwards 2025 iniciam nos saldos de 2024 (ECL 1.006.059; empréstimos 1.079.033; debêntures 891.963; arrendamento 1.077.072; provisões 141.919) | ✓ |
| Carteira Midway 2024: total 5.718.394 e ECL 1.005.287 (DFP 2024, NE 12e) = soma dos estágios comparativos da DFP 2025 | ✓ nos totais |
Conclusão do teste: **os saldos de abertura de 2025 correspondem aos saldos finais auditados de 2024**, sem reapresentação de valores.

## 2. Auditor e opinião do exercício anterior [RP]
- **PwC Auditores Independentes Ltda. (CRC 2SP000160/O-5), mesmo sócio responsável (Daniel Vinícius Fumo, CRC 1SP256197/O-9)** nos relatórios de 2024 (**19/03/2025**) e 2025 (11/02/2026). Em termos reais, não há troca de auditor: a continuidade reduz o risco de saldos iniciais, mas, no exercício didático, o aluno não tem acesso aos papéis.
- **Opinião de 2024: sem ressalva**; sem parágrafo de ênfase; 'Outros assuntos': DVA como informação suplementar (DFP 2024, p.99–104 do rodapé).
- **PAAs de 2024 (os mesmos cinco de 2025):** ECL (R$ 1.006.059 mil), IR/CS diferido (R$ 1.157.516 mil), conciliações e processos de tesouraria, controles gerais de TI e arrendamentos (direito de uso 964.849; passivo 1.077.072).
- **Deficiência recorrente:** em 2024 o auditor já identificava **deficiências de controle sobre acesso a programas e dados** e informava que sua abordagem planejada **não depositava confiança no ambiente de controles**; o relatório de 2025 repete a deficiência, mas **não repete essa frase** sobre a abordagem. Observação **[hipótese]**: verificar com o auditor se houve mudança de abordagem [PL].

## 3. Políticas contábeis e consistência entre exercícios
| Tema | 2024 (original) | 2025 | Efeito |
|---|---|---|---|
| Baixa de recebíveis vencidos | Carteira medida 'até 360 dias' (Rel. Adm. 2024: carteira R$ 5.718 mil… 'até 360 dias') | **Baixa só acima de 541 dias** (NE 13d) | Nova faixa 361–540 (511.753); baixas −72%; carteira bruta e provisão maiores com efeito líquido possivelmente neutro; **comparabilidade reduzida** |
| Divulgação de qualidade de crédito | Níveis **A–H (categorias do BACEN)**; provisão por nível: A–B 46.899; total 1.005.287; cobertura total 17,58% | **Estágios 1–3 (IFRS 9/CPC 48)**; comparativo 2024 re-apresentado: estágio 1 = 301.050 | Mesmo total, **alocação por faixa não reconciliável** (diferença de 254.151 entre 'A+B' e 'estágio 1') |
| Aging | Última faixa: 'vencidos acima de 180 dias' (457.619) | Reapresentada como '181 a 360' (457.619) e nova faixa 361–540 | Valores iguais; rótulo alterado |
| Normas novas (NE 3.9.1) | – | IAS 21/CPC 02 (conversibilidade), sem impacto | Imaterial |
**Indicadores de gestão estáveis:** inadimplência > 90 dias 17,3% (2024) × 17,2% (2025, mesma base) e PDD líquida/carteira 5,3% × 5,3% – consistentes com a nova política na base comparável.

## 4. Procedimentos planejados [PL]
Ler papéis do auditor predecessor (continuidade da PwC); retrospectiva da ECL 2024 (R$ 1.006.059) × baixas e recuperações de 2025; entender a base da mudança de nível A–H para estágios (norma adotada, data, efeito) e da política de 541 dias; testes de corte e de estoques iniciais; confirmar a ausência de ajustes de saldos iniciais.

## 5. Conclusão e limitações
**Saldos iniciais coerentes** com as demonstrações auditadas de 2024 (opinião sem ressalva, sem reapresentação). Persistem **mudanças de política e de apresentação** que afetam a comparabilidade da carteira de crédito (PT 540). Não houve acesso aos papéis do auditor anterior.
**Preparado por:** matrícula 241021515 – 25/10/2026 | **Revisão:** ________ (em branco; sem revisão simulada)
