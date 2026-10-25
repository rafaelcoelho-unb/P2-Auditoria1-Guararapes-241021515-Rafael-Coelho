"""Gera a BASE SINTÉTICA de Contas a receber de clientes (Guararapes/Riachuelo, 31/12/2025).
Todos os registros são SINTÉTICOS. Os totais são calibrados às Notas Explicativas 2025 (dados reais).
Uso: python3 01_gerar_base.py   (semente = matrícula 241021515)"""
import os, numpy as np, pandas as pd
from config import *
rng = np.random.default_rng(SEED)
OUT = os.path.join(os.path.dirname(__file__), "..", "dados"); os.makedirs(OUT, exist_ok=True)
DB = pd.Timestamp(DATA_BASE)
CENT = 100  # trabalhamos em centavos inteiros (R$ mil -> R$ * 1000 -> centavos)

def alloc(total_cents, w):
    """Distribui total_cents (int) em partes inteiras proporcionais a w; resto vai à maior parte."""
    w = np.asarray(w, float); p = np.floor(total_cents * w / w.sum()).astype(np.int64)
    p[np.argmax(w)] += total_cents - p.sum(); return p

# ---- IPF: matriz produto Midway (cartão, CP) x célula, fechando linhas (NE13a) e colunas (células) ----
cel_tot = np.array([c[2] for c in CELULAS], float)
seed_cp = np.array([.12, .30, .14, .30, .16, .30, .18, .30, .20, .22, .24])  # CP mais concentrado em atraso
M = np.vstack([cel_tot * (1 - seed_cp), cel_tot * seed_cp])
rows = np.array([NE13A["CARTAO_RIACHUELO"], NE13A["CREDITO_PESSOAL"]], float)
for _ in range(200):
    M *= (rows / M.sum(1))[:, None]; M *= (cel_tot / M.sum(0))[None, :]
M_c = np.vstack([alloc(int(round(rows[i] * 1000 * CENT)), M[i]) for i in range(2)])  # aproximação inicial
# fechamento exato por célula (centavos): ajusta o cartão para a soma da coluna bater
for j, c in enumerate(CELULAS):
    alvo = c[2] * 1000 * CENT; M_c[0, j] += alvo - M_c[:, j].sum()
dif = rows[0] * 1000 * CENT - M_c[0].sum(); M_c[0, np.argmax(M_c[0])] += int(dif); M_c[1, np.argmax(M_c[1])] -= int(dif)
# (o ajuste acima pode deixar 1 centavo-milhar entre linhas/colunas; a conciliação final em 'reconciliacao' mostra o resíduo)

registros = []
def nova(prod, empresa, cel_idx, n, total_cents, estagio, renego, aging):
    lo, hi = FAIXA_ATRASO[aging] if aging else (0, 0)
    w = rng.lognormal(0, 1.0, n); val = alloc(int(total_cents), w)
    atraso = rng.integers(lo, hi + 1, n) if aging != "A_VENCER" else np.zeros(n, int)
    df = pd.DataFrame({"produto": prod, "empresa": empresa, "estagio_ifrs9": estagio, "flag_renegociado": renego,
                       "faixa_aging": aging, "dias_atraso": atraso, "saldo_bruto_cent": val})
    registros.append(df)

for j, c in enumerate(CELULAS):
    est, ag, _, ren = c
    for i, prod in enumerate(["CARTAO_RIACHUELO", "CREDITO_PESSOAL"]):
        # nº de linhas proporcional ao valor da célula dentro do produto (mesmo ticket médio)
        n = max(1, int(round(LINHAS_PRODUTO[prod] * M_c[i, j] / M_c[i].sum())))
        nova(prod, "Midway Financeira", j, n, M_c[i, j], est, ren, ag)
