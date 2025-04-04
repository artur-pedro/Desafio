# main.py
import os
import requests
from tools import PDFDownloader, FileManager

def main():

    url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos" # URL da página que contém os PDFs
    arquivo_zip = "anexos.zip"# Nome do arquivo ZIP final
    arquivo_rar = "anexos.rar"# Nome do arquivo RAR final
    nome_comum = "Anexo"# Nome comum aos PDFs buscados para download
    nome_pasta = "Desafio1_resultados"# Nome da pasta onde os arquivos serão salvos
    quantidade_de_pdfs = 2 # Quantidade de pdfs  buscados
    arquivos_baixados = [] # array que salvará o endereço dos arquivos baixados, para possível remoção ou outras operaçõs no futuro
    

    try:
        downloader = PDFDownloader(url_base, quantidade_de_pdfs, url_base, nome_comum)  # Instacia objeto da classe PDFDownloader que possui as funções de download de pdfs
        
        manager = FileManager(nome_pasta, arquivos_baixados) # Instacia objeto da classe FileManager que possui as funçõs de gerenciamento de arquivos
        manager.verificar_existencia(nome_pasta) # Verifica a existência da pasta onde os arquivos finais serão salvos
        
        caminho_pasta = manager.criar_e_acessar_pasta() # Criando a pasta onde os arquivos serão salvos
        
        arquivos_baixados = downloader.buscar_e_baixar_pdfs(arquivos_baixados, pasta_temp=caminho_pasta) # Baixando  o pds e adicionando o endereço ao array, para remoção futura
        manager.criar_zip(arquivo_zip, arquivos_baixados) # Cria o arquivo zip com os arquivos baixados
        arquivos_baixados_relativos = [os.path.relpath(arquivo, start=caminho_pasta) for arquivo in arquivos_baixados] #Converte o caminho absoluto p/ um caminho relativo
        manager.criar_rar(arquivo_rar, arquivos_baixados_relativos) # Cria o arquivo rar
        
        manager.apagar_arquivos(arquivos_baixados) #Apagando os arquivos pdfs avulsos e deixando somente o zip ou rar
        
        
        
    except requests.RequestException as e:
        print(f"Erro ao acessar {url_base}: {e}")


if __name__ == "__main__":
    main()
