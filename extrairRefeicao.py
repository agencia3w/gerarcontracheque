from PyPDF2 import PdfFileReader, PdfFileWriter

pdf_document = "pdfs/Refeicao.pdf"

months = {
    '01': 'JANEIRO',
    '02': 'FEVEREIRO',
    '03': 'MARCO',
    '04': 'ABRIL',
    '05': 'MAIO',
    '06': 'JUNHO',
    '07': 'JULHO',
    '08': 'AGOSTO',
    '09': 'SETEMBRO',
    '10': 'OUTUBRO',
    '11': 'NOVEMBRO',
    '12': 'DEZEMBRO'
}

print(months['06'])

with open(pdf_document, "rb") as filehandle:
    pdf = PdfFileReader(filehandle, strict=False)
    info = pdf.getDocumentInfo()
    pages = pdf.getNumPages()

    for page in range(pdf.getNumPages()):
        current_page = pdf.getPage(page)
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(current_page)

        contentPage = current_page.extractText()
        contentPageParse = contentPage.split(" ")
        dateIndex = contentPageParse.index('PERÍODO')
        monthCurrentPayment = contentPageParse[dateIndex + 1].split("/")
        monthCurrentPayment = months[monthCurrentPayment[1]] +"-"+ monthCurrentPayment[2]
        employeeIndex = contentPageParse.index('________________________________________________\nFuncionário.:')
        employeeID = contentPageParse[employeeIndex + 1]
        employeeName = contentPageParse[employeeIndex + 3]

        outputFilename = "extraidos/refeicao/{}-{}-{}_REFEICAO.pdf".format(employeeID, employeeName, monthCurrentPayment)
        with open(outputFilename, "wb") as out:
            pdf_writer.write(out)
            print("Arquivo gerado: " + employeeID +"-"+ employeeName +"-"+ monthCurrentPayment +"_REFEICAO.pdf")