#!/usr/bin/env python3

#
# Filename: pdfpagenumbertest.py
#
# Author: Thomas Grasse
# Created on: Mon Feb 15 2021
#
# Copyright (c) 2021 Exercim Oy
#

import logging
import unittest
import pdfpagenumber

class PdfPageNumberTest( unittest.TestCase ):

    log = logging.getLogger()

    def testExtractObjectSuccessfully( self ):
        # given 
        object = b' 7 0 obj /jfjhve /hjefhew endobj'
        source = b'hdshdsdd %PDF-1.1  kijoweifhwefowf  fejfwe %%EOF>>><<  <<<' + object + b'jdfwe fwejfjew <<<>>> %%%EOF jt t7zjtjn '

        # test
        extractedObject = pdfpagenumber.extractObject(b'7 0', source)

        # then
        self.assertIsNotNone(extractedObject)
        self.assertEqual(object, extractedObject)
        self.assertLogs(self.log, "extractObject  finished with result: " + object.decode('ascii'))

    def testExtractObjectIdNotFound( self ):
        # given 
        object = b'obj /jfjhve /hjefhew endobj'
        source = b'hdshdsdd %PDF-1.1  kijoweifhwefowf  fejfwe %%EOF>>><<  <<<' + object + b'jdfwe fwejfjew <<<>>> %%%EOF ur56u 5r  '

        # test
        extractedObject = pdfpagenumber.extractObject(b'7 0', source)

        # then
        self.assertIsNone(extractedObject)
        self.assertLogs(self.log, "extractObject match object is None-Type.")

    @unittest.skip("Test does not work")
    def testExtractLinkSuccess( self ):
        # given 
        object = b'7 0'
        tag = b'/Root '
        source = b'hdshdsdd %PDF-1.1  kijoweifhwefowf ' + tag + object + b' R fejfwe %%EOF>>><<  <<<jdfwe fwejfjew <<<>>> %%%EOF tu5u6ru '

        # test
        extractedObject = pdfpagenumber.extractLinkIdFromTag(tag, source)

        # then
        self.assertIsNotNone(extractedObject)
        self.assertEqual(object, extractedObject)

    def testExtractLinkSuccess( self ):
        # given 
        object = b'7 0'
        tag = b'/Root '
        source = b'hdshdsdd %PDF-1.1  kijoweifhwefowf ' + tag + object + b' fejfwe %%EOF>>><<  <<<jdfwe fwejfjew <<<>>> %%%EOF tu5u6ru '

        # test
        extractedObject = pdfpagenumber.extractLinkIdFromTag(tag, source)

        # then
        self.assertIsNone(extractedObject)
        self.assertLogs(self.log, "extractLinkIdFromTag match object is None-Type.")

    def testHelp( self ):
        testResult = help( pdfpagenumber )
        self.assertIsNone(testResult)

if __name__ == "__main__":
    unittest.main()