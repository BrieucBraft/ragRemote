from langchain_ollama import OllamaEmbeddings
# from langchain_community.embeddings.bedrock import BedrockEmbeddings
#from langchain_community.embeddings import BedrockEmbeddings

def get_embedding_function():
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    #embeddings = OllamaEmbeddings(model="granite-embedding:30m", base_url="http://localhost:11434")  # adjust if necessary)
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    #embeddings = OllamaEmbeddings(model='mxbai-embed-large')
    return embeddings
