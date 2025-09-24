import os
import json
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# --- Import the MOCK Bedrock module ---
from bedrock_module import get_bedrock_response

# --- MOCK EMBEDDINGS ---
# This class mocks the BedrockEmbeddings function for local testing.
class MockEmbeddings:
    def embed_documents(self, texts):
        # A simple mock embedding that returns a list of zeros for each text
        return [[0] * 1024 for _ in texts]
    
    def embed_query(self, text):
        return [0] * 1024

# --- MOCK KNOWLEDGE BASE ---
KNOWLEDGE_BASE_TEXT = """
Data Structures & Algorithms (DSA) are fundamental topics in Computer Science. A
key concept is the Big O notation, which describes the performance or complexity of an
algorithm. Common data structures include Arrays, Linked Lists, Stacks, Queues,
Trees, and Graphs.
Object-Oriented Programming (OOP) is a programming paradigm based on the concept of
"objects". These objects can contain data, in the form of fields (often known as
attributes), and code, in the form of procedures (often known as methods).
Popular OOP languages include Java and Python.
"""

# --- YOUR RAG ENGINE ---
def get_ai_response_with_rag(user_query: str) -> str:
    """
    Takes a user query, finds relevant context, and uses an AI model to answer.
    """
    try:
        # Step 1: Use the MOCK Embeddings client
        embeddings = MockEmbeddings()

        # Step 2: Create a temporary knowledge base from the text.
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        texts = text_splitter.split_text(KNOWLEDGE_BASE_TEXT)
        vector_db = Chroma.from_texts(texts, embeddings, collection_name="zypher_knowledge")
        
        # Step 3: Find the most relevant documents
        relevant_docs = vector_db.similarity_search(user_query)
        context = "Relevant information:\n" + "\n".join([doc.page_content for doc in relevant_docs])

        # Step 4: Use the MOCK Bedrock model to generate a final response
        final_response = get_bedrock_response(query=user_query, context=context)

        return final_response
    
    except Exception as e:
        return f"An error occurred: {e}"

# --- DEMONSTRATION ---
if __name__ == "__main__":
    print("Running the RAG engine...")
    
    response_1 = get_ai_response_with_rag("What is Big O notation?")
    print("\n--- Question 1 ---")
    print("Answer:", response_1)
    
    response_2 = get_ai_response_with_rag("What is the capital of France?")
    print("\n--- Question 2 ---")
    print("Answer:", response_2)
