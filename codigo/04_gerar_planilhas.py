"""Planilhas editáveis com FÓRMULAS (materialidade, sensibilidade ECL, analíticos, conciliação, MUS). Dados reais: NE 2025."""
import os, json, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from config import *
R = os.path.join(os.path.dirname(__file__), "..", "resultados"); P = os.path.join(os.path.dirname(__file__), "..", "planilhas"); os.makedirs(P, exist_ok=True)
wb = Workbook(); H = Font(bold=True, color="FFFFFF"); F = PatternFill("solid", fgColor="1F3864"); IN = PatternFill("solid", fgColor="FFF2CC")
def cab(ws, row, vals):
    for i, v in enumerate(vals, 1): c = ws.cell(row, i, v); c.font = H; c.fill = F; c.alignment = Alignment(wrap_text=True)
def larg(ws, w): [ws.column_dimensions.__getitem__(chr(65 + i)).__setattr__("width", x) for i, x in enumerate(w)]
# ---- Materialidade (PT 320) ----
ws = wb.active; ws.title = "PT320_Materialidade"
ws["A1"] = "PT 320 – Materialidade (R$ mil) – amarelo = entrada (NE 2025 / julgamento do aluno)"; ws["A1"].font = Font(bold=True)
d = [("Lucro antes do IR/CS 2025 consolidado (NE 6(b))", LAIR_2025), ("(-) Ganho líquido na venda do Midway Mall, antes dos tributos (NE 5.3)", GANHO_MIDWAY_MALL)]
for i, (k, v) in enumerate(d, 3): ws.cell(i, 1, k); c = ws.cell(i, 2, v); c.fill = IN
ws["A5"] = "LAIR normalizado (não recorrente excluído)"; ws["B5"] = "=B3-B4"
ws["A7"] = "Benchmark"; ws["B7"] = "Base"; ws["C7"] = "%"; ws["D7"] = "Resultado"; cab(ws, 7, ["Benchmark", "Base (R$ mil)", "%", "Resultado (R$ mil)"])
bm = [("LAIR normalizado (ESCOLHIDO)", "=B5", .05), ("LAIR reportado (referência)", "=B3", .05), ("Receita líquida 2025 (NE 6)", 10_497_046, .005), ("Ativo total 2025 (NE 6)", 14_872_670, .005), ("LAIR 2024 (NE 6)", 361_945, .05)]
for i, (k, b_, p) in enumerate(bm, 8):
    ws.cell(i, 1, k); ws.cell(i, 2, b_); c = ws.cell(i, 3, p); c.fill = IN; c.number_format = "0.0%"; ws.cell(i, 4, f"=B{i}*C{i}")
ws["A14"] = "Materialidade global (PM) – arredondada a R$ 100 mil"; ws["B14"] = "=ROUND(D8,-2)"
ws["A15"] = "% de execução"; ws["B15"] = .75; ws["B15"].fill = IN; ws["B15"].number_format = "0%"
ws["A16"] = "Materialidade para execução (PE)"; ws["B16"] = "=B14*B15"
ws["A17"] = "% limite de acumulação de distorções claramente triviais"; ws["B17"] = .05; ws["B17"].fill = IN; ws["B17"].number_format = "0%"
ws["A18"] = "Limite de distorções claramente triviais"; ws["B18"] = "=B14*B17"
ws["A20"] = "PM como % do LAIR reportado"; ws["B20"] = "=B14/B3"; ws["B20"].number_format = "0.00%"
ws["A21"] = "PM como % da receita líquida"; ws["B21"] = "=B14/B10"; ws["B21"].number_format = "0.00%"
ws["A22"] = "PM como % do saldo líquido de contas a receber (5.478.486)"; ws["B22"] = "=B14/5478486"; ws["B22"].number_format = "0.00%"
larg(ws, [62, 18, 10, 20])
# ---- Sensibilidade ECL (PT 540) ----
s = wb.create_sheet("PT540_Sensibilidade_ECL"); s["A1"] = "PT 540 – Sensibilidade da estimativa de perdas esperadas (NE 13(g)) – R$ mil"; s["A1"].font = Font(bold=True)
cab(s, 3, ["Estágio", "Bruto 31/12/25", "Provisão 31/12/25", "Cobertura 2025", "Bruto 31/12/24", "Provisão 31/12/24", "Cobertura 2024", "Δ cobertura (pp)"])
est = [(1, 4_679_473, 209_602, 4_600_923, 301_050), (2, 179_402, 53_537, 236_887, 59_247), (3, 1_757_287, 1_322_917, 880_584, 644_990)]
for i, (e, b1, p1, b0, p0) in enumerate(est, 4):
    s.cell(i, 1, e); s.cell(i, 2, b1); s.cell(i, 3, p1); s.cell(i, 4, f"=C{i}/B{i}"); s.cell(i, 5, b0); s.cell(i, 6, p0); s.cell(i, 7, f"=F{i}/E{i}"); s.cell(i, 8, f"=(D{i}-G{i})*100")
    for col in "DG": s[f"{col}{i}"].number_format = "0.00%"
