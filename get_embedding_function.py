from langchain_ollama import OllamaEmbeddings
# from langchain_community.embeddings.bedrock import BedrockEmbeddings
#from langchain_community.embeddings import BedrockEmbeddings

def get_embedding_function():
    # Specify the path to the model file
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )
