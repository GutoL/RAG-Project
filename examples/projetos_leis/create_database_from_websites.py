
import sys
sys.path.append('../../')
# from indexer.indexer import DocumentsHandler
# from utils.database_manager import DataBaseManager
# from generator.generator import QueryHandler

from codes.indexer.indexer import DocumentsHandler
from codes.utils.database_manager import DataBaseManager
from codes.generator.generator import QueryHandler

from bs4 import BeautifulSoup
import requests
import json
import re

def collect(config):

    ## GETTING LINKS
    response = requests.get(config['main_url'])
    soup = BeautifulSoup(response.content, 'html.parser')
    reference_url = r'https://www25\.senado\.leg\.br/web/atividade/materias/-/materia/\d+$'

    # find all the urls (tags <a> with href attribute)
    links = [a.get('href') for a in soup.find_all('a', href=True)]

    links_filtered = [link for link in links if re.match(reference_url, link)]

    config_file = 'config.json'

    ## LOAD DOCUMENTS
    documents_handler = DocumentsHandler(config_file)

    documents = documents_handler.load_documents_from_web(links_filtered)

    
    ### CREATE DOCUMENT CHUNKS
    chunks = documents_handler.split_documents(documents=documents,
                                            chunk_size=1000, 
                                            chunk_overlap=100, 
                                            is_separator_regex=False)
    
    for c in chunks:
        print(c)
        print('------------')

    print(len(chunks))
    
    #### SAVE DOCUMENTS
    database_manager = DataBaseManager(config_file)
    database_manager.add_to_chroma(chunks) # I am liminting the chunks to be saved because it takes too long to save all of them
    
    # database_manager.get_existing_data()

    # #### PROCESSING A QUERY
    # PROMPT_TEMPLATE = """
    #     Answer the question based only on the following context:

    #     {context}

    #     ---

    #     Answer the question based on the above context: {question}
    #     """

    # query_handler = QueryHandler(PROMPT_TEMPLATE, config_file)
    # query_handler.query_rag('Quem é Capitu?')

def main():
    fp = open('config.json')
    config = json.load(fp)
    fp.close()

    collect(config)

if __name__=="__main__":
    main()