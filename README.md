The pdf-page-counter module is used to determine the number of pages in a pdf document. The result is the total number of pages in a docuemnt, even if it is a compound document (like a printer stream file) that contains several PDF.

# Getting started
See the [Installing Packages](https://packaging.python.org/installing/) instructions in the Python Packaging User Guide on installing, upgrading and uninstalling pdf-page-counter.

Make sure you uns an up-to-date version of pip. 

Questions, comments and big reports as well as vulnerability reports can be directly submitted to teh maintainer: <thomas.grasse@exercim.com>.

# Usage

The package can be used in 2 ways. When executed as the main package with: `python3 -m pdf-page-count <filename>`. The process ends with the page count returned as the process exit code.

The package can also be imported, by using: `import pdfpagenumber`. The function `extractPdfPageCount` is used with the path to the PDF file as argument, to determine the page count.

# Licensing
The package is distributed under MIT license ([link](https://opensource.org/licenses/MIT)).
