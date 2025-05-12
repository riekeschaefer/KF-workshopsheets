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

workshops = pd.read_csv(r'2025_Workshops.csv')

pdfmetrics.registerFont(
    TTFont('OSBold', 'OpenSans-Bold.ttf')
)
pdfmetrics.registerFont(
    TTFont('OS', 'OpenSans-Regular.ttf')
)
pdfmetrics.registerFont(
    TTFont('OSItalic', 'OpenSans-Italic.ttf')
)

def make_document(index, category="Workshop", numberParticipants=False):
    
    #make empty strings for the empty documents
    if category == "Empty":
        doc = canvas.Canvas("Workshop2025_"+str(index+1)+".pdf", pagesize=portrait(A4))
        workshopname = " "
        category = " "
        firstname = " "
        lastname = " "
        languages = " "
        prerequisites = " "
        participants = " "+" "+" "+" "
        description = " "
    elif category == "Children":
        workshopname = "Kinderkurs"
        category = " "
        firstname = " "
        lastname = " "
        languages = " "
        prerequisites = "Keine / None"
        participants = " "+" "+" "+" "
        description = " "
        doc = canvas.Canvas("Workshop2025_Kinderkurs.pdf", pagesize=portrait(A4))
    #usual workshop data
    else:
        doc = canvas.Canvas("Workshop2025_"+str(index+1)+".pdf", pagesize=portrait(A4))
        workshopname = workshops['Task Name'][index]
        category = workshops['Category (labels)'][index].strip("[]")
        firstname = workshops['Vorname (short text)'][index]
        lastname = workshops['Nachname (short text)'][index]
        languages = workshops['Language (labels)'][index].strip("[]")
        prerequisites = workshops['Student Requirements (drop down)'][index]
        participants = str(workshops['Maximum Number of Participants (number)'][index])
        numberParticipants = workshops['Maximum Number of Participants (number)'][index]
        description = workshops['Short Discription (text)'][index]
    
    #formatting and creating of pdf document
    #doc = canvas.Canvas("Workshop2025_"+str(index)+"_ohneHintergrund.pdf", pagesize=portrait(A4)) 
    

    if len(workshopname) > 50:
        doc.setFont('OSBold', 20)
        wraped_workshopname ="\n".join(wrap(workshopname, 36))
    else:
        doc.setFont('OSBold', 25)
        wraped_workshopname ="\n".join(wrap(workshopname, 30))
    
    tname = doc.beginText()
    tname.setTextOrigin(57, 740)
    tname.textLines(wraped_workshopname)
    doc.drawText(tname)
    
    doc.setFont('OSBold', 10)
    doc.drawString(57, 771, "Kategorie / Category:")
    doc.setFont('OSBold', 13)
    doc.drawString(57, 683, "Instructor/in:")
    doc.drawString(57, 665, "Sprache / Language:")
    doc.drawString(57, 630, "Tag / Day:")
    doc.drawString(57, 610, "Uhrzeit / Time:")
    doc.drawString(57, 580, "Voraussetzung / Prerequisite:")
    doc.drawString(57, 523, "Beschreibung / Description:")
    doc.drawString(57, 417, "Teilnehmende / Participants:")
    
    doc.setFont('OS', 10)
    doc.drawString(170, 771, category)
    doc.setFont('OS', 13)
    doc.drawString(150, 683, firstname+" "+lastname)
    
    doc.drawString(195, 665, languages)

    if prerequisites == 'Other':
        wraped_prerequ ="\n".join(wrap(workshops['Detailed Student Requirements (text)'][index], 80))
        tpre = doc.beginText()
        tpre.setTextOrigin(60, 560)
        tpre.textLines(wraped_prerequ)
        doc.drawText(tpre)
    elif str(prerequisites) == "nan":
        doc.drawString(60, 560, "Keine / None")
    else:
        doc.drawString(60, 560, str(prerequisites))
    
    doc.drawString(250, 417, "(max. "+participants+")")
    
    #text with line breaks
    wraped_description ="\n".join(wrap(description, 70))
    t = doc.beginText()
    t.setTextOrigin(60, 503)
    t.textLines(wraped_description)
    doc.drawText(t)
    
    #lines for participants
    for j in range(0, numberParticipants): 
        
        #move things to second column if more than 8 lines
        k = 0
        l = 0
        if j > 7 :
            k = 260 # move to right
            l = -8*40 # move up
        
        doc.drawString(60+k, 380-j*40-l, str(j+1))
        doc.line(80+k, 380-j*40-l, 270+k, 380-j*40-l)

    #add logo
    doc.drawInlineImage("Logo.png", 450, 710, width = 1.58*70, height = 1.30*70)
    
    #save
    doc.save()

    
#loop through all workshops
for i in range(0, len(workshops.index)):
    make_document(i)
#create empty document
make_document(-1, category="Empty", numberParticipants=8)
make_document(-1, category="Children", numberParticipants=12)
