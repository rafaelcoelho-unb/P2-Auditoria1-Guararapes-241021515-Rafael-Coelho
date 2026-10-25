# Dossiê de auditoria da Guararapes (Riachuelo) – exercício de 2025

**UnB – Auditoria 1 (CCA0024), Turma 02, 2026.2 – Prof. Lucas Oliveira Gomes Ferreira**
**P2 – entrega em 25/10/2026 – trabalho individual**

| Campo | Informação |
|---|---|
| Aluno | Rafael Pinheiro Gonçalves Coelho |
| Matrícula | 241021515 |
| Companhia atribuída | Guararapes Confecções S.A. (nome de pregão Riachuelo; GUAR3 → RIAA3 em 05/02/2026, confirmado na NE 1 da DFP 2025, p.52) |
| Documentos base | DFP 2025 completa (CVM), incluindo notas explicativas e relatório do auditor (PwC); DFP 2024 completa (em uso no PT 510); ITRs e FRE de 2026 não obtidos (limitação declarada no PT 560) |

> **Aviso.** Trabalho acadêmico, não é opinião de auditoria independente nem asseguração. Dados reais vêm de documentos públicos. **A base de dados e os resultados dos testes de detalhe são sintéticos** e não representam registros da companhia. Nenhuma confirmação, entrevista, inspeção ou acesso a sistemas foi realizado. Uso de IA (Claude) autorizado pelo professor da disciplina (declaração do aluno).

## Estrutura do repositório
```
README.md
matriz_cobertura_normas.csv   norma -> papel de trabalho -> arquivos de apoio
dossie/        papéis de trabalho (.md), programas, conclusão e PDF final (Dossie_Auditoria_Guararapes_2025_P2.pdf)
dados/         base sintética, dicionário, registro de erros inseridos
codigo/        geração, testes, amostragem, planilhas
planilhas/     materialidade, conciliações, analíticos, amostras
resultados/    saídas dos testes
fontes/        relacao_fontes.md
```

## Como reproduzir
```
pip install -r codigo/requirements.txt     # numpy, pandas, openpyxl
bash codigo/05_executar_tudo.sh             # gera base, testes, amostragem e planilhas (~2 min)
python3 codigo/07_comparar_dfp2024_2025.py DFP2025.pdf DFP2024.pdf   # PT 510 (requer os PDFs originais da CVM e pdftotext)
python3 codigo/06_montar_dossie_pdf.py      # remonta o PDF (requer pandoc e wkhtmltopdf)
```
Ambiente de referência: Python 3.12.3, numpy 2.4.4, pandas 3.0.2. Semente = matrícula 241021515.
SHA-256 do CSV descomprimido: `ed6b2fb119b136d104b30983f92ac9a5d6f232469f6ba87bac4d8dfbed296b5f`.
Conta escolhida: **Contas a receber de clientes** (R$ 5.478.486 mil líquido; 36,8% do ativo). Base: 522.622 linhas (≥ 500.000), 100% sintética.

## Limite do GitHub
A base tem ~22 MB compactada: fica no repositório (`dados/`). O código a reproduz.

## Limitações
Sem acesso à companhia, a evidência real é pública. A estrutura interna da base é hipótese do aluno; a conciliação com o saldo contábil é por calibração.
