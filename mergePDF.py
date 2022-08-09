from PyPDF2 import PdfFileMerger
import os

refeicoes = []
holerites = []

path_to_files = r'extraidos/'
for root, dirs, file_names in os.walk(path_to_files):
    for file_name in file_names:
        tempName = file_name.split('_')
        folder = tempName[1].replace('.pdf','')
        employee = tempName[0]
        
        if folder == 'REFEICAO':
            refeicoes.append(employee)
        else:
            holerites.append(employee)

for holerite in holerites:
    if holerite in refeicoes:
        merger = PdfFileMerger()
        merger.append('extraidos/holerite/' + holerite + '_CONTRACHEQUE.pdf')
        merger.append('extraidos/refeicao/' + holerite + '_REFEICAO.pdf')
        merger.write('merged/' + holerite + '.pdf')
        print('merged/' + holerite + '.pdf')
        merger.close()