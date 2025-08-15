from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv
import asyncio
import re
import os

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise EnvironmentError("GOOGLE_API_KEY not found in environment variables.")

def ensure_event_loop():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

# Extract YouTube video ID from URL
def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    raise ValueError("Invalid YouTube URL")

# Get transcript from YouTube video--
def get_transcript(video_id: str) -> str:
    try:
        ytt_api = YouTubeTranscriptApi()
        transcripts = ytt_api.list(video_id)
        # Prefer English (manual), else fall back to generated English
        try:
            transcript_obj = transcripts.find_manually_created_transcript(['en'])
        except NoTranscriptFound:
            transcript_obj = transcripts.find_generated_transcript(['en'])

        data = transcript_obj.fetch()
        return " ".join(entry.text for entry in data)

    except (TranscriptsDisabled, NoTranscriptFound):
        raise ValueError("Transcript is not available for this video.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while fetching transcript: {e}")

# Build the RAG chain using Gemini 2.0 Flash
def build_chain(transcript: str):
    ensure_event_loop()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = [Document(page_content=chunk) for chunk in text_splitter.split_text(transcript)]

    #Create Embending Object
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    #Create Vector Store Object
    vector_store = FAISS.from_documents(docs, embeddings)

    # Step 3: Chat model (Gemini 2.0 Flash)
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.0-flash",
        temperature=0.5
    )

    # Step 4: Prompt template
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant. Use the following context to answer the user's question.

    Context:
    {context}

    Question: {question}
    Answer:
    """)

    # Step 5: RAG chain
    def chain_function(question: str):
        relevant_docs = vector_store.similarity_search(question, k=4)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        str_parser = StrOutputParser()
        chain = prompt | llm | str_parser
        return chain.invoke({"context": context, "question": question})

    return chain_function
