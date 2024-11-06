from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

import json

class DocumentsHandler():

    def __init__(self) -> None:
        fp = open('../config.json')
        config = json.load(fp)
        fp.close()

        self.documents_path = config['documents_folder']

    def load_documents(self, path:str=None):

        if not path:
            path = self.documents_path
        
        # https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/
        document_loader = PyPDFDirectoryLoader(path)
        return document_loader.load()

    

    def split_documents(self, documents: list[Document], chunk_size:int, chunk_overlap:int, is_separator_regex:bool):
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=is_separator_regex
        )

        return text_splitter.split_documents(documents)
