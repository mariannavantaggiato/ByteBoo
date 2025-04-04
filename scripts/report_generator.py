from fpdf import FPDF
import json

# Carica i dati
with open("dataset/analisi_risultati.json", "r") as file:
    analisi = json.load(file)

# Creazione del PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Report Analisi Cybersecurity", ln=True, align="C")

for log_id, risultato in analisi.items():
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Log ID: {log_id}", ln=True)
    pdf.multi_cell(200, 10, txt=f"Analisi: {risultato}")

pdf.output("../datasets/report_analisi.pdf")

print("Report PDF generato con successo!")
