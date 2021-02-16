#!/usr/bin/env python

#
# Filename: pdfpagenumber.py
#
# Author: Thomas Grasse
# Created on: Tue Feb 02 2021
#
# Copyright (c) 2021 Exercim Oy
#

import sys
import re

REGEX_COUNT = b'/Count [0-9]+'
REGEX_PDF = b'%PDF\-.+?%%EOF'

# Extracts an object from the PDF file strcuture
def extractObject( objectId, source ):
    regex = b'[ \n]' + objectId + b' obj.+?endobj'
    m = re.search( regex, source, re.DOTALL  )
    return m.string[m.start():m.end()]

# Extracts a pdf tag from nay pdf structure; from single object to full file
def extractLinkIdFromTag( tagId, source ):
    regex = tagId + b' +[0-9]+ +[0-9]+ +R'
    m = re.search( regex, source, re.DOTALL )
    return m.string[m.start():m.end()].lstrip(tagId).rstrip(b'R').strip()

# test Documents for Mac
sys.argv.append( '/Users/thomas/Exercim Oy/Synka - prn page number tool/Kanzlei203_NachbearbeitungSB_BAD_D_SX_1_20200915-225916_0154.prn' )
sys.argv.append( '/Users/thomas/Exercim Oy/Synka - prn page number tool/NBREG_Dortmund_S_REG_K4_DX_1_20201021-002943_1.prn' )
#sys.argv.append( '/Users/thomas/Exercim Oy/Synka - prn page number tool/NachbearbeitungSB_Dortmund_1_REG_SX_1_20201031-002710_1.prn' )sys.argv.append( '/Users/thomas/Documents/code-projects/pdf-page-counter/background_material/PDF32000_2008.pdf' )
#sys.argv.append( '/Users/thomas/Documents/code-projects/pdf-page-counter/background_material/PDF Explained.pdf' )

# Now for MS
#sys.argv.append( 'Z:\Kanzlei203_NachbearbeitungSB_BAD_D_SX_1_20200915-225916_0154.prn' )
#sys.argv.append( 'Z:\NBREG_Dortmund_S_REG_K4_DX_1_20201021-002943_1.prn' )
#sys.argv.append( 'Z:\NachbearbeitungSB_Dortmund_1_REG_SX_1_20201031-002710_1.prn' )
#sys.argv.append( 'Y:\\background_material\PDF32000_2008.pdf' )
#sys.argv.append( 'Y:\\background_material\PDF Explained.pdf' )

# check if at least one parameter was passed
if len( sys.argv ) < 2:
    print("Skript needs at least 1 parameter")
    sys.exit( -1 )

totalPageCount = 0 # accumulates the end result

for fileLocation in sys.argv[1:len(sys.argv)]:
    with open(fileLocation, "rb") as f: #if open fails, the exception is bubbled up to the command line
        fileContent = f.read()

    # Extract list of pdf documents
    pdfDocuments = re.findall( REGEX_PDF, fileContent, re.DOTALL )
    if len(pdfDocuments) < 1:
        print("Document does not contain PDF files")
        sys.exit( -1 )

    # for each pdf search page count tag
    for pdf in pdfDocuments:

        # Find root tag and extract catalog id
        catalogId = extractLinkIdFromTag( b'/Root', pdf )

        # Find catalog object and extract page tree root id
        catalog = extractObject( catalogId, pdf )
        pageTreeRootId = extractLinkIdFromTag( b'/Pages', catalog )

        #Find page tree root object and extract page count tag
        pageTreeRoot = extractObject( pageTreeRootId, pdf )
        m = re.search( REGEX_COUNT, pageTreeRoot, re.DOTALL  )
        pageCount = m.string[m.start():m.end()].lstrip(b'/Count').rstrip(b'R').strip()

        totalPageCount += int(pageCount)

sys.exit( totalPageCount )