s["A7"] = "Total"; s["B7"] = "=SUM(B4:B6)"; s["C7"] = "=SUM(C4:C6)"; s["D7"] = "=C7/B7"; s["E7"] = "=SUM(E4:E6)"; s["F7"] = "=SUM(F4:F6)"; s["G7"] = "=F7/E7"; s["D7"].number_format = s["G7"].number_format = "0.00%"
s["A9"] = "Cenários (efeito na provisão = bruto × Δ cobertura; positivo = provisão adicional)"; s["A9"].font = Font(bold=True)
cab(s, 10, ["Cenário", "Δ cobertura aplicada", "Efeito (R$ mil)", "Efeito / PM", "Efeito / PE"])
cen = [("Estágio 1 volta à cobertura do comparativo 2024 (re-apresentado na DFP 2025; não comparável com níveis A–H originais)", "=G4-D4", "B4"), ("Estágio 3 -5 pp de cobertura", -.05, "B6"), ("Estágio 3 +5 pp de cobertura", .05, "B6"), ("Estágio 2 -5 pp de cobertura", -.05, "B5"), ("Estágio 2 +5 pp", .05, "B5")]
for i, (k, dlt, base) in enumerate(cen, 11):
    s.cell(i, 1, k); c = s.cell(i, 2, dlt); c.number_format = "0.00%"; c.fill = IN; s.cell(i, 3, f"=B{i}*{base}".replace("B%d*" % i, "B%d*" % i) if False else f"=B{i}*{base}"); s.cell(i, 4, f"=C{i}/PT320_Materialidade!$B$14"); s.cell(i, 5, f"=C{i}/PT320_Materialidade!$B$16"); s.cell(i, 4).number_format = s.cell(i, 5).number_format = '0.0"x"'
s["A16"] = "Cobertura TOTAL da Midway ±1 pp (não depende da alocação por estágio)"; s["B16"] = 0.01; s["B16"].number_format = "0.00%"; s["B16"].fill = IN; s["C16"] = "=B16*B7"; s["D16"] = "=C16/PT320_Materialidade!$B$14"; s["E16"] = "=C16/PT320_Materialidade!$B$16"; s["D16"].number_format = s["E16"].number_format = '0.0"x"'
s["A18"] = "Cobertura total Midway: 2024 original (DFP 2024) 17,58% = 1.005.287/5.718.394; 2025 = 23,97% = 1.586.056/6.616.161"
s["A17"] = "Combinado: E1 volta a 2024 + E3 -2 pp"; s["C17"] = "=C11+(-0.02*B6)"; s["D17"] = "=C17/PT320_Materialidade!$B$14"; s["D17"].number_format = '0.0"x"'
larg(s, [48, 18, 18, 14, 16, 18, 14, 16])
# ---- Analíticos (PT 520) ----
a = wb.create_sheet("PT520_Analiticos"); a["A1"] = "PT 520 – Procedimentos analíticos substantivos (dados REAIS das NE 2025, R$ mil)"; a["A1"].font = Font(bold=True)
cab(a, 3, ["Indicador", "2025", "2024", "Variação %", "Expectativa 2025", "Diferença", "Limite de investigação (PE)", "Investigar?"])
an = [("Receita de operações de crédito (NE 33)", 2_454_777, 2_238_120, "=C4*(1+(B5/C5-1))"), ("Carteira Midway: cartão + crédito pessoal (NE 13a)", 6_616_161, 5_718_038, None),
      ("Contas a receber bruto (NE 13a)", 7_065_501, 6_117_786, None), ("Saldo vencido (NE 13d)", 1_970_663, 895_053, None), ("Provisão para perdas (ECL) (NE 13f)", 1_587_015, 1_006_059, None),
      ("Baixas para perda no ano (NE 13f)", 272_324, 971_639, None), ("Despesa ECL (NE 34.2)", 845_004, 794_613, None), ("Estoques – provisão para perdas (NE 14b)", 143_085, 86_035, None),
      ("Receita líquida (NE 33)", 10_497_046, 9_634_207, None), ("Custo dos produtos/mercad. e serviços (NE 34.1)", 4_114_271, 3_952_420, None)]
for i, (k, v5, v4, ex) in enumerate(an, 4):
    a.cell(i, 1, k); a.cell(i, 2, v5); a.cell(i, 3, v4); a.cell(i, 4, f"=B{i}/C{i}-1").number_format = "0.0%"
