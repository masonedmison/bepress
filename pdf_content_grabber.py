import os
import PyPDF2


def get_files_names():

    with open('pdf_file_list.txt', 'r') as pdf_list:
        filenames = [file.strip() for file in pdf_list.readline().split(',') if not file.isspace()]
    return filenames


def create_pdf_minus_cover_page(filename):

    pdfIn = open('body_grab/{}-transcript.pdf'.format(filename), 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfIn)
    pdfWriter = PyPDF2.PdfFileWriter()

    for pageNum in range(1, pdfReader.getNumPages()):
        page = pdfReader.getPage(pageNum)
        pdfWriter.addPage(page)

    pdfOut = open('body_grab/content_only2/{}-contents.pdf'.format(filename), 'wb')
    pdfWriter.write(pdfOut)

    pdfIn.close()
    pdfOut.close()


def main():
    filenames_no_ext = get_files_names()

    for file in filenames_no_ext:
        try:
            create_pdf_minus_cover_page(file)

        except FileNotFoundError:
            print('file not found for {}'.format(file))


if __name__ == '__main__':
    main()
