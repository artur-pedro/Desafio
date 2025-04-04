import os
import requests
from tools import PDFDownloader, PDFConverter, FileManager


def main():
    url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos" # Link do site 
    pdf_name = "Anexo I.pdf" # Nome que o pdf será salvado
    arquivo_csv_name = "Anexo_I.csv" # Nome que o arquivo .csv será salvo
    arquivo_zip_name = "Teste_Pedro_Artur.zip" # Nome que o arquivo zipado será salvo
    nome_comum = "Anexo I" # Nome comum aos pdfs que serão baixados da url passada
    nome_pasta = "Desafio2_resultados" # Nome da pasta onde os arquivos serão salvos
    quantidade_de_pdfs = 1 # Quantidade de pdfs a serem baixados da url 
    arquivos_baixados = [] # array que salvará o endereço dos arquivos baixados, para possível remoção ou outras operaçõs no futuro

    try:
        
        downloader = PDFDownloader(url_base, quantidade_de_pdfs, url_base, nome_comum) # Instaciar objeto da classe PDFDownloader que possui as funções de download de pdfs
        manager = FileManager(nome_pasta, arquivos_baixados) # Instaciar objeto da classe FileManager que possui as funçõs de gerenciamento de arquivos
        
        manager.verificar_existencia(nome_pasta) # Verificar a existência da pasta onde os arquivos finais serão salvos
        
        caminho_pasta = manager.criar_e_acessar_pasta() # Criando a pasta onde os arquivos serão salvos

        pdf_path = os.path.join(caminho_pasta, pdf_name) # caminho que o pdf será salvo
        
        csv_path = os.path.join(caminho_pasta, arquivo_csv_name) # caminho que o csv será salvo
        
        converter = PDFConverter(pdf_path, csv_path) # instaciando o objeto para converter pdf em csv no futuro 

        # Buscar e baixar PDFs
        arquivos_baixados = downloader.buscar_e_baixar_pdfs(arquivos_baixados, pasta_temp=caminho_pasta) # Baixando  o pds e adicionando o endereço ao array, para remoção futura

        # Verificar se o PDF realmente existe antes da conversão
        if os.path.exists(pdf_path):
            arquivos_baixados = converter.pdf_para_csv(arquivos_baixados) # fazendo a conversão de pdf para csv e adicionando o endereço do csv ao array
            # Criar ZIP do CSV
            caminho_zip = os.path.join(caminho_pasta, arquivo_zip_name) # caminho para salvar o arquivo zip
            manager.csv_para_zip(csv_path, caminho_zip) # gerando o arquivo zipado
        else:
            print(f"Erro: O arquivo {pdf_path} não foi baixado corretamente.")
        manager.apagar_arquivos(arquivos_baixados) # apagando os arquivos .csv e .pdf e deixando somente o zipado
        
        

    except requests.RequestException as e:
        print(f"Erro ao acessar {url_base}: {e}")

if __name__ == "__main__":
    main()