a["E4"] = "=C4*(B5/C5)"; a["F4"] = "=B4-E4"; a["G4"] = "=PT320_Materialidade!$B$16"; a["H4"] = '=IF(ABS(F4)>G4,"SIM","NÃO")'
a["A15"] = "Razões"; a["A15"].font = Font(bold=True)
cab(a, 16, ["Razão", "2025", "2024", "Δ (pp)"])
rz = [("ECL / carteira bruta", "=B8/B6", "=C8/C6"), ("Vencido / carteira bruta", "=B7/B6", "=C7/C6"), ("Baixas / ECL inicial", "=B9/C8", None), ("Provisão estoques / estoques bruto (NE 14: 143.085 / 1.752.648; 86.035 / 1.547.476)", "=143085/(1609563+143085)", "=86035/(1461441+86035)"), ("Margem bruta (consolidada)", "=(B12-B13)/B12", "=(C12-C13)/C12")]
for i, (k, f5, f4) in enumerate(rz, 17):
    a.cell(i, 1, k); a.cell(i, 2, f5).number_format = "0.00%"
    if f4: a.cell(i, 3, f4).number_format = "0.00%"; a.cell(i, 4, f"=(B{i}-C{i})*100").number_format = "0.00"
a["A23"] = "Expectativa da receita de crédito = receita 2024 × crescimento da carteira Midway (fim de ano). Limite de investigação = PE."; a["A24"] = "Reconciliação EBITDA (NE 4.2): lucro + IR/CS + resultado financeiro + D&A"; a["B24"] = "=1475168+403819+496741+758497"; a["C24"] = 3_134_225; a["D24"] = "=B24-C24"
larg(a, [70, 16, 16, 14, 18, 14, 22, 14])
# ---- Conciliação, erros, MUS ----
rc = pd.read_csv(os.path.join(R, "T01_conciliacao_NE13.csv")); c = wb.create_sheet("PT500_Conciliacao_NE13"); cab(c, 1, list(rc.columns))
for i, r in enumerate(rc.itertuples(index=False), 2):
    for j, v in enumerate(r, 1): c.cell(i, j, v)
    c.cell(i, 5, f"=D{i}-C{i}")
larg(c, [14, 30, 18, 20, 16])
cp = pd.read_csv(os.path.join(R, "comparacao_inseridos_x_identificados.csv")); e = wb.create_sheet("PT450_Erros_x_Testes"); cab(e, 1, list(cp.columns))
for i, r in enumerate(cp.itertuples(index=False), 2):
    for j, v in enumerate(r, 1): e.cell(i, j, v)
n = len(cp) + 2; e.cell(n, 1, "TOTAL"); e.cell(n, 3, f"=SUM(C2:C{n-1})"); e.cell(n, 5, f"=SUM(E2:E{n-1})"); e.cell(n, 8, f"=SUM(H2:H{n-1})")
e.cell(n + 1, 1, "Distorção líquida total / PM"); e.cell(n + 1, 8, f"=H{n}/PT320_Materialidade!B14"); larg(e, [10, 34, 12, 14, 14, 12, 16, 26])
m = json.load(open(os.path.join(R, "PT530_resultado.json"))); u = wb.create_sheet("PT530_MUS"); u["A1"] = "PT 530 – Amostragem por Unidade Monetária (base SINTÉTICA)"; u["A1"].font = Font(bold=True)
par = [("Valor contábil da população (R$ mil)", m["valor_contabil_R$mil"]), ("Erro tolerável = PE (R$ mil)", "=PT320_Materialidade!B16"), ("Fator de confiança 95% (Poisson, 0 erros)", 3.0), ("Erro esperado (% do tolerável)", .10), ("Fator de expansão", 1.6)]
for i, (k, v) in enumerate(par, 3): u.cell(i, 1, k); u.cell(i, 2, v)
u["A9"] = "Intervalo de amostragem (R$ mil)"; u["B9"] = "=(B4-B6*B4*B7)/B5"; u["A10"] = "Tamanho teórico da amostra"; u["B10"] = "=B3/B9"
res = [("Itens selecionados", m["n_selecionado"]), ("Itens com distorção", m["itens_com_distorcao"]), ("Distorção projetada (R$ mil)", m["distorcao_projetada_R$mil"]), ("Limite superior Stringer (R$ mil)", m["limite_superior_Stringer_R$mil"]), ("Distorção real inserida (R$ mil)", m["distorcao_real_inserida_R$mil"]), ("Conclusão", m["conclusao"])]
for i, (k, v) in enumerate(res, 12): u.cell(i, 1, k); u.cell(i, 2, v)
larg(u, [50, 28]); wb.save(os.path.join(P, "Papeis_de_trabalho_calculos.xlsx")); print("planilha ok")
