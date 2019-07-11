# ******************************************
#  Author : Ali Azhari
#  Created On : Sat Jun 29 2019
#  File : test1.py
# *******************************************/

import tabula as tb
import numpy as np

data = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]]

print('plain data')
print(data)

dataarray = np.array(data)
print('dataarray')
print(dataarray)

datat = np.array(data).T

print('transport')
print(datat)

# readinf the PDF file that contain Table Data
# you can find find the pdf file with complete code in below
# read_pdf will save the pdf table into Pandas Dataframe

# df = tb.read_pdf("bacc.pdf")
# df = tb.read_pdf('bacc.pdf', pages='all')


# in order to print first 5 lines of Table
# print(df.head())
# print(len(df))


# import PyPDF2
# # pdf file object
# # you can find find the pdf file with complete code in below
# pdfFileObj = open('bacc.pdf', 'rb', ,encoding = "utf-8")
# # pdf reader object
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# # number of pages in pdf
# print(pdfReader.numPages)
# # a page object
# pageObj = pdfReader.getPage(0)
# # extracting text from page.
# # this will print the text you can also save that into String
# print(pageObj.extractText())
