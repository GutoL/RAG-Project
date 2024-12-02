import sys
sys.path.append('../../')

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from codes.generator.generator import QueryHandler

class TextRequest(BaseModel):
    question:str

# start the api: uvicorn examples.projetos_leis.api:app
app = FastAPI()

@app.post('/')
def read_root(request:TextRequest):

    if not request.question:
        raise HTTPException(status_code=400, detail='No text provided')
    
    # try:
    #### PROCESSING A QUERY
    PROMPT_TEMPLATE = """
        Answer the question based only on the following context:

        {context}

        ---

        Answer the question based on the above context: {question}
        """

    path = 'examples/projetos_leis/'
    # path = ''

    query_handler = QueryHandler(PROMPT_TEMPLATE, path+'config.json')
    response = query_handler.query_rag(request.question)

    return {'response': response}
            
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))