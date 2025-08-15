# YouTube RAG (Retrieval-Augmented Generation) App

The **YouTube RAG App** is a **Streamlit-based web application** that allows you to **ask natural language questions** about the content of a YouTube video.  
It automatically extracts the video’s transcript, retrieves relevant parts using **FAISS vector search**, and generates an answer using **Google Gemini 2.0 Flash**.

---

## 🚀 Features
- 📜 **Automatic transcript extraction** from YouTube videos.
- 🔍 **Semantic search** using FAISS to retrieve relevant transcript segments.
- 🤖 **Answer generation** powered by Google Generative AI (Gemini 2.0 Flash).
- 🖥️ **User-friendly Streamlit interface** with instant feedback.
- 🐳 **Dockerized** for easy deployment anywhere.

---

## 📂 Project Structure

youtube_rag\
&emsp;-app.py\
&emsp;-rag_backend.py # Backend logic\
&emsp;-.env\
-requirements.txt \
-Dockerfile \
-README.md 


## 🛠️ Setup

### 1️⃣ Clone the Repository
```
git clone https://github.com/your-username/youtube-rag.git
cd youtube-rag

2️⃣ Create a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies

cd ..
pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Configure Environment Variables

GOOGLE_API_KEY=your_google_api_key_here


▶️ Run Locally

streamlit run app.py

Access the app at: http://localhost:8501

```

🐳 Run with Docker

```
Build Image

docker build -t youtube-rag .

Run Container

docker run -d --name {container-name} -p 8501:8501 youtube-rag

Access the app at: http://localhost:8501
```

📜 How It Works

🔹 1. Extract Video ID

The backend parses the YouTube URL to retrieve the video ID.

🔹 2. Fetch Transcript

Uses youtube-transcript-api to retrieve manual or auto-generated English transcripts.

🔹 3. Chunk Text

Splits transcript into chunks (1000 characters, 200 overlap) using LangChain’s RecursiveCharacterTextSplitter.

🔹 4. Embed & Store

Creates embeddings with Google Generative AI and stores them in a FAISS vector database.

🔹 5. Retrieve Relevant Chunks

Uses similarity search to fetch top-k matching transcript chunks for a given question.

🔹 6. Generate Answer

Passes retrieved chunks + the user’s question to Gemini 2.0 Flash for a final answer.


👨‍💻 Author

Shiv Choudhary\
📧 shivchoudhary369@gmail.com\
🔗 https://www.linkedin.com/in/shiv-kumar-choudhary/ | https://github.com/chshiv