nova("CARTAO_TERCEIROS", "Lojas Riachuelo", None, LINHAS_PRODUTO["CARTAO_TERCEIROS"], NE13A["CARTAO_TERCEIROS"] * 1000 * CENT, 0, 0, "A_VENCER")
nova("CESSAO_FIDC", "FIDC Midway EP", None, LINHAS_PRODUTO["CESSAO_FIDC"], NE13A["CESSAO_FIDC"] * 1000 * CENT, 1, 0, "A_VENCER")
nova("OUTROS_VALORES", "Lojas Riachuelo", None, LINHAS_PRODUTO["OUTROS_VALORES"], NE13A["OUTROS_VALORES"] * 1000 * CENT, 0, 0, "A_VENCER")
b = pd.concat(registros, ignore_index=True)
# pequena parcela de renegociados também fora do estágio 3 (cenário natural)
m = (b.empresa == "Midway Financeira") & (b.flag_renegociado == 0)
b.loc[m & (rng.random(len(b)) < 0.01), "flag_renegociado"] = 1
b.loc[b.estagio_ifrs9.isin([0]) & ~b.produto.isin(["CARTAO_TERCEIROS", "OUTROS_VALORES"]), "estagio_ifrs9"] = 0

# ---- provisão (ECL) ----
b["provisao_cent"] = 0
for est, tot in ECL_ESTAGIO.items():
    m = (b.empresa == "Midway Financeira") & (b.estagio_ifrs9 == est)
    taxa = np.where(est == 3, b.loc[m, "faixa_aging"].map(PESO_PROV_S3), 1.0) * rng.uniform(.85, 1.15, m.sum())
    b.loc[m, "provisao_cent"] = alloc(tot * 1000 * CENT, b.loc[m, "saldo_bruto_cent"].values * taxa)
m = b.empresa == "FIDC Midway EP"; b.loc[m, "provisao_cent"] = alloc(ECL_FIDC * 1000 * CENT, b.loc[m, "saldo_bruto_cent"].values)
b.loc[~b.empresa.isin(["Midway Financeira", "FIDC Midway EP"]), "estagio_ifrs9"] = 0  # 0 = não aplicável (sem estágio)

# ---- atributos descritivos (sintéticos) ----
n = len(b)
rng.shuffle(b.values) if False else None
b = b.sample(frac=1, random_state=SEED).reset_index(drop=True)
b.insert(0, "id_registro", ["SYN-%07d" % i for i in range(1, n + 1)])
b["id_contrato"] = ["CT%09d" % x for x in rng.permutation(np.arange(100_000_000, 100_000_000 + n))]
b["id_cliente"] = ["CL%07d" % x for x in rng.integers(1, int(n * .72), n)]
due_dias = np.where(b.faixa_aging == "A_VENCER",
                    np.where(b.produto == "CREDITO_PESSOAL", rng.integers(1, 1400, n), rng.integers(1, 61, n)), 0)
