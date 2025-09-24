import os
import json
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# --- Import the MOCK Bedrock module ---
from bedrock_module import get_bedrock_response

# --- MOCK EMBEDDINGS ---
class MockEmbeddings:
    def embed_documents(self, texts):
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

def get_ai_response_with_rag(user_query: str) -> str:
    """
    Takes a user query, finds relevant context, and uses an AI model to answer.
    """
    try:
        embeddings = MockEmbeddings()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        texts = text_splitter.split_text(KNOWLEDGE_BASE_TEXT)
        vector_db = Chroma.from_texts(texts, embeddings, collection_name="zypher_knowledge")
        
        relevant_docs = vector_db.similarity_search(user_query)
        context = "Relevant information:\n" + "\n".join([doc.page_content for doc in relevant_docs])

        final_response = get_bedrock_response(query=user_query, context=context)

        return final_response
    
    except Exception as e:
        return f"An error occurred: {e}"

# --- NEW FUNCTION FOR THE STREAMLIT APP ---
def generate_plan_with_rag(course, semester, subjects, interests):
    """
    Generates a personalized learning plan using the RAG engine.
    """
    # Create a single prompt based on all user inputs
    user_prompt = f"""
    User's academic info:
    - Course: {course}
    - Semester: {semester}
    - Subjects: {', '.join(subjects)}
    
    User's interests:
    - Skills to develop: {', '.join(interests)}
    
    Generate a comprehensive, actionable 2-week learning plan based on this information. The plan should include:
    1. A clear title for the overall plan.
    2. For each week, provide a title, a short academic focus, a skill focus based on interests, and a concrete actionable task.
    3. For each focus/task, suggest a relevant resource (e.g., a link to an article, a video tutorial, a specific book).
    4. The output must be in a structured JSON format.
    """
    
    # Get the AI-generated response from the RAG engine
    raw_response = get_ai_response_with_rag(user_prompt)
    
    # The AI returns a JSON string, so we need to parse it
    try:
        plan = json.loads(raw_response)
        return plan
    except json.JSONDecodeError:
        # Fallback if the AI doesn't return valid JSON
        return {"title": "Error Generating Plan", "weeks": []}
