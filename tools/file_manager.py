import os
import zipfile
import patoolib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import shutil

class FileManager:
    def __init__(self, nome_pasta, arquivos_baixados):
        self.nome_pasta = nome_pasta
        

    def verificar_existencia(self, nome_pasta): # Função para verificar a existência de uma pasta
        if os.path.exists(nome_pasta):
            if os.path.isfile(nome_pasta):
                os.remove(nome_pasta)
            else:
                shutil.rmtree(nome_pasta)
            print(f"{nome_pasta} foi removido com sucesso.")
        else:
            print(f"{nome_pasta} não existe.")
            

    def criar_zip(self, arquivo_zip, arquivos_baixados): # Função para criar um arquivo zip contendo todos os arquivos(endereços) de um array
        with zipfile.ZipFile(arquivo_zip, "w") as zipf:
            for arquivo in arquivos_baixados:
                zipf.write(arquivo, os.path.basename(arquivo))
        print(f"Arquivo ZIP criado: {arquivo_zip}")

    def csv_para_zip(self, caminho_csv, caminho_zip):
        if not os.path.exists(caminho_csv):
            print(f"Erro: O arquivo {caminho_csv} não foi encontrado.")
            return False
        try:
            import zipfile
            with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(caminho_csv, os.path.basename(caminho_csv))
            print(f"Arquivo ZIP criado com sucesso: {caminho_zip}")
            return True
        except Exception as e:
            print(f"Erro ao criar o ZIP: {e}")
            return False
        
    def criar_rar(self, arquivo_rar, arquivos_baixados): #Função para criar um arquivo rar contendo uma pasta
        patoolib.create_archive(arquivo_rar, arquivos_baixados)
        print(f"Arquivo RAR criado: {arquivo_rar}")

    def apagar_arquivos(self, arquivos_baixados): #Função para apagar um conjunto de arquivos
        for arquivo in arquivos_baixados:
            os.remove(arquivo)
            print(f"Removido: {arquivo}")

    def criar_e_acessar_pasta(self): # Função para criar e acessar uma pasta

        try:
            diretorio_pai = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho_pasta = os.path.join(diretorio_pai, self.nome_pasta)
            os.makedirs(caminho_pasta, exist_ok=True)
            print(f"Pasta criada: {caminho_pasta}")
            os.chdir(caminho_pasta)
            return caminho_pasta
        except Exception as e:
            print(f"Erro ao criar/acessar a pasta: {e}")
            return None