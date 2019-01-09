#!/usr/bin/python3
import os
import sys
from pdfrw import PdfReader
from PyPDF2 import PdfFileReader

programName = "PDF_Sorter"
programVersion = "1.0"
licenseVersion = " GNU v 3.0"
homepageProyect = "https://github.com/J0MS/PDF_Sorter"
programName.__repr__()
"Version".__repr__()
#print(programName,"\n" ,"Version", programVersion,"\n" ,"license",licenseVersion,"\n" ,"Homepage:",homepageProyect)

#Colors for console output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def getTitle(aPDF):
    title = " "
    temp_PDF = PdfReader(aPDF)
    if temp_PDF.isEncrypted:
        temp_PDF._override_encryption = True
        temp_PDF.decrypt('')
    title = temp_PDF.Info.Title
    return title

def getPubDate(aPDF):
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

def renameFileToPDFTitle(aPDFList):
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
            formerName = os.path.join(cwd, pdf)
            newName = newName.replace("-", "_")
            newName = newName.replace(" ", "_")
            newName = newName.replace("(", "" )
            newName = newName.replace(")", "" )
            newName = newName.replace("/", "_")
            newName = newName.replace("”", "_")
            if pdf != newName:
                os.rename(formerName,newName)
                print (pdf + bcolors.OKGREEN + " changed to " + bcolors.OKGREEN + chr(27)+"[0m" + newName )
                list_new_names.append(pdf)

        except TypeError:
            print("TypeError")

def printHelp():
    print(programName,"\n" ,"Version", programVersion,"\n" ,"license",licenseVersion,"\n" ,"Homepage:",homepageProyect)
    print("Usage: python3 PDF_Sorter.py [OPTION] ... [FILE]")
    print("If path to files constains blank spaces, add", "\\", " to blank spaces, example:"  )
    print( "/folder X/files.pdf must be -> ", "folder\\","X/files.pdf")
    comands = """
        -v, --version
        -h, --help
        -s  --silent mode (For no verbose output.)
    """
    print(comands)


def flags(x):
    return {
        '-h': "--help",
        '-s': "--silent"
        '-v': "--version",
    }#.get(x, 9)


def main(args):
    if len(args) < 2:
        sys.exit("No arguments!")
    else:
        flag = sys.argv[1]
        if flag in flags(flag):
            print ("blah")
        else:
            print ("No blah")


        cwd = sys.argv[1]
        if os.path.isdir(cwd):
            print("COol")
        else:
            print("No Cool")


    print("Path",sys.argv[1])
    cwd = os.getcwd()
    #os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))
    if os.path.isdir('./data'):
        cwd = cwd  + '/data'
        os.chdir(cwd)
        if os.path.isdir('./pdf'):
            cwd = cwd  + '/pdf'
            os.chdir(cwd)

    list_of_Files = os.listdir(cwd)
    list_of_PDFs = []
    list_new_names = []
    n_total_pdfs = 0
    n_changed_pdfs = 0
    path = ""
    max_long_title = 60

    for file in list_of_Files:
        if ".pdf" in file:
            n_total_pdfs += 1
        #    print (file)
            list_of_PDFs.append(file)

    isascii = lambda s: len(s) == len(s.encode())



    renameFileToPDFTitle(list_of_PDFs)

    print('PDF(s) found:', n_total_pdfs, 'PDF(s) changed:',n_changed_pdfs )

if __name__=='__main__':
    main(sys.argv)
