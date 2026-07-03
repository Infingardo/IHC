import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm

# Lista FBF + Sacco (bianca) - AGGIORNATA con: BRG1/SMARCA4, FOSFOISTONE-H3, SALL4 aggiunti; ALK 1 rimosso
fbf_sacco = set([
    "ACTINA HHF35", "ACTINA m.l. (muscolo liscio)", "AFP/ALF (alfafetoproteina)",
    "ALK (D5F3)", "ANIDRASI CARBONICA (CAIX)", "ANDROGENI", "ANNEXIN A1",
    "ARGINASI-1", "ATRX", "Bcl2", "Bcl6", "Bcl10", "Betacatenina", "Ca125",
    "Calcitonina", "Caldesmone", "Calponina", "Calretinina",
    "CD1a", "CD2", "CD3", "CD4", "CD5", "CD7", "CD8", "CD10", "CD14", "CD15",
    "CD19", "CD20", "CD21", "CD23", "CD30", "CD31", "CD34", "CD38", "CD44",
    "CD45 (LCA)", "CD56", "CD61", "CD68 KP1", "CD68 PGM1", "CD79a", "CD99",
    "CD117/cKIT", "CD138", "CD163", "CDK4", "CDX2", "CEA Monoclonale",
    "Bcl1 (Ciclina D1)", "c-myc", "CMV", "Cromogranina", "CK5/6", "CK7", "CK19",
    "CK20", "CK34betaE12", "CK PAN", "CK CAM5.2",
    "CTRL Mon NEG (FOLR1/CLND18 RxDx)", "Desmina", "D2-40 (podoplanina)",
    "DOG1", "E-caderina EP700Y", "EMA", "EP-CAM (ber-EP4)",
    "Estrogeni (ER)", "ERG", "Fattore VIII", "FATTORE XIII", "Fumarato Idratasi",
    "Galectina 3", "GATA 3", "GFAP", "Glicoforina", "Glypican3", "GLUT 1",
    "GLUTAMINA SINTETASI", "Hepatocyte/HSA (specific antigen)", "hCG",
    "HER2 (c-erb B2)", "HHV8 (orf73)", "HGAL", "HMB45 (Melanosome)", "HPV",
    "HU/HUD", "IDH1", "IgG", "IgG4", "Inibina alpha", "Ki67", "KAPPA", "LAMBDA",
    "MAMMOGLOBINA", "Melan A (MART 1)", "MDM2", "Mieloperossidasi", "Miogenina",
    "MLH1", "MSH2", "MSH6", "MUM1", "Napsin A", "Neurofilamenti (NF)", "NKX3",
    "NSE", "OLIG2", "p16", "p53", "p57", "p63", "p40", "PAX5", "PAX8",
    "PDL1 (SP263)", "PDL1 (SP142)", "PHH3", "PLAP", "PML-RAR1", "PMS2", "PRAME",
    "Progesterone (PR)", "PSA", "PSAP", "PTEN", "RACEMASI (P504S AMACR)",
    "RCC", "S100", "SATB2", "Sinaptofisina", "SOX10", "SOX11", "STAT6",
    "TdT", "Tiroglobulina", "TTF1", "Vimentina", "WT1",
    "BRG1/SMARCA4", "FOSFOISTONE-H3", "SALL4", "Claudina-18"
])

# Lista Solo Sacco (rosa) - AGGIORNATA: ALK 1 aggiunto; BRG1/SMARCA4, FOSFOISTONE-H3, SALL4 rimossi
solo_sacco = [
    "ALK 1",
    "Amiloide A", "Amiloide P", "ANTI-BRAF", "ARID1A", "Aspergillus",
    "BAP1 (C-4)", "BRAF V600E", "Calbindin",
    "Candida Albicans", "CEA Policlonale", "CD11c", "CD16", "CD43", "CD57",
    "CD123", "CD146", "Chymotripsina (antichimotripsina)", "Claudina 4",
    "CMITA1", "Collagene IV", "CK MNF116", "DNAJB9",
    "EBV-LMP1", "EBER", "FOLR1 Rx Dx Assay", "FOSB", "c-FOS", "FOXL2",
    "Gastrina", "GCDFP15", "Granzyme B",
    "HBME 1 (Mesothelial cell)", "HCL DBA44", "hPL",
    "HSV I (Herpesvirus 1)", "HSV II (Herpesvirus 1/2)", "HIV p24",
    "IgA", "IgD", "IgM", "INI-1", "IRTA1/FCRL4", "LEF1",
    "MUC1", "MUC2", "MUC4", "MUC6", "MyoD1", "NeuN", "NRAS", "OCT 3/4",
    "OCT-2", "Pan-TRK", "Parvovirus B19", "Perforin", "PLA2R1",
    "Pneumocistis Carinii", "POLE", "PTH", "RB1 (SP384)", "ROS1 (SP384)",
    "SAR COV2", "SDHB", "SF1", "SOX2", "SV40", "TIA1", "TB", "TFEB",
    "Toxoplasma Gondii", "TREPONEMA SPIROCHETE", "Tri-Methyl-Histone H3",
    "WT49", "ZAP70", "Surfactante SPB"
]

def sort_key(name):
    m = re.match(r'^CD(\d+)(.*)', name, re.IGNORECASE)
    if m:
        return (0, int(m.group(1)), m.group(2).upper())
    return (1, name.upper(), "")

all_abs = sorted(list(fbf_sacco) + solo_sacco, key=sort_key)

ROSA = colors.HexColor('#FFB6C1')
BIANCO = colors.white

solo_sacco_set_check = set(s.upper() for s in solo_sacco)
all_abs_display = [f"{a} *" if a.upper() in solo_sacco_set_check else a for a in all_abs]

rows_flat = []
for i in range(0, len(all_abs_display), 3):
    row = all_abs_display[i:i+3]
    while len(row) < 3:
        row.append("")
    rows_flat.append(row)

doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/Pannello_AB_aggiornato.pdf",
    pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

title_style = ParagraphStyle('title', fontSize=14, fontName='Helvetica-Bold', spaceAfter=4)
legend_style = ParagraphStyle('legend', fontSize=8, fontName='Helvetica', spaceAfter=8)

story = []
story.append(Paragraph("PANNELLO ANTICORPI \u2013 SC ANATOMIA PATOLOGICA FBF\u2013SACCO", title_style))
story.append(Paragraph("Legenda: Riga bianca = disponibile FBF + Sacco | Riga rosa + asterisco (*) = disponibile solo Sacco", legend_style))

col_width = (A4[0] - 3*cm) / 3
table = Table(rows_flat, colWidths=[col_width]*3)

style_cmds = [
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#CCCCCC')),
    ('ROWBACKGROUND', (0,0), (-1,-1), BIANCO),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
]

for row_idx, row in enumerate(rows_flat):
    for col_idx, cell in enumerate(row):
        if cell.endswith(" *"):
            style_cmds.append(('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), ROSA))

table.setStyle(TableStyle(style_cmds))
story.append(table)

doc.build(story)
print(f"PDF generato. Totale anticorpi: {len(all_abs)} (FBF+Sacco: {len(fbf_sacco)}, Solo Sacco: {len(solo_sacco)})")
