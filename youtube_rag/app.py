from rag_backend import extract_video_id, get_transcript, build_chain
import streamlit as st

st.title("YouTube RAG")

# Use a form so Enter key works as submit
with st.form("youtube_rag_form"):
    url = st.text_input("Enter YouTube video URL")
    question = st.text_input("Ask a question about the video")
    submit = st.form_submit_button("Submit")  # Works on button click or Enter

if submit:
    if not url and not question:
        st.error("Please enter both YouTube video URL and a question")
    elif not url:
        st.error("Please enter a valid YouTube video URL")
    elif not question:
        st.error("Please enter a question")
    else:
        with st.spinner("Processing..."):
            try:
                video_id = extract_video_id(url)
                if not video_id:
                    st.error("Invalid YouTube URL")
                else:
                    transcript = get_transcript(video_id)
                    rag_chain = build_chain(transcript)
                    answer = rag_chain(question)
                    st.success("Answer:")
                    st.write(answer)
            except Exception as e:
                st.error(f"Error: {str(e)}")