b["data_vencimento"] = DB + pd.to_timedelta(due_dias, "D") - pd.to_timedelta(b.dias_atraso, "D")
idade = np.where(b.produto == "CREDITO_PESSOAL", rng.integers(60, 1500, n), rng.integers(30, 2400, n))
dt_orig = b.data_vencimento - pd.to_timedelta(idade, "D")
fidc = b.produto == "CESSAO_FIDC"; terc = b.produto.isin(["CARTAO_TERCEIROS"]); outr = b.produto == "OUTROS_VALORES"
dt_orig[fidc] = pd.Timestamp("2025-11-14") + pd.to_timedelta(rng.integers(0, 47, fidc.sum()), "D")
b.loc[fidc, "data_vencimento"] = dt_orig[fidc] + pd.to_timedelta(rng.integers(120, 900, fidc.sum()), "D")
dt_orig[terc] = DB - pd.to_timedelta(rng.integers(0, 55, terc.sum()), "D")
b.loc[terc, "data_vencimento"] = dt_orig[terc] + pd.to_timedelta(rng.integers(15, 90, terc.sum()), "D")
dt_orig[outr] = DB - pd.to_timedelta(rng.integers(0, 300, outr.sum()), "D")
b.loc[outr, "data_vencimento"] = DB + pd.to_timedelta(rng.integers(1, 120, outr.sum()), "D")
# origem nunca posterior à data-base (a base legítima não contém recebíveis de 2026)
dt_orig = np.minimum(dt_orig, DB - pd.to_timedelta(rng.integers(0, 31, n), "D"))
b["data_origem"] = pd.Series(dt_orig).clip(lower=pd.Timestamp("2015-01-01"))
b["data_lancamento"] = np.minimum(b.data_origem + pd.to_timedelta(rng.integers(0, 3, n), "D"), DB)
b["tipo_lancamento"] = np.where(rng.random(n) < .003, "MANUAL", "AUTOMATICO")
b["usuario_lancamento"] = np.where(b.tipo_lancamento == "MANUAL", ["USR%03d" % x for x in rng.integers(1, 40, n)], "SYS_BATCH")
ufs = ["RN", "CE", "PE", "BA", "SP", "RJ", "MG", "PA", "AM", "MA", "PB", "PI", "SE", "AL", "GO", "DF", "PR", "SC", "RS", "ES", "MT", "MS", "TO", "RO", "AC", "AP", "RR"]
pu = np.array([8, 7, 8, 7, 14, 6, 6, 4, 3, 4, 3, 2, 2, 2, 3, 2, 3, 2, 3, 2, 1.5, 1.2, .7, .6, .3, .3, .2]); pu /= pu.sum()
b["uf"] = rng.choice(ufs, n, p=pu)
b["canal_origem"] = rng.choice(["LOJA_FISICA", "APP", "ECOMMERCE"], n, p=[.62, .26, .12])
b["faixa_score"] = rng.choice(["A", "B", "C", "D", "E"], n, p=[.18, .30, .27, .16, .09])
b["taxa_mensal_pct"] = np.where(b.produto == "CREDITO_PESSOAL", rng.uniform(3.5, 9.5, n), np.where(b.produto == "CARTAO_RIACHUELO", rng.uniform(6, 13, n), 0)).round(2)
b["tipo_registro"] = "RECEBIVEL"
# ---- linhas de ajuste contábil (negativas) ----
aj = pd.DataFrame({"id_registro": ["SYN-AJ%04d" % i for i in (1, 2)], "produto": list(AJUSTES), "empresa": ["Midway Financeira", "Grupo"],
                   "estagio_ifrs9": 0, "flag_renegociado": 0, "faixa_aging": "A_VENCER", "dias_atraso": 0,
                   "saldo_bruto_cent": [v * 1000 * CENT for v in AJUSTES.values()], "provisao_cent": 0,
                   "id_contrato": ["AJ-001", "AJ-002"], "id_cliente": "N/A", "data_vencimento": DB, "data_origem": DB, "data_lancamento": DB,
                   "tipo_lancamento": "MANUAL", "usuario_lancamento": "CONTABIL", "uf": "RN", "canal_origem": "N/A", "faixa_score": "N/A",
                   "taxa_mensal_pct": 0.0, "tipo_registro": "AJUSTE"})
b = pd.concat([b, aj], ignore_index=True)
b["fonte"] = "SINTETICO"
b.to_pickle(os.path.join(OUT, "_base_limpa.pkl"))

# ================== INJEÇÃO DE ERROS (registro de gabarito) ==================
erros, extras = [], []
def add_linhas(tipo, n_, total_mil, **kw):
    """Cria n_ linhas NOVAS (inseridas) somando total_mil (R$ mil)."""
    val = alloc(int(total_mil * 1000 * CENT), rng.lognormal(0, .9, n_))
    base = b[(b.tipo_registro == "RECEBIVEL") & (b.produto == "CARTAO_RIACHUELO") & (b.faixa_aging == "A_VENCER")].sample(n_, random_state=int(rng.integers(1e9))).copy()
    base["saldo_bruto_cent"] = val; base["provisao_cent"] = 0; base["estagio_ifrs9"] = 1; base["flag_renegociado"] = 0
    base["id_registro"] = ["SYN-%s%05d" % (tipo, i) for i in range(1, n_ + 1)]
    base["id_contrato"] = ["CT9%s%06d" % (tipo[-1], i) for i in range(1, n_ + 1)]
    for k, v in kw.items(): base[k] = v(base) if callable(v) else v
    extras.append(base); return base
def registra(df, tipo, desc, dgross=None, dprov=None, val_correto_liq=None):
    for r in df.itertuples():
        erros.append({"id_erro": tipo, "id_registro": r.id_registro, "descricao": desc})

# E01 corte: recebíveis originados em jan/2026 incluídos no saldo de dez/2025 (R$ 14.800 mil)
e1 = add_linhas("E01", 1100, 14_800, data_origem=lambda d: pd.Timestamp("2026-01-02") + pd.to_timedelta(rng.integers(0, 8, len(d)), "D"),
                data_lancamento=lambda d: pd.Timestamp("2025-12-31"))
e1["data_vencimento"] = e1.data_origem + pd.to_timedelta(30, "D")
# E04 duplicidade: contrato lançado duas vezes (R$ 9.600 mil)
orig = b[(b.tipo_registro == "RECEBIVEL") & (b.faixa_aging == "A_VENCER") & (b.empresa == "Midway Financeira")]
alvo = int(9_600 * 1000 * CENT); cands = orig.sample(5000, random_state=7); cs = cands.saldo_bruto_cent.cumsum()
sel = cands[cs <= alvo].head(700).copy()
sel["id_registro"] = ["SYN-E04%05d" % i for i in range(1, len(sel) + 1)]   # nova linha, mesmo contrato/cliente/valor
sel["id_contrato"] = cands[cs <= alvo].head(700).id_contrato.values
extras.append(sel); e4 = sel
# E06 baixa devida não efetuada: vencidos > 541 dias mantidos (R$ 10.800 mil bruto, provisão 95%)
e6 = add_linhas("E06", 800, 10_800, faixa_aging="361_540", estagio_ifrs9=3, flag_renegociado=0)
e6["dias_atraso"] = rng.integers(560, 900, len(e6)); e6["data_vencimento"] = DB - pd.to_timedelta(e6.dias_atraso, "D")
e6["data_origem"] = e6.data_vencimento - pd.to_timedelta(rng.integers(100, 900, len(e6)), "D"); e6["provisao_cent"] = (e6.saldo_bruto_cent * .95).astype(np.int64)
# E07 lançamentos manuais, valores redondos, fim de semana de fim de período (R$ ~ 9.000 mil)
e7 = add_linhas("E07", 60, 9_000, tipo_lancamento="MANUAL", usuario_lancamento=lambda d: np.array(["USR007"] * len(d)),
                data_lancamento=lambda d: pd.to_datetime(rng.choice(["2025-12-27", "2025-12-28"], len(d))))
r = (np.round(e7.saldo_bruto_cent / 100 / 50_000) * 50_000).clip(50_000); r = r.astype(np.int64) * 100
e7["saldo_bruto_cent"] = r.values
# E02 estágio incorreto: S3 (91-360 dias) classificados em estágio 1, provisão recalculada à taxa do estágio 1 (~4,48%)
s3 = b[(b.estagio_ifrs9 == 3) & b.faixa_aging.isin(["91_180", "181_360"]) & (b.empresa == "Midway Financeira")].sample(2500, random_state=11).index
e2 = b.loc[s3]; b.loc[s3, "provisao_cent"] = (b.loc[s3, "saldo_bruto_cent"] * .0448).astype(np.int64); b.loc[s3, "estagio_ifrs9"] = 1
# E03 provisão não constituída: S3 > 180 dias com provisão zero
s3b = b[(b.estagio_ifrs9 == 3) & (b.faixa_aging.isin(["181_360", "361_540"])) & (b.empresa == "Midway Financeira")].sample(600, random_state=13).index
e3 = b.loc[s3b]; b.loc[s3b, "provisao_cent"] = 0
# E05 inconsistência de datas: vencimento anterior à origem (sem efeito monetário)
s5 = b[(b.tipo_registro == "RECEBIVEL") & (b.faixa_aging == "A_VENCER")].sample(400, random_state=17).index
e5 = b.loc[s5]; b.loc[s5, "data_vencimento"] = b.loc[s5, "data_origem"] - pd.to_timedelta(rng.integers(1, 40, len(s5)), "D")

for df, tipo, desc in [(e1, "E01", "Corte: recebível de jan/2026 no saldo de dez/2025"), (e4, "E04", "Duplicidade de contrato"),
                       (e6, "E06", "Título > 541 dias não baixado (política NE 13)"), (e7, "E07", "Lançamento manual, valor redondo, fim de semana/fim de período"),
                       (e2, "E02", "Estágio 3 classificado como estágio 1 com provisão a ~4,5%"), (e3, "E03", "Estágio 3 > 180 dias sem provisão"),
                       (e5, "E05", "Data de vencimento anterior à data de origem")]:
    registra(df, tipo, desc)
base = pd.concat([b] + extras, ignore_index=True)
# gabarito: valor líquido correto de cada linha com erro
gt = base[["id_registro", "saldo_bruto_cent", "provisao_cent"]].copy(); gt["liq_registrado_cent"] = gt.saldo_bruto_cent - gt.provisao_cent
gt["liq_correto_cent"] = gt.liq_registrado_cent
ids = lambda d: gt.id_registro.isin(d.id_registro)
gt.loc[ids(e1) | ids(e4), "liq_correto_cent"] = 0                      # não deveriam existir
gt.loc[ids(e6), "liq_correto_cent"] = 0                               # deveriam estar baixados
gt.loc[ids(e7), "liq_correto_cent"] = 0                               # lançamento indevido (premissa do cenário)
for d in (e2, e3):                                                    # provisão correta ~ 75,28% (taxa média do estágio 3)
    m = ids(d); gt.loc[m, "liq_correto_cent"] = (gt.loc[m, "saldo_bruto_cent"] * (1 - .7528)).astype(np.int64)
for d in (e2, e3):
    pass
base["saldo_liquido_cent"] = base.saldo_bruto_cent - base.provisao_cent
for c in ["saldo_bruto", "provisao", "saldo_liquido"]:
    base[c + "_rs"] = (base[c + "_cent"] / 100).round(2)
base = base.sample(frac=1, random_state=SEED).reset_index(drop=True)
cols = ["id_registro", "tipo_registro", "fonte", "empresa", "produto", "id_contrato", "id_cliente", "data_origem", "data_vencimento", "dias_atraso",
        "faixa_aging", "estagio_ifrs9", "flag_renegociado", "saldo_bruto_rs", "provisao_rs", "saldo_liquido_rs", "taxa_mensal_pct",
        "uf", "canal_origem", "faixa_score", "data_lancamento", "tipo_lancamento", "usuario_lancamento"]
base[cols].to_csv(os.path.join(OUT, "base_contas_receber_sintetica.csv.gz"), index=False, compression="gzip", date_format="%Y-%m-%d")
gt["liq_registrado_rs"] = (gt.liq_registrado_cent / 100).round(2); gt["liq_correto_rs"] = (gt.liq_correto_cent / 100).round(2)
gt[["id_registro", "liq_registrado_rs", "liq_correto_rs"]].to_csv(os.path.join(OUT, "verdade_terreno_valores_corretos.csv.gz"), index=False, compression="gzip")
er = pd.DataFrame(erros).merge(gt[["id_registro", "liq_registrado_rs", "liq_correto_rs"]], on="id_registro")
er["distorcao_liquida_rs"] = (er.liq_registrado_rs - er.liq_correto_rs).round(2)
er.to_csv(os.path.join(OUT, "registro_erros_inseridos.csv"), index=False)
if os.path.exists(os.path.join(OUT, "_base_limpa.pkl")): os.remove(os.path.join(OUT, "_base_limpa.pkl"))
print("linhas:", len(base), "| recebíveis:", (base.tipo_registro == "RECEBIVEL").sum())
print("erros inseridos:", er.groupby("id_erro").agg(n=("id_registro", "count"), distorcao_mil=("distorcao_liquida_rs", lambda s: round(s.sum() / 1000, 1))).to_dict("index"))
