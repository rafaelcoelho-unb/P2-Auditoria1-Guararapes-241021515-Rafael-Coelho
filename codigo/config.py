"""Parâmetros comuns. Valores REAIS vêm das Notas Explicativas 2025 (R$ mil, consolidado).
Tudo o que é gerado a partir deles é SINTÉTICO."""
MATRICULA = 241021515
SEED = MATRICULA
DATA_BASE = "2025-12-31"
N_LINHAS = 520_000

# NE 13(a) – composição do saldo bruto (R$ mil)
NE13A = {"CARTAO_RIACHUELO": 5_730_153, "CREDITO_PESSOAL": 886_008, "CARTAO_TERCEIROS": 386_955,
         "CESSAO_FIDC": 50_461, "OUTROS_VALORES": 50_396}
AJUSTES = {"PROVISAO_LIMITE_A_LIBERAR": -34_104, "AVP": -4_368}
SALDO_BRUTO_NE13 = 7_065_501      # soma de NE13A + AJUSTES
ECL_TOTAL = 1_587_015             # NE 13(e)/(f)
SALDO_LIQUIDO_NE13 = 5_478_486

# NE 13(d) – aging (R$ mil). Premissa P1: ajustes (-38.472) alocados ao 'à vencer'.
AGING = {"A_VENCER": 5_094_838, "ATE_30": 145_437, "31_60": 90_881, "61_90": 110_037,
         "91_180": 380_520, "181_360": 732_035, "361_540": 511_753}
# NE 13(g) – estágios IFRS 9 da Midway Financeira (R$ mil) e provisão
ECL_ESTAGIO = {1: 209_602, 2: 53_537, 3: 1_322_917}
ECL_FIDC = 959
# Células (estágio x aging) que reconciliam NE 13(d) e NE 13(g) ao mesmo tempo (premissa P2:
# parte do estágio 3 tem atraso <= 90 dias – renegociados/período de cura – para fechar as duas notas).
CELULAS = [  # (estagio, aging, R$ mil, renegociado)
    (1, "A_VENCER", 4_555_498, 0), (3, "A_VENCER", 90_000, 1),
    (1, "ATE_30", 123_975, 0),     (3, "ATE_30", 21_462, 1),
    (2, "31_60", 81_365, 0),       (3, "31_60", 9_516, 1),
    (2, "61_90", 98_037, 0),       (3, "61_90", 12_000, 1),
    (3, "91_180", 380_520, 0),     (3, "181_360", 732_035, 0), (3, "361_540", 511_753, 0)]
FAIXA_ATRASO = {"A_VENCER": (0, 0), "ATE_30": (1, 30), "31_60": (31, 60), "61_90": (61, 90),
                "91_180": (91, 180), "181_360": (181, 360), "361_540": (361, 540)}
# taxa relativa de provisão por célula de estágio 3 (reescalada para fechar a NE 13(g))
PESO_PROV_S3 = {"A_VENCER": .40, "ATE_30": .40, "31_60": .40, "61_90": .40,
                "91_180": .60, "181_360": .80, "361_540": .92}
LINHAS_PRODUTO = {"CARTAO_RIACHUELO": 330_000, "CREDITO_PESSOAL": 100_000, "CARTAO_TERCEIROS": 50_000,
                  "CESSAO_FIDC": 15_000, "OUTROS_VALORES": 25_000}
# Materialidade (PT 320), R$ mil
LAIR_2025 = 1_878_987
GANHO_MIDWAY_MALL = 1_204_894   # NE 5.3, ganho líquido antes dos tributos
LAIR_NORMALIZADO = LAIR_2025 - GANHO_MIDWAY_MALL
PM = 33_700
PE = 25_275
TRIVIAL = 1_685
