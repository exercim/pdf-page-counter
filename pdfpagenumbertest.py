#!/usr/bin/env python3

#
# Filename: pdfpagenumbertest.py
#
# Author: Thomas Grasse
# Created on: Mon Feb 15 2021
#
# Copyright (c) 2021 Exercim Oy
#

import unittest
import pdfpagenumber

class PdfPageNumberTest( unittest.TestCase ):

    def __init__( self ):
        self.testFiles = (
            '/Users/thomas/Exercim Oy/Synka - prn page number tool/Kanzlei203_NachbearbeitungSB_BAD_D_SX_1_20200915-225916_0154.prn',
            '/Users/thomas/Exercim Oy/Synka - prn page number tool/NBREG_Dortmund_S_REG_K4_DX_1_20201021-002943_1.prn',
            '/Users/thomas/Exercim Oy/Synka - prn page number tool/NachbearbeitungSB_Dortmund_1_REG_SX_1_20201031-002710_1.prn',
            '/Users/thomas/Documents/code-projects/pdf-page-counter/background_material/PDF32000_2008.pdf',
            '/Users/thomas/Documents/code-projects/pdf-page-counter/background_material/PDF Explained.pdf' )

    def testPdfObjectExtraction( self ):
        pdfpagenumber.extractObject
        self.assertTrue( True )

    def testPdfLinkIdExtraction( self ):
        self.assertTrue( True )

    def testHelp( self ):
        help( pdfpagenumber )


if __name__ == "__main__":
    unittest.main()