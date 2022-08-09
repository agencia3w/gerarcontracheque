from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import os, shutil

PATH_CONTRACHEQUE = 'extraidos/holerite/'
PATH_REFEICAO = 'extraidos/refeicao/'
PATH_CONTRACHEQUE_REFEICAO = 'contracheque_refeicao/'
FOLDER_REFEICAO = 'REFEICAO'
PDF_CONTRACHEQUE = 'pdfs/HoleriteCompleto.pdf'
PDF_REFEICAO = 'pdfs/Refeicao.pdf'
CNPJ = '98.765.432/0001-98'

if not os.path.exists(PDF_CONTRACHEQUE) or not os.path.exists(PDF_REFEICAO):
    print('VERIFIQUE SE EXISTEM OS ARQUIVOS: ' + PDF_CONTRACHEQUE + ', ' + PDF_REFEICAO)
    exit()

paths = [PATH_CONTRACHEQUE, PATH_REFEICAO, PATH_CONTRACHEQUE_REFEICAO]

for pathItem in paths:
    if not os.path.exists(pathItem):
        os.makedirs(pathItem)

print('### CONTRACHEQUES')
with open(PDF_CONTRACHEQUE, "rb") as filehandle:
    pdf = PdfFileReader(filehandle, strict=False)
    info = pdf.getDocumentInfo()
    pages = pdf.getNumPages()
    employeeNameCompare = ''

    EMPLOYEE_NAME_STEPS = 5
    MONTH_AND_EMPLOYEEID_STEPS = 4

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
            outputFilename = PATH_CONTRACHEQUE + "{}-{}-{}_CONTRACHEQUE.pdf".format(employeeID, employeeName, monthCurrentPayment)
            with open(outputFilename, "wb") as out:
                pdf_writer.write(out)
                print("Arquivo temporario gerado: " + employeeID +"-"+ employeeName +"-"+ monthCurrentPayment +"_CONTRACHEQUE.pdf")
                employeeNameCompare = employeeName
        else:
            outputFile = open(outputFilename, 'wb')
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(current_page2)
            pdf_writer.addPage(current_page)
            pdf_writer.write(outputFile)
            employeeNameCompare = ''

# Extrair Refeição
print('\n### REFEICAO')

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

with open(PDF_REFEICAO, "rb") as filehandle:
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

        outputFilename = PATH_REFEICAO + "{}-{}-{}_REFEICAO.pdf".format(employeeID, employeeName, monthCurrentPayment)
        with open(outputFilename, "wb") as out:
            pdf_writer.write(out)
            print("Arquivo temporario gerado: " + employeeID +"-"+ employeeName +"-"+ monthCurrentPayment +"_REFEICAO.pdf")

# Juntar arquivos
print('\n### CONTRACHEQUE/REFEICAO')

refeicoes = []
holerites = []

path_to_files = r'extraidos/'
for root, dirs, file_names in os.walk(path_to_files):
    for file_name in file_names:
        tempName = file_name.split('_')
        folder = tempName[1].replace('.pdf','')
        employee = tempName[0]
        
        if folder == FOLDER_REFEICAO:
            refeicoes.append(employee)
        else:
            holerites.append(employee)

for holerite in holerites:
    if holerite in refeicoes:
        merger = PdfFileMerger()
        merger.append(PATH_CONTRACHEQUE + holerite + '_CONTRACHEQUE.pdf')
        merger.append(PATH_REFEICAO + holerite + '_REFEICAO.pdf')
        merger.write(PATH_CONTRACHEQUE_REFEICAO + holerite + '.pdf')
        print(PATH_CONTRACHEQUE_REFEICAO + holerite + '.pdf')
        merger.close()

# Excluir pasta extraidos
shutil.rmtree(path_to_files, ignore_errors=True)