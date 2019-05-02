import os
import PyPDF2
from create_pdf_files import get_pdf_filenames


# def get_files_names():
#
#     with open('pdf_file_list.txt', 'r') as pdf_list:
#         filenames = [file.strip() for file in pdf_list.readline().split(',') if not file.isspace()]
#     return filenames

os.chdir('/Users/MasonBaran/PycharmProjects/bepress_import_create')

def create_pdf_minus_cover_page(filename):
    print('body_grab/{0}-transcript.pdf'.format(filename))
    pdfIn = open('body_grab/{0}-transcript.pdf'.format(filename), 'rb')

    pdfReader = PyPDF2.PdfFileReader(pdfIn)
    pdfWriter = PyPDF2.PdfFileWriter()

    for pageNum in range(1, pdfReader.getNumPages()):
        page = pdfReader.getPage(pageNum)
        pdfWriter.addPage(page)

    pdfOut = open('body_grab/content_only3/{}-contents.pdf'.format(filename), 'wb')
    pdfWriter.write(pdfOut)

    pdfIn.close()
    pdfOut.close()


if __name__ == '__main__':
    # to read in from .txt file
    # filenames_no_ext = get_files_names()
    ################################################################
    # to read in from create_pdf_files method
    filenames_no_ext = get_pdf_filenames()
    for file in filenames_no_ext:
        try:
            create_pdf_minus_cover_page(file)
        except FileNotFoundError:
            print('file not found for {}'.format(file))

