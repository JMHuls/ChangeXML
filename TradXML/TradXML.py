'''
Created on 29 nov. 2018

@author: JHuls
'''
import sys
import ctypes
import xml.etree.ElementTree as ET
from PyQt4.QtGui import *

# Defanitions
def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

# Create a PyQt4 application and widget
a = QApplication(sys.argv)
w = QWidget()

# Set window
w.resize(320, 240)
w.setWindowTitle("Open XML")

# Get filename
File = QFileDialog.getOpenFileName(w, 'Open XML', '/')
if len(File) > 0:
    if str(File).lower().endswith('.xml'):
        # Open original file
        tree = ET.parse(File)
        root = tree.getroot()
        i = 0
        c = 0
        
        # Edit file
        for ibis in root.iter('TradbegrotingIbis'):
            ibis.tag = str('Tradbegroting4')
            i = i + 1
            
        for check in root.iter('Tradbegroting4'):
            c = c + 1
        
        # Write back to file
        #tree.write(File, encoding="utf-8", xml_declaration=True)
        tree.write(File)
        
        line_prepender(File, '<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
        
        if i >= 1:
            if i == 1:
                Mbox(u'XML aangepast', u'Conversie gelukt, de XML kan ingelezen worden in BouwVision', 0)
            else:
                Mbox(u'XML niet aangepast', u'Conversie mislukt', 0)
        else:
            if c >= 1:
                Mbox(u'XML niet aangepast', u'DeXML lijkt al correct te zijn en zou in BouwVision ingelezen moeten kunnen worden', 0)
            else:
                Mbox(u'XML niet aangepast', u'Ongeldige XML ingevoerd', 0)
    else:
        Mbox(u'Open XML', u'Geen XML-bestand gekozen', 0)
else:
    Mbox(u'Open XML', u'Geen bestand gekozen', 0)
    
#sys.exit(a.exec_())
sys.exit()
