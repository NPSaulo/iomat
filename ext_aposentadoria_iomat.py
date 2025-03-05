import requests
import io
import re
from pypdf import PdfReader



def baixar_ler_diário(edicao):
    try:
        url = f"https://www.iomat.mt.gov.br/portal/edicoes/download/{str(edicao)}"
        print(f"Tentando baixar edição nº {edicao} do Diário Oficial de Mato Grosso.")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Levanta excessão em caso de erros na resposta
        
        #Lendo o pdf, em formato de bytes, na resposta à requisição
        pdf_file = io.BytesIO(response.content)

        #Iniciando o objeto PdfReader, para ler o arquivo PDF
        pdf_reader = PdfReader(pdf_file)
        
        # Extraindo número de páginas
        num_paginas = len(pdf_reader.pages)
        print(f"PDF com {num_paginas} páginas baixado e lido com sucesso.")
    
        # Extraindo todo o texto
        texto = ""
        for num_pagina in range(num_paginas):
            pagina = pdf_reader.pages[num_pagina]
            texto += pagina.extract_text() + "\n\n"


        aposentar_pattern = r"(?s)ATO\s*N[º\.]\.?\s*\d+/\d+.*?(?:Aposentar|aposentar).*?MAURO\s*MENDES(?:\s*Governador do Estado)?(?:\s*\(Assinado digitalmente\))?"
        matches = re.findall(aposentar_pattern, texto, re.IGNORECASE | re.DOTALL)
        # Retornando as informações desejadas
        return {
            #"num_paginas": num_paginas,
            #"texto": texto,
            "match": matches
        }
            
    except requests.exceptions.RequestException as e:
        print(f"Erro baixando o PDF: {e}")
        return None
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return None


if __name__ == "__main__":
    
    edicao = input("Forneça o nº da edição desejada: ")
    pdf_info = baixar_ler_diário(edicao)
    if pdf_info['match']:
        print(f"Localizadas {len(pdf_info['match'])} publicações de aposentadoria.")
        for ato in pdf_info['match']:
            print("-----------------")
            print(ato)
            print("-----------------")
    else:
        print(f"Nenhuma publicação de aposentadoria localizada na edição {edicao}")