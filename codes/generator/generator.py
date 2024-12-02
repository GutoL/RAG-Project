import sys
sys.path.append('../../')

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from codes.utils.database_manager import DataBaseManager

import json

class QueryHandler():
    
    def __init__(self, PROMPT_TEMPLATE:str, config_file:str) -> None:
        self.PROMPT_TEMPLATE = PROMPT_TEMPLATE

        fp = open(config_file)
        config = json.load(fp)
        fp.close()

        # Prepare the DB
        self.database_manager = DataBaseManager(config_file)

        self.llm_name = config['llm_name']
        

    def query_rag(self, query_text: str, PROMPT_TEMPLATE:str=None, k:int=10):
        
        if not PROMPT_TEMPLATE:
            PROMPT_TEMPLATE = self.PROMPT_TEMPLATE
            
        db = self.database_manager.get_db_connection()        
        
        # Search
        results = db.similarity_search(query_text, k=k)
        
        context_text = '\n\n---\n\n'.join([doc.page_content for doc in results])

        # results = db.similarity_search_with_score(query_text, k=5)
        # context_text = '\n\n---\n\n'.join([doc.page_content for doc, _score in results])

        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        prompt = prompt_template.format(context=context_text, question=query_text)
        # print(prompt)

        model = OllamaLLM(model=self.llm_name)
        response_text = model.invoke(prompt)

        # sources = [doc.metadata.get("id", None) for doc, _score in results]
        sources = [doc.metadata.get("id", None) for doc in results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        # print(formatted_response)

        return response_text # '''

        