import sys
sys.path.append('../../')

from langchain.schema.document import Document
from langchain_chroma import Chroma

# from langchain_community.docstore.in_memory import InMemoryDocstore
# from langchain_community.vectorstores import FAISS
# import faiss
import os
import shutil
import json

from ..utils.embeddings_handler import Embeddings


class DataBaseManager():

    def __init__(self, config_file:str) -> None:

        fp = open(config_file)
        config = json.load(fp)
        fp.close()

        self.CHROMA_PATH = config['db_name']
        self.db = None
        self.embedding_model_name = config['embedding_model_name']
    
    def get_db_connection(self):
        
        if not self.db:
            self.db = Chroma(
                persist_directory=self.CHROMA_PATH, embedding_function=Embeddings.get_embedding_function(self.embedding_model_name)
            )
        
        return self.db
        
    def calculate_chunk_ids(self, chunks: list[Document]):
        # This will create IDs like: Page source : Page number : Chunk index

        last_page_id = None,
        current_chunk_index = 0

        for i, chunk in enumerate(chunks):
            
            if 'page' not in chunk:
                page = i
            else:
                page = chunk.metadata['page']

            source = chunk.metadata['source']
            
            current_page_id = f'{source}:{page}'

            # if the current page ID is the same of the last one, we have to increment
            # the chunk ID
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID
            chunk_id = f'{current_page_id}:{current_chunk_index}'
            last_page_id = current_page_id

            # Add it to the page metadata
            chunk.metadata['id'] = chunk_id

        return chunks

    def add_to_chroma(self, chunks: list[Document], CHROMA_PATH:str=None):

        db = self.get_db_connection()

        # Calculate the page IDs
        chunks_with_ids = self.calculate_chunk_ids(chunks)

        # Add or update the documents

        existing_items = db.get(include=[]) # ids that are always included by default
        existing_ids = set(existing_items['ids'])
        print(f'Number of existing documents in DB: {len(existing_ids)}')

        # Only add documents that don'exist in the DB
        new_chunks = []

        for chunk in chunks_with_ids:
            if chunk.metadata['id'] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")

            new_chunks_ids = [chunk.metadata['id'] for chunk in new_chunks]
            db.add_documents(documents=new_chunks, ids=new_chunks_ids)
            # db.persist()

        else:
            print("✅ No new documents to add")

    def get_existing_data(self):
        
        db = self.get_db_connection()
        # existing_items = db.get(include=[]) # ids that are always included by default
        existing_items = db.get()

        return existing_items

    def clear_database(self, CHROMA_PATH:str=None):

        if not CHROMA_PATH:
            CHROMA_PATH = self.CHROMA_PATH

        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)