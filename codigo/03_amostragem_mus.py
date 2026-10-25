"""PT 530 – Amostragem por Unidade Monetária (MUS) sobre a base sintética. Semente = matrícula."""
import os, json, numpy as np, pandas as pd
from config import *
D = os.path.join(os.path.dirname(__file__), "..", "dados"); R = os.path.join(os.path.dirname(__file__), "..", "resultados")
b = pd.read_csv(os.path.join(D, "base_contas_receber_sintetica.csv.gz"), usecols=["id_registro", "tipo_registro", "produto", "saldo_bruto_rs", "saldo_liquido_rs"])
gt = pd.read_csv(os.path.join(D, "verdade_terreno_valores_corretos.csv.gz"))
pop = b[(b.tipo_registro == "RECEBIVEL") & (b.saldo_bruto_rs > 0)].reset_index(drop=True)
BV = pop.saldo_bruto_rs.sum(); TM = PE * 1000.0               # erro tolerável = materialidade para execução (R$)
RF, EE_pct, EF = 3.0, 0.10, 1.6                               # 95% confiança; erro esperado 10% de TM; fator de expansão
intervalo = (TM - EE_pct * TM * EF) / RF
n_teor = BV / intervalo
rng = np.random.default_rng(SEED); inicio = rng.uniform(0, intervalo)
cum = pop.saldo_bruto_rs.cumsum().values
pontos = np.arange(inicio, BV, intervalo)
idx = np.unique(np.searchsorted(cum, pontos, side="left")); idx = idx[idx < len(pop)]
amo = pop.loc[idx].merge(gt, on="id_registro")
amo["distorcao_rs"] = (amo.liq_registrado_rs - amo.liq_correto_rs).round(2)         # sobrevalorização do valor líquido
amo["taint"] = (amo.distorcao_rs / amo.saldo_bruto_rs).clip(upper=1.0)
grandes = amo[amo.saldo_bruto_rs >= intervalo]; peq = amo[amo.saldo_bruto_rs < intervalo]
erros = peq[peq.taint > 0].sort_values("taint", ascending=False)
projetada = float(grandes.distorcao_rs.sum() + (peq.taint * intervalo).sum())
LAM = [2.996, 4.744, 6.296, 7.754, 9.154, 10.513, 11.842, 13.148, 14.435, 15.705, 16.962, 18.208, 19.443, 20.669, 21.886, 23.098, 24.302, 25.50, 26.69, 27.88, 29.06]
k = len(erros); lam = lambda i: LAM[i] if i < len(LAM) else LAM[-1] + 1.19 * (i - len(LAM) + 1)
precisao_basica = lam(0) * intervalo
incremento = sum(t * (lam(i + 1) - lam(i) - 1) * intervalo for i, t in enumerate(erros.taint.values))
uml = float(grandes.distorcao_rs.sum() + precisao_basica + incremento + (erros.taint.values * intervalo).sum())
distorcao_real = float((gt.liq_registrado_rs - gt.liq_correto_rs).sum())
res = {"populacao_linhas": int(len(pop)), "valor_contabil_R$mil": round(BV / 1000, 1), "TM_R$mil": TM / 1000, "intervalo_R$mil": round(intervalo / 1000, 1),
       "n_teorico": round(n_teor, 1), "n_selecionado": int(len(amo)), "itens_acima_intervalo": int(len(grandes)), "itens_com_distorcao": int(len(erros)) + int((grandes.distorcao_rs > 0).sum()),
       "distorcao_conhecida_grandes_R$mil": round(grandes.distorcao_rs.sum() / 1000, 1), "distorcao_projetada_R$mil": round(projetada / 1000, 1),
       "limite_superior_Stringer_R$mil": round(uml / 1000, 1), "distorcao_real_inserida_R$mil": round(distorcao_real / 1000, 1),
       "conclusao": "REJEITAR (limite superior > erro tolerável)" if uml > TM else "ACEITAR (limite superior <= erro tolerável)"}
amo[["id_registro", "produto", "saldo_bruto_rs", "liq_registrado_rs", "liq_correto_rs", "distorcao_rs", "taint"]].to_csv(os.path.join(R, "PT530_amostra_selecionada.csv"), index=False)
json.dump(res, open(os.path.join(R, "PT530_resultado.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps(res, indent=1, ensure_ascii=False))
