from langchain_ollama import OllamaEmbeddings
# from langchain_community.embeddings.bedrock import BedrockEmbeddings

class Embeddings():

    def __init__(self, model_name:str='nomic-embed-text') -> None:
        self.model_name = model_name

    # https://python.langchain.com/docs/integrations/text_embedding/

    @staticmethod
    def get_embedding_function(model_name:str=None):
        
        if not model_name:
            model_name = model_name

        # embeddings = BedrockEmbeddings(
        #     credentials_profile_name='default', region_name='us-east-1'
        # )

        embeddings = OllamaEmbeddings(model=model_name)

        return embeddings