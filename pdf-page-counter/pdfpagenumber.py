#!/usr/bin/env python3

#
# Filename: pdfpagenumber.py
#
# Author: Thomas Grasse
# Created on: Tue Feb 15 2021
#
# Copyright (c) 2021 Exercim Oy
#

'''This module determines the total number of pages in a PDF document. The passed docunent can 
be of any format and might contain several PDF documents. As an example, a print stream file (PRN) created by a printer 
driver might contain several PDFs. This script determines the number of PDF pages of all enclosed PDF documents.'''

import sys
import re
from argparse import ArgumentParser
import logging

#if __name__ == "__main__":
logHandler = logging.StreamHandler( sys.stdout )
logFormatter = logging.Formatter( 
    '[{levelname:4}] {asctime} {funcName} Line {lineno}: {message}',
    datefmt= r'%d.%m.%Y %H:%M:%S',
    style='{' )
logHandler.setFormatter( logFormatter )
logHandler.setLevel( logging.DEBUG )
log = logging.getLogger()
log.addHandler( logHandler )
log.setLevel( logging.DEBUG )

REGEX_COUNT = b'/Count [0-9]+'
REGEX_PDF = b'%PDF\-.+?(?=%PDF\-|\Z)'
VERSION = "1.1"

def LogIt( func ):
    def log_wrapper( id, source ):
        log.info( f"{func.__name__} started with argument: {id}." )
        log.debug( f"{func.__name__} source: {source}." )
        rv = func( id, source )
        log.info( f"{func.__name__} finished with result: {rv}." )
        return rv
    return log_wrapper

@LogIt
def extractObject( objectId, source ):
    '''This function searches the object with the object id objectId within source and returns
    a String representation of the found object.'''

    regex = b'\s' + objectId + b' obj.+?endobj'
    m = re.search( regex, source, re.DOTALL  )
    log.debug( f"extractObject match object: {m}." )
    if m == None:
        log.error( 'extractObject match object is None-Type.')
        return None
    rv = m.string[m.start():m.end()]
    assert rv != None, f"Object was null. Tag: {objectId}."
    assert len( rv ) > 7, f"Object string is too short. Found tag link: {rv}."
    return rv

@LogIt
def extractLinkIdFromTag( tagId, source ):
    '''This function searches for a tag with the id tagId within source. The function assumes, 
    that the found tag is of type of a link tag. Successively, the function extracts the link id 
    from the tag and returns it.'''

    regex = tagId + b' +[0-9]+ +[0-9]+ +R'
    m = re.search( regex, source, re.DOTALL )
    log.debug( f"extractLinkIdFromTag match object: {m}." )
    if m == None:
        log.error( 'extractLinkIdFromTag match object is None-Type.')
        return None
    rv = m.string[m.start():m.end()].lstrip(tagId).rstrip(b'R').strip()
    assert rv != None, f"Tag link was null. Tag: {tagId}."
    assert len( rv ) > 2, f"Tag Link string is too short. Found tag link: {rv}."
    return rv

def extractPdfPageCount( filepath ):
    '''This function extratcs the number of PDF pages in a document.'''

    with open(filepath, 'rb') as f: #if open fails, the exception is bubbled up to the command line
        assert f != None, f"File error while opening file {filepath}."
        fileContent = f.read()
        log.debug( f"File has been read: {fileContent}." )

    # Extract list of pdf documents
    pdfDocuments = re.findall(REGEX_PDF, fileContent, re.DOTALL)
    if len(pdfDocuments) < 1:
        log.error( f"Document does not contain PDF files: {fileContent}." )
        print( f"Document does not contain PDF files: {fileContent}." )
        sys.exit( -1 )

    documentPageCount = 0 #accumulates the number of pages in file

    # for each pdf search page count tag
    for pdf in pdfDocuments:
        log.debug( f"PDF extracted: {pdf}." )

        # Find root tag and extract catalog id
        catalogId = extractLinkIdFromTag( b'/Root', pdf )

        # Find catalog object and extract page tree root id
        catalog = extractObject( catalogId, pdf )
        pageTreeRootId = extractLinkIdFromTag( b'/Pages', catalog )

        #Find page tree root object and extract page count tag
        pageTreeRoot = extractObject( pageTreeRootId, pdf )
        log.info( f"Page tree root found: {pageTreeRoot}." )
        m = re.search( REGEX_COUNT, pageTreeRoot, re.DOTALL  )
        log.debug( f"Count tag search match object: {m}." )
        if m == None:
            log.error( f"Count Tag search match object is None-Type for page tree root object: {pageTreeRoot}." )
        assert m != None, f"Count tag not found in page tree root object: {pageTreeRootId}."

        pageCount = m.string[m.start():m.end()].lstrip(b'/Count').rstrip(b'R').strip()
        assert pageCount != None, f"Page count was null. Object: {pageTreeRoot}."
        assert len( pageCount ) > 0, f"Page count string is too short. Found page count: {pageCount}."
        log.info( f"Page count found: {pageCount}." )

        documentPageCount += int(pageCount)      

    log.debug ( f"Document: {f}." )
    log.info( f"Document page count: Document: {fileLocation}, Count: {documentPageCount}.")
    return documentPageCount


# Here starts the main program of the module

if __name__ == "__main__":
    parser = ArgumentParser(  prog='PDF Page Counter',
        description = '''Determines the total number of pages in a PDF document. The passed docunent can
        be of any format and might contain several PDF documents. As an example, a print stream file (PRN) created by a printer 
        driver might contain several PDFs. This script determines the number of PDF pages of all enclosed PDF documents.''',
        epilog = '(c) 2021 Exercim Oy',
        add_help = True )
    parser.add_argument( 'filepathList',
        nargs='+',
        help = 'Location of the PDF file(s) to process.',
        metavar = 'Filepath' )
    parser.add_argument( 
        '-v',
        action='count',
        default= 0,
        #type= int,
        #choices= range(0, 3),
        help= 'Set the verbosity of the function logging. Possible values are: none, -v, -vv.',
        dest= 'verbose')
    parser.add_argument(
        '--verbose',
        action='store',
        default=0,
        type= int,
        choices= range(0, 3),
        help= 'Set the verbosity of the function logging. 0 is default.',
        dest= 'verbose')
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.1.0'
    )
    args = parser.parse_args()
    log.debug( f"Parsed command line arguments: {args}." )
    logLevels = {
        0: logging.ERROR,
        1: logging.INFO,
        2: logging.DEBUG
    }
    log.setLevel( logLevels[args.verbose])
    #log.setLevel( logging.DEBUG )

    totalPageCount = 0 # accumulates the end result

    for fileLocation in args.filepathList:
        totalPageCount += extractPdfPageCount( fileLocation )

    log.info( f"Total page count: {totalPageCount}." )

    #help(__name__)
    print( f"{totalPageCount}" )
    sys.exit( totalPageCount )
