"""Monta o dossiê em PDF a partir dos papéis em dossie/*.md (pandoc + wkhtmltopdf). Uso: python3 06_montar_dossie_pdf.py"""
import subprocess, pathlib, re, datetime
R = pathlib.Path(__file__).resolve().parent.parent; D = R / "dossie"
ordem = ["PT_EC_estrutura_conceitual", "PT_200_objetivos_gerais", "PT_210_termos_do_trabalho", "PT_220_gestao_da_qualidade", "PT_230_documentacao",
         "PT_240_fraude", "PT_250_leis_e_regulamentos", "PT_260_comunicacao_governanca", "PT_265_deficiencias_controle", "PT_300_planejamento",
         "PT_315_riscos", "PT_320_materialidade", "PT_330_respostas_aos_riscos", "PT_402_servicos_terceirizados", "PT_450_distorcoes", "PT_500_evidencia",
         "PT_501_itens_especificos", "PT_505_confirmacoes_externas", "PT_510_saldos_iniciais", "PT_520_analiticos", "PT_530_amostragem", "PT_540_estimativas",
         "PT_550_partes_relacionadas", "PT_560_eventos_subsequentes", "PT_570_continuidade_operacional", "PT_580_representacoes_formais", "PT_600_auditoria_de_grupos",
         "PROGRAMAS_DE_AUDITORIA", "BASE_SIMULADA_justificativa", "CONCLUSAO_INTEGRADA"]
capa = f"""<div class="capa"><p class="u">Universidade de Brasília – UnB · Auditoria 1 (CCA0024) · Turma 02 · 2026.2<br>Prof. Lucas Oliveira Gomes Ferreira</p>
<h1 class="tt">Dossiê de Auditoria – P2</h1><h2 class="st">Guararapes Confecções S.A. (RIAA3 – Riachuelo)<br>Exercício encerrado em 31/12/2025</h2>
<p class="m">Aluno: Rafael Pinheiro Gonçalves Coelho · Matrícula 241021515<br>Data de elaboração: 25/10/2026</p>
<div class="av"><b>Aviso.</b> Trabalho acadêmico. Não contém opinião de auditoria independente nem asseguração. Dados reais: documentos públicos (DFP 2025 e notas explicativas). Base de dados e testes de detalhe: <b>sintéticos</b>. Nenhuma confirmação, entrevista, inspeção ou acesso a sistemas foi realizado. Uso de IA (Claude) autorizado pelo professor. Versões das NBC TA: conferidas na lista oficial do CFC em 25/10/2026 (PT 230, seção 7). Campos de revisão em branco.</div></div>"""
md = []
for n in ordem:
    t = (D / f"{n}.md").read_text(encoding="utf-8"); md.append('<div class="pb"></div>\n\n' + t)
md.append('<div class="pb"></div>\n\n# Anexo A – Matriz de cobertura das normas\n\n' + "\n".join(
    ["| Norma | PT | Arquivo | Apoio | Estado |", "|---|---|---|---|---|"] + ["| " + " | ".join(str(c).replace("|", "/") for c in l.split(",")[:5]) + " |" for l in (R / "matriz_cobertura_normas.csv").read_text(encoding="utf-8").splitlines()[1:]]))
md.append('<div class="pb"></div>\n\n' + (R / "fontes" / "relacao_fontes.md").read_text(encoding="utf-8").replace("# Relação", "# Anexo B – Relação", 1))
src = D / "_dossie_completo.md"; src.write_text(capa + "\n\n" + "\n\n".join(md), encoding="utf-8")
css = R / "dossie" / "_estilo.css"
css.write_text("""body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:9.2pt;line-height:1.35;color:#111}
h1{font-size:15pt;color:#1F3864;border-bottom:2px solid #1F3864;padding-bottom:3px;margin-top:0}h2{font-size:11.5pt;color:#1F3864;margin-top:14px}
table{border-collapse:collapse;width:100%;margin:6px 0;font-size:8pt}th{background:#1F3864;color:#fff;padding:3px 4px;text-align:left}td{border:1px solid #bbb;padding:3px 4px;vertical-align:top}
tr{page-break-inside:avoid}code{font-size:8pt;background:#f2f2f2}blockquote{border-left:3px solid #c00;margin:6px 0;padding:2px 8px;background:#fdf1f1}
.pb{page-break-before:always}.capa{text-align:center;padding-top:90px;page-break-after:always}.tt{font-size:26pt;border:none}.st{font-size:14pt}.u,.m{font-size:10pt}.av{margin-top:50px;text-align:left;border:1px solid #c00;padding:10px;font-size:9pt}
#TOC{page-break-after:always}""", encoding="utf-8")
html = D / "_dossie_completo.html"
subprocess.run(["pandoc", str(src), "-f", "markdown-tex_math_dollars+pipe_tables+raw_html", "-t", "html5", "-s", "--toc", "--toc-depth=1", "--metadata", "title=Dossiê de Auditoria – Guararapes 2025 (P2)",
                "-c", str(css), "-o", str(html)], check=True)
txt = html.read_text(encoding="utf-8"); txt = re.sub(r'<header id="title-block-header">.*?</header>', "", txt, flags=re.S)
m = re.search(r'<nav id="TOC".*?</nav>', txt, flags=re.S); nav = m.group(0); txt = txt.replace(nav, "")
nav = nav.replace("<nav", '<h1>Índice dos papéis de trabalho</h1><nav', 1)
mm = re.search(r'<div class="pb">\s*</div>', txt); i = mm.start(); txt = txt[:i] + '<div class="pb"></div>' + nav + txt[i:]   # capa -> índice -> papéis
html.write_text(txt, encoding="utf-8")
out = R / "dossie" / "Dossie_Auditoria_Guararapes_2025_P2.pdf"
subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "--page-size", "A4", "-T", "14mm", "-B", "16mm", "-L", "12mm", "-R", "12mm",
                "--footer-center", "Dossiê P2 – Guararapes 2025 – Matrícula 241021515 – pág. [page]/[topage]", "--footer-font-size", "7", str(html), str(out)], check=True)
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
r = PdfReader(str(out)); w = PdfWriter(); n = len(r.pages)
for k, pg in enumerate(r.pages, 1):
    W = float(pg.mediabox.width); H = float(pg.mediabox.height); buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H)); c.setFont("Helvetica", 7); c.setFillGray(.35)
    if k > 1: c.drawCentredString(W / 2, 22, f"Dossie P2 - Guararapes 2025 - Matricula 241021515 - pag. {k}/{n}")
    c.save(); buf.seek(0); pg.merge_page(PdfReader(buf).pages[0]); w.add_page(pg)
w.add_metadata({"/Title": "Dossie de Auditoria - Guararapes 2025 (P2)", "/Author": "Matricula 241021515"}); w.write(str(out))
for f in (src, html, css): f.unlink()
print("PDF:", out, round(out.stat().st_size / 1e6, 2), "MB")
