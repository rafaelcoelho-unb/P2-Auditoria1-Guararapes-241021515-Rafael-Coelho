"""Testes de auditoria sobre a BASE SINTÉTICA + comparação erros inseridos x identificados (PT 240, 500, 520)."""
import os, json, numpy as np, pandas as pd
from config import *
D = os.path.join(os.path.dirname(__file__), "..", "dados"); R = os.path.join(os.path.dirname(__file__), "..", "resultados"); os.makedirs(R, exist_ok=True)
b = pd.read_csv(os.path.join(D, "base_contas_receber_sintetica.csv.gz"), parse_dates=["data_origem", "data_vencimento", "data_lancamento"])
er = pd.read_csv(os.path.join(D, "registro_erros_inseridos.csv"))
DB = pd.Timestamp(DATA_BASE); rec = b[b.tipo_registro == "RECEBIVEL"]
res = {}
# ---------- T-01 conciliação com a NE 13 (R$ mil) ----------
mil = lambda s: round(s.sum() / 1000, 3)
rows = []
for p, v in NE13A.items(): rows.append(("produto", p, v, mil(rec[rec.produto == p].saldo_bruto_rs)))
for p, v in AJUSTES.items(): rows.append(("ajuste", p, v, mil(b[b.produto == p].saldo_bruto_rs)))
for a, v in AGING.items():
    s = b[b.faixa_aging == a].saldo_bruto_rs; rows.append(("aging", a, v, mil(s)))
rows.append(("total bruto", "Saldo bruto", SALDO_BRUTO_NE13, mil(b.saldo_bruto_rs)))
rows.append(("ECL", "Provisão total", ECL_TOTAL, mil(b.provisao_rs)))
rows.append(("líquido", "Saldo líquido", SALDO_LIQUIDO_NE13, mil(b.saldo_liquido_rs)))
for e, v in ECL_ESTAGIO.items(): rows.append(("ECL estágio", f"Estágio {e}", v, mil(b[(b.empresa == "Midway Financeira") & (b.estagio_ifrs9 == e)].provisao_rs)))
rc = pd.DataFrame(rows, columns=["bloco", "item", "ne_2025_mil", "base_sintetica_mil"]); rc["diferenca_mil"] = (rc.base_sintetica_mil - rc.ne_2025_mil).round(3)
rc.to_csv(os.path.join(R, "T01_conciliacao_NE13.csv"), index=False)
# explicação das diferenças pelo gabarito: linhas inseridas
ins = b[b.id_registro.str.contains(r"SYN-E0[1467]")]
res["T01"] = {"dif_bruto_mil": float(rc.loc[rc.bloco == "total bruto", "diferenca_mil"].iloc[0]),
              "bruto_linhas_inseridas_mil": mil(ins.saldo_bruto_rs), "dif_provisao_mil": float(rc.loc[rc.bloco == "ECL", "diferenca_mil"].iloc[0]),
              "dif_liquido_mil": float(rc.loc[rc.bloco == "líquido", "diferenca_mil"].iloc[0])}
# ---------- testes de exceção ----------
T = {}
T["T02_vencimento_antes_origem"] = rec[rec.data_vencimento < rec.data_origem]
T["T03_corte_origem_pos_2025"] = rec[rec.data_origem > DB]
d = rec[rec.duplicated("id_contrato", keep=False)]; T["T04_duplicidade_contrato"] = d
mid = rec[rec.empresa == "Midway Financeira"]
T["T05_estagio_incoerente_atraso"] = mid[((mid.estagio_ifrs9 == 1) & (mid.dias_atraso > 30)) | ((mid.estagio_ifrs9 == 2) & (mid.dias_atraso > 90))]
s3 = mid[mid.estagio_ifrs9 == 3]; T["T06_estagio3_provisao_baixa"] = s3[s3.provisao_rs < .20 * s3.saldo_bruto_rs]
T["T07_titulo_acima_541_dias"] = rec[rec.dias_atraso > 541]
we = rec.data_lancamento.dt.dayofweek >= 5
T["T08_manual_redondo_fim_periodo"] = rec[(rec.tipo_lancamento == "MANUAL") & (rec.saldo_bruto_rs % 50_000 == 0) & (rec.saldo_bruto_rs >= 50_000) & (we | (rec.data_lancamento >= "2025-12-20"))]
cols = ["id_registro", "produto", "id_contrato", "data_origem", "data_vencimento", "dias_atraso", "estagio_ifrs9", "saldo_bruto_rs", "provisao_rs", "tipo_lancamento", "data_lancamento"]
for k, v in T.items(): v[cols].to_csv(os.path.join(R, k + ".csv"), index=False)
mapa = {"E05": "T02_vencimento_antes_origem", "E01": "T03_corte_origem_pos_2025", "E04": "T04_duplicidade_contrato", "E02": "T05_estagio_incoerente_atraso",
        "E03": "T06_estagio3_provisao_baixa", "E06": "T07_titulo_acima_541_dias", "E07": "T08_manual_redondo_fim_periodo"}
comp = []
for e, t in mapa.items():
    ins_ = set(er[er.id_erro == e].id_registro); fl = set(T[t].id_registro); tp = len(ins_ & fl)
    comp.append({"id_erro": e, "teste": t, "inseridos": len(ins_), "sinalizados": len(fl), "identificados": tp,
                 "recall_pct": round(100 * tp / len(ins_), 1), "falsos_positivos": len(fl - ins_),
                 "distorcao_liquida_inserida_mil": round(er[er.id_erro == e].distorcao_liquida_rs.sum() / 1000, 1)})
comp = pd.DataFrame(comp); comp.to_csv(os.path.join(R, "comparacao_inseridos_x_identificados.csv"), index=False)
# ---------- T-09 analíticos ----------
an = []
for e in (1, 2, 3):
    g = mid[mid.estagio_ifrs9 == e]; an.append(("cobertura estágio %d (%%)" % e, round(100 * g.provisao_rs.sum() / g.saldo_bruto_rs.sum(), 2), {1: 4.48, 2: 29.84, 3: 75.28}[e]))
an.append(("cobertura total ECL/bruto (%)", round(100 * b.provisao_rs.sum() / b.saldo_bruto_rs.sum(), 2), round(100 * ECL_TOTAL / SALDO_BRUTO_NE13, 2)))
an.append(("vencido > 90 dias / estágio 3 (R$ mil)", mil(rec[rec.dias_atraso > 90].saldo_bruto_rs), 1_624_308))
pd.DataFrame(an, columns=["indicador", "base_sintetica", "referencia_NE"]).to_csv(os.path.join(R, "T09_analiticos.csv"), index=False)
res["comparacao"] = comp.to_dict("records"); res["linhas"] = int(len(b))
json.dump(res, open(os.path.join(R, "resumo_testes.json"), "w"), indent=1, default=float)
pd.set_option("display.width", 250); print(rc.to_string()); print(comp.to_string()); print(json.dumps(res["T01"]))
