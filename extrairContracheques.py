from PyPDF2 import PdfFileReader, PdfFileWriter

pdf_document = "pdfs/HoleriteCompleto.pdf"

with open(pdf_document, "rb") as filehandle:
    pdf = PdfFileReader(filehandle, strict=False)
    info = pdf.getDocumentInfo()
    pages = pdf.getNumPages()
    employeeNameCompare = ''

    EMPLOYEE_NAME_STEPS = 5
    MONTH_AND_EMPLOYEEID_STEPS = 4
    CNPJ = '98.765.432/0001-98'

    for page in range(pdf.getNumPages()):
        current_page = pdf.getPage(page)
        contentPage = current_page.extractText()
        contentPageParse = contentPage.split(" ")

        cnpjIndex = contentPageParse.index('CIC\n' + CNPJ)
        monthAndEmployeeID = contentPageParse[cnpjIndex + MONTH_AND_EMPLOYEEID_STEPS].replace("\n", " ").split(" ")
        employeeName = contentPageParse[cnpjIndex + EMPLOYEE_NAME_STEPS]
        monthCurrentPayment = monthAndEmployeeID[0].replace("/", "-").upper()
        employeeID = monthAndEmployeeID[1]
        
        if (employeeNameCompare != employeeName):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(current_page)
            current_page2 = current_page
            outputFilename = "extraidos/holerite/{}-{}-{}_CONTRACHEQUE.pdf".format(employeeID, employeeName, monthCurrentPayment)
            with open(outputFilename, "wb") as out:
                pdf_writer.write(out)
                print("Arquivo gerado: " + employeeID +"-"+ employeeName +"-"+ monthCurrentPayment +"_CONTRACHEQUE.pdf")
                employeeNameCompare = employeeName
        else:
            outputFile = open(outputFilename, 'wb')
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(current_page2)
            pdf_writer.addPage(current_page)
            pdf_writer.write(outputFile)
            employeeNameCompare = ''