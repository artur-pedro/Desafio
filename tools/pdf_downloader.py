import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

class PDFDownloader:
    def __init__(self, url_completo, quantidade_de_pdfs, url_base, nome_comum):
        
        self.url_completo = url_completo
        self.url_base = url_base
        self.nome_comum = nome_comum
        self.quantidade_de_pdfs = quantidade_de_pdfs
    
    def buscar_e_baixar_pdfs(self, arquivos_baixados, pasta_temp=None): 
        '''
        Função para buscar os arquivos pdfs em um site, 
        se baseando em um nome comum no html, chama a função de baixar
        
        '''
        contador_de_pdfs = 0
        try:
            response = requests.get(self.url_base)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            todos_os_links = soup.find_all("a", href=True)

            for link in todos_os_links:
                texto_link = link.text.strip()
                href = link.get("href", "")

                if texto_link.startswith(self.nome_comum) and contador_de_pdfs < self.quantidade_de_pdfs:
                    url_completo = urljoin(self.url_base, href)
                    print(f"Baixando: {url_completo}")
                    self.baixar_pdf(url_completo, texto_link, arquivos_baixados, pasta_temp)
                    contador_de_pdfs += 1
            return arquivos_baixados
        
        except requests.RequestException as e:
            print(f"Erro ao acessar {self.url_base}: {e}")
        
    def baixar_pdf(self, url_completo, nome_do_arquivo, arquivos_baixados, pasta_temp): 
        '''
        Função para baixar um arquivo .pdf e 
        adicioná-lo a um array para possível exclusão no futuro, 
        ou outra operação
        
        '''
        try:
            response = requests.get(url_completo)
            response.raise_for_status()
            
            diretorio_pai = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho_arquivo = os.path.join(diretorio_pai, f"{nome_do_arquivo}.pdf")
            caminho_arquivo = os.path.join(pasta_temp or os.getcwd(), f"{nome_do_arquivo}pdf")
            
            with open(caminho_arquivo, "wb") as f:
                f.write(response.content)

            print(f"Download concluído: {caminho_arquivo}")
            
            arquivos_baixados.append(caminho_arquivo)
            
        except requests.RequestException as e:
            print(f"Erro ao baixar {url_completo}: {e}")
            