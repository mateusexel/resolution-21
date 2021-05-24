import io
import glob
import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFEncryptionError, PDFSyntaxError
from Crypto.Cipher import AES
import os
import sys, getopt
import pandas as pd
import re
from docx import Document
import os


def convert_doc(path):
    os.chdir(path)
    os.system('lowriter --convert-to docx *.doc')
    os.system('lowriter --convert-to docx *.DOC')
    os.system('rm *.doc')
    os.system('rm *.DOC')


def convertpdf(fname):
    pagenums = set()
    output = io.StringIO()
    manager = PDFResourceManager()
    laparams = LAParams()
    password = "''"

    converter = TextConverter(manager, output, laparams=laparams)
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')

    for page in PDFPage.get_pages(infile, pagenums, password=password, check_extractable=False):
        interpreter.process_page(page)

    infile.close()
    converter.close()
    text = output.getvalue()

    output.close()
    return text


def convertdocx(f_name):
    text = ''
    document = Document(f_name)
    for para in document.paragraphs:
        text += str(para.text) + '/n'
    return text


def convertmultiple(filedir, txtdir):
    all_files = [".".join(f.split(".")[:-1]) for f in os.listdir(filedir)]
    converted_files = [".".join(f.split(".")[:-1]) for f in os.listdir(txtdir)]
    not_converted_files = [f for f in all_files if f not in converted_files]

    files_list = glob.glob(filedir + "/*")

    for file_name in not_converted_files:  # iterate through pdfs in pdf directory

        full_file_name = [s for s in files_list if file_name in s][0]
        fileExtension = full_file_name.split(".")[-1]

        if fileExtension.lower() == "pdf":

            try:
                text = convertpdf(full_file_name)

            except PDFEncryptionError as e:
                command = f"qpdf --password={''} --decrypt {full_file_name} {full_file_name[:-4]}D.pdf;"
                os.system(command)
                text = convertpdf(full_file_name[:-4] + 'D.pdf')

            except PDFSyntaxError:
                print('PDFSyntaxError')
                next

        elif fileExtension == "docx":

            text = convertdocx(full_file_name)

        else:
            print(fileExtension)
            next

        textFilename = txtdir + file_name + ".txt"
        textFile = open(textFilename, "w")

        textFile.write(text)
        textFile.close()
