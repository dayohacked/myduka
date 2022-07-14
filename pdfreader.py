from csv import reader
import PyPDF2
pdf = open("python_beginners.pdf","rb")
reader = PyPDF2.PdfFileReader(pdf)
page1 = reader.getPage([])
page = reader.get_object()
for i in page:
    print(i)
print(page.extractText())