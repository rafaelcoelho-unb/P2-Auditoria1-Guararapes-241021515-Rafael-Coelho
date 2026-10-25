"""PT 510 – compara as colunas de 2024 da DFP 2025 (comparativos) com a DFP 2024 originalmente publicada (consolidado).
Uso: python3 07_comparar_dfp2024_2025.py DFP2025.pdf DFP2024.pdf   (requer pdftotext/poppler)"""
import re, subprocess, sys, os, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados"); os.makedirs(R, exist_ok=True)
def texto(pdf): return subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, check=True).stdout.decode("utf-8", "replace").split("\f")
def parse(pages, tag):
    out = {}
    for p in pages:
        if not re.search(r"DFs Consolidadas / " + tag, p): continue
        for l in p.splitlines():
            m = re.match(r"\s*(\d\.\d\d(?:\.\d\d)*|\d)\s+(.+?)\s{2,}(-?[\d\.]+|-)\s+(-?[\d\.]+|-)\s+(-?[\d\.]+|-)\s*$", l)
            if m:
                n = lambda s: 0 if s == "-" else int(s.replace(".", ""))
                out[m.group(1)] = (m.group(2).strip(), n(m.group(3)), n(m.group(4)), n(m.group(5)))
    return out
if __name__ == "__main__":
    p25, p24 = texto(sys.argv[1]), texto(sys.argv[2]); linhas = []
    for nome, tag in {"Balanço patrimonial": "Balanço Patrimonial", "DRE": "Demonstração do Resultado", "Fluxo de caixa": "Demonstração do Fluxo de Caixa"}.items():
        a, b = parse(p25, tag), parse(p24, tag)
        for k in sorted(set(a) & set(b)): linhas.append((nome, k, b[k][0], b[k][1], a[k][2], a[k][2] - b[k][1]))
    df = pd.DataFrame(linhas, columns=["demonstracao", "codigo_cvm", "conta", "valor_2024_DFP2024", "valor_2024_na_DFP2025", "diferenca"])
    df.to_csv(os.path.join(R, "comparativos_DFP2024_vs_DFP2025.csv"), index=False)
    print(df.groupby("demonstracao").agg(linhas=("codigo_cvm", "count"), divergentes=("diferenca", lambda s: int((s != 0).sum()))))
