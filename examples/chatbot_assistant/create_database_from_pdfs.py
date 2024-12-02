
import sys
sys.path.append('../../')
# from indexer.indexer import DocumentsHandler
# from utils.database_manager import DataBaseManager
# from generator.generator import QueryHandler

from codes.indexer.indexer import DocumentsHandler
from codes.utils.database_manager import DataBaseManager
from codes.generator.generator import QueryHandler


def main():

    config_file = 'config.json'

    ## LOAD DOCUMENTS
    documents_handler = DocumentsHandler(config_file)

    documents = documents_handler.load_documents_from_pdf()

    ### CREATE DOCUMENT CHUNKS
    chunks = documents_handler.split_documents(documents=documents,
                                            chunk_size=800, 
                                            chunk_overlap=80, 
                                            is_separator_regex=False)
    

    #### SAVE DOCUMENTS
    database_manager = DataBaseManager(config_file)
    database_manager.add_to_chroma(chunks) # I am liminting the chunks to be saved because it takes too long to save all of them
    
    database_manager.get_existing_data()

    # #### PROCESSING A QUERY
    # PROMPT_TEMPLATE = """
    #     Answer the question based only on the following context:

    #     {context}

    #     ---

    #     Answer the question based on the above context: {question}
    #     """

    # query_handler = QueryHandler(PROMPT_TEMPLATE)
    # query_handler.query_rag('Quem é Capitu?')

if __name__=="__main__":
    main()