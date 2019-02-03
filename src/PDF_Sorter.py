#!/usr/bin/python3

"""
A Python tool for appropriate sort of PDF Files collection.
See README for links to FAQ, documentation, homepage, etc.
"""

__author__ = "J0MS"
__author_email__ = "passwd@ciencias.unam.mx"


import os
import sys
import logging
import threading
from pdfrw import PdfReader
from PyPDF2 import PdfFileReader

logging.basicConfig(level=logging.INFO, format='[%(levelname)s](%(threadName)-s) %(message)s')

programName = "PDF_Sorter"
programVersion = "1.0"
licenseVersion = " GNU v 3.0"
homepageProyect = "https://github.com/J0MS/PDF_Sorter"
programName.__repr__()
"Version".__repr__()
#print(programName,"\n" ,"Version", programVersion,"\n" ,"license",licenseVersion,"\n" ,"Homepage:",homepageProyect)
#python3 -c "import PyPDF2; print(PyPDF2.__version__)"

list_of_all_PDFs = []
list_new_names = []
max_long_title = 60
list_of_paths= []
#verboseMode = False
n_changed_pdfs = 0
n_total_pdfs = 0

#Colors for console output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def getTitle(aPDF):
    #logging.info("Method getTitle for:" + str(aPDF))
    title = " "
    temp_PDF = PdfReader(aPDF)
    if temp_PDF.isEncrypted:
        temp_PDF._override_encryption = True
        temp_PDF.decrypt('')
    title = temp_PDF.Info.Title
    return title

def getPubDate(aPDF):
    #logging.info("Method getPubDate for:" + str(aPDF))
    publication_date = " "
    temp_PDF = PdfFileReader(open(aPDF, "rb"))
    if temp_PDF.isEncrypted:
        temp_PDF._override_encryption = True
        temp_PDF.decrypt('')
    pdf_info = temp_PDF.getDocumentInfo()
    for key,val in pdf_info.items():
        if key == '/CreationDate':
            if str(type(val))[8:39] != 'PyPDF2.generic.TextStringObject' or key == " ":
                publication_date = "No_Year"
            else:
                publication_date = val[:6]
                publication_date = publication_date[2:]
    if publication_date == " ":
        publication_date = "No_Year"
    return publication_date

def getPDFIntrospection(aPDF):
    #logging.info("Method getPDFIntrospection for:" + str(aPDF))
    content = " "
    pdf = open(aPDF, 'rb')
    reader = PdfFileReader(pdf)
    if reader.isEncrypted:
        reader._override_encryption = True
        reader.decrypt('')
    content = reader.getPage(0).extractText() + "\n"
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    pdf.close()
    return content

isascii = lambda s: len(s) == len(s.encode())

def renameFileToPDFTitle(aPDFList,aOutputMode,dst):
    #logging.info("Method renameFileToPDFTitle for:" + str(aPDFList))
    n_changed_pdfs = 0
    i = 0
    for pdf in aPDFList:
        try:
            NoneType = type(None)
            newName = " "
            name = str(getTitle(pdf))
            if isinstance(getTitle(pdf), NoneType):
                date = getPubDate(pdf)
                name = getPDFIntrospection(pdf)[:55]
                newName = str(date)+ "_"+ str(name)
            elif not isascii(name):
                print (bcolors.FAIL + "Non ASCII Char(s) in this file." + bcolors.FAIL +chr(27)+"[0m")
                date = getPubDate(pdf)
                name = getPDFIntrospection(pdf)[:55]
                newName = str(date)+ "_"+ str(name)
            else:
                newName = str(getPubDate(pdf)) + "_"+ str(getTitle(pdf))
            newName = newName[:max_long_title] + ".pdf"
            formerName = os.path.join(dst, pdf)
            newName = newName.replace("-", "_")
            newName = newName.replace(" ", "_")
            newName = newName.replace("(", "" )
            newName = newName.replace(")", "" )
            newName = newName.replace("/", "_")
            newName = newName.replace("”", "_")
            newName = os.path.join(dst, newName)

            if pdf != newName:
                os.rename(formerName,newName)
                list_new_names.append(newName)
                if aOutputMode:
                    print (pdf[len(dst):] + bcolors.OKGREEN + " changed to " + bcolors.OKGREEN + chr(27)+"[0m" + newName[len(dst):] )

        except TypeError:
            print("TypeError")

def printHelp():
    print(programName,"\n" ,"Version", programVersion,"\n" ,"license",licenseVersion,"\n" ,"Homepage:",homepageProyect)
    print("Usage: python3 PDF_Sorter.py [OPTION] ... [FILE]")
    print(" ")
    print("If path to files constains blank spaces, add", "\\", " to blank spaces, example:"  )
    print( "/folder X/files.pdf must be -> ", "folder\\","X/files.pdf")
    comands = """
        -v, --version
        -h, --help
        -s  --silent mode (For no verbose output.)
    """
    print(comands)

def printVersion():
    print("PDF_Sorter Version", programVersion,)

def flags(x):
    return {
        '-h': "--help",
        '-s': "--silent",
        '-v': "--version"
    }#.get(x, 9)


def get_List_of_pdfFiles(aPath):
    #logging.info("Method get_List_of_pdfFiles for:" + str(aPath))
    cwd = aPath
    list_of_Files = os.listdir(cwd)
    list_of_PDFs = []
    if os.path.isdir(cwd):
        for file in list_of_Files:
            if ".pdf" in file:
                list_of_all_PDFs.append(file)
                list_of_PDFs.append(cwd+file)
    else:
        sys.exit("No valid path.")
    return list_of_PDFs



def rename_list_of_files(aPath,aOutputMode):
    #logging.info("Method rename_list_of_files for:" + str(aPath))
    renameFileToPDFTitle(get_List_of_pdfFiles(aPath),aOutputMode,aPath)

def main(args):
    path = ""
    if len(args) < 2:
        sys.exit("No arguments!")
    else:
        flag = sys.argv[1]
        if flag in flags(flag):
            if flag == "-h":
                printHelp()
            elif flag == "-v":
                printVersion()
            elif flag == "-s":
                verboseMode = False
                index = 0
                for path in sys.argv[2:]:
                    index += 1
                    rename_list_of_files(path,verboseMode)

        else:
            verboseMode = True
            index = 0
            for path in sys.argv[1:]:
                index += 1
                rename_list_of_files(path,verboseMode)


    print('PDF(s) found:', len(list_of_all_PDFs), 'PDF(s) changed:',len(list_new_names) )

if __name__=='__main__':
    main(sys.argv)
