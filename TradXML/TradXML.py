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

#  Specify tags
RightTag = 'Tradbegroting4'
WrongTag = 'TradbegrotingIbis'

# Create a PyQt4 application and widget
a = QApplication(sys.argv)
w = QWidget()

# Set window
w.resize(320, 240)
w.setWindowTitle("Open XML")

# Get filename
File = QFileDialog.getOpenFileName(w, 'Open XML', '/')
if len(File) > 0:
    # If file is a XML
    if str(File).lower().endswith('.xml'):
        # Check if original file isn't corrupt
        try:
            tree = ET.parse(File)
        except:
            Mbox(u'XML niet aangepast', u'Corrupte XML ingevoerd', 0)
            sys.exit()
            
        # Open original file
        tree = ET.parse(File)
        root = tree.getroot()
        i = 0
        c = 0
        
        # Check tags
        for check in root.iter(RightTag):
            c = c + 1
        
        # If RightTag is found
        if c >= 1:
            Mbox(u'XML niet aangepast', u'De XML lijkt al correct te zijn en zou in BouwVision ingelezen moeten kunnen worden', 0)
        # If RightTag is not found
        else:
            # Count and change tags, do not write to file yet
            for ibis in root.iter(WrongTag):
                ibis.tag = str(RightTag)
                i = i + 1
            
            if i >= 1:
                if i == 1:
                    # Write back to file if file and tags are confirmed
                    tree.write(File)
                    line_prepender(File, '<?xml version="1.0" encoding="utf-8" standalone="yes"?>')
                    Mbox(u'XML aangepast', u'Conversie gelukt, de XML kan ingelezen worden in BouwVision', 0)
                else:
                    Mbox(u'XML niet aangepast', u'Conversie mislukt', 0)
            else:
                Mbox(u'XML niet aangepast', u'Ongeldige XML ingevoerd', 0)
    else:
        Mbox(u'Open XML', u'Geen XML-bestand gekozen', 0)
else:
    Mbox(u'Open XML', u'Geen bestand gekozen', 0)
    
# Stop this script
sys.exit()
