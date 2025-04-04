import os
import pdfplumber
import csv
import zipfile

class PDFConverter:
    def __init__(self, caminho_pdf, caminho_csv):
        self.caminho_pdf = caminho_pdf
        self.caminho_csv = caminho_csv  

    def pdf_para_csv(self, arquivos_baixados): # Função para converter um arquivo PDF para CSV extraindo tabelas e substitui abreviações.
        if not os.path.exists(self.caminho_pdf):
            print(f"Erro: O arquivo '{self.caminho_pdf}' não foi encontrado.")
            return False
        
        try:
            with pdfplumber.open(self.caminho_pdf) as pdf, open(self.caminho_csv, 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.writer(arquivo_csv)
                primeira_pagina = True

                for pagina in pdf.pages:
                    tabela = pagina.extract_table()
                    if tabela:
                        # Substituir abreviações na tabela
                        tabela_modificada = []
                        for linha in tabela:
                            linha_modificada = [
                                celula.replace("OD", "Seg. Odontológica").replace("AMB", "Seg. Ambulatorial") if celula else celula
                                for celula in linha
                            ]
                            tabela_modificada.append(linha_modificada)

                        # Escrevendo no CSV
                        if primeira_pagina:
                            escritor.writerow(tabela_modificada[0])  # Escreve o cabeçalho
                            primeira_pagina = False
                        escritor.writerows(tabela_modificada[1:])

                print(f"Conversão concluída: {self.caminho_csv}")
                
            arquivos_baixados.append(self.caminho_csv) 
            
            ''' Adiciona o endereço do csv ao array de arquivos 
            baixados para possível exclusão no futuro, ou outra operação'''
            
            return arquivos_baixados
        except Exception as e:
            print(f"Erro ao processar o PDF: {e}")
            return False
        
    def csv_para_zip(caminho_csv, caminho_zip): # Função para compactar um arquivo csv em .zip"
        if not os.path.exists(caminho_csv):
            print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
            return False

        try:
            with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(caminho_csv, os.path.basename(caminho_csv))
            print(f"Arquivo ZIP criado com sucesso: {caminho_zip}")
            return True
        except Exception as e:
            print(f"Erro ao criar o ZIP: {e}")
            return False

