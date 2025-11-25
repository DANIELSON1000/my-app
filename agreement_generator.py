# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 15:05:00 2025

@author: ELINA
"""

# agreement_generator.py
from fpdf import FPDF
from pathlib import Path
from database import timestamp_now

AGREEMENT_DIR = Path("agreements")
AGREEMENT_DIR.mkdir(exist_ok=True)

def generate_agreement(tenant: dict, landlord: dict):
    """
    tenant: dict with tenant fields
    landlord: dict with landlord info (name, phone, email, address)
    returns filepath
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AMASEZERANO YO GUKODESHA INZU", ln=1, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Amazina ya Nyir'inzu: {landlord.get('name','')}", ln=1)
    pdf.cell(0, 8, f"Telefone: {landlord.get('phone','')}", ln=1)
    pdf.cell(0, 8, f"Email: {landlord.get('email','')}", ln=1)
    pdf.ln(4)

    pdf.cell(0, 8, f"Amazina y'Umukiriya: {tenant.get('fullname','')}", ln=1)
    pdf.cell(0, 8, f"Indangamuntu: {tenant.get('id_number','')}", ln=1)
    pdf.cell(0, 8, f"Telefone: {tenant.get('phone','')}", ln=1)
    pdf.cell(0, 8, f"Igitsina: {tenant.get('sex','')}", ln=1)
    pdf.cell(0, 8, f"Abantu batuye mu nzu: {tenant.get('people','')}", ln=1)
    pdf.cell(0, 8, f"Status y'inzu: {tenant.get('house_status','')}", ln=1)
    pdf.cell(0, 8, f"Amafaranga y'ubukode buri kwezi: {tenant.get('rent','')}", ln=1)
    pdf.cell(0, 8, f"Itariki y'itangira: {tenant.get('start_date','')}", ln=1)
    pdf.ln(8)

    pdf.multi_cell(0, 7,
        "IKITONDERWA:\n"
        "1. Umukiriya agomba  kwishyura ubukode buri kwezi ku gihe.\n"
        "2. Kubahiriza isuku, kubungabunga ibikoresho n'ibindi byubatse inzu ni incingano zawe.\n"
        "3. Iyo umukiriya yatinze kwishyura , nyir'inzu afite uburenganzira bwo gukurikirana.\n"
    )
    pdf.ln(8)
    pdf.cell(0, 8, f"Itariki: {timestamp_now()}", ln=1)
    pdf.ln(12)
    pdf.cell(0, 8, "Umukiriya: _______________________", ln=1)
    pdf.cell(0, 8, "Nyir'inzu: _______________________", ln=1)

    filename = AGREEMENT_DIR / f"{tenant.get('tenant_id')}_agreement.pdf"
    pdf.output(str(filename))
    return str(filename)
