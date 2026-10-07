
from langchain_ollama import OllamaEmbeddings
# import db
import tiktoken

# função pra ser chamada todas as vezes que necessita de um embedding
def get_embeddings(text):

    embeddings_model = OllamaEmbeddings(model='mxbai-embed-large')
    embeddings = embeddings_model.embed_query(text)
    return embeddings

def count_tokens(text):

    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except:
    
        return len(text) // 4