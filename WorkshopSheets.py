#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rieke
"""

import pandas as pd
import os

from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from textwrap import wrap

workshops = pd.read_csv(r'2024_Workshops.csv')

pdfmetrics.registerFont(
  TTFont('OSBold', 'OpenSans-Bold.ttf')
)
pdfmetrics.registerFont(
  TTFont('OS', 'OpenSans-Regular.ttf')
)

def make_document(index):

    #formatting and creating of pdf document
    doc = canvas.Canvas("Workshop_"+str(index)+"_ohneHintergrund.pdf", pagesize=portrait(A4)) 
    
    doc.setFont('OSBold', 14)
    doc.drawString(50, 800, workshops['Task Name'][index])
    doc.setFont('OS', 12)

    doc.drawString(50, 700, workshops['Instructor (short text)'][index])
    doc.drawString(50, 600, workshops['Sprache / Taal / Language (labels)'][index].strip("[]"))
    
    #text with line breaks
    wraped_description ="\n".join(wrap(workshops['Kurze Beschreibung (text)'][index], 80))
    t = doc.beginText()
    t.setTextOrigin(50, 500)
    t.textLines(wraped_description)
    doc.drawText(t)
    
    doc.save()

    try:
        command = "pdftk Workshop_"+str(index)+"_ohneHintergrund.pdf background WorkshopBackground.pdf output Workshop_"+str(index)+".pdf"
        os.system(command)
        command2 = "rm Workshop_"+str(index)+"_ohneHintergrund.pdf"
        os.system(command2)
    except:
        print("can't combine")
        
#loop through all workshops
for i in range(0, len(workshops.index)):
    make_document(i)
