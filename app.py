import os
import base64
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

# Load API key
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 AI Financial Assistant")
st.write("Upload a financial document and ask questions about it!")

# Initialize LLM
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY")
)

# Helper: convert image to base64
def image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "image_data" not in st.session_state:
    st.session_state.image_data = None

# Layout: two columns
col1, col2 = st.columns([1, 1])

# Left column: document upload
with col1:
    st.subheader("📄 Upload Document")
    uploaded_file = st.file_uploader(
        "Upload invoice, receipt or credit card statement",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document", use_column_width=True)

        # Store image data in session
        uploaded_file.seek(0)
        st.session_state.image_data = image_to_base64(uploaded_file)
        st.success("✅ Document uploaded successfully!")

# Right column: chat
with col2:
    st.subheader("💬 Ask Questions")

    # Show chat history
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                # Handle both string and list content
                if isinstance(msg.content, str):
                    st.write(msg.content)
                else:
                    for part in msg.content:
                        if part["type"] == "text":
                            st.write(part["text"])
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)

    # Question input
    if st.session_state.image_data:
        question = st.chat_input("Ask about your document...")

        if question:
            # Build message with image + question
            # Only send image in first message, text only after that
            if len(st.session_state.messages) == 0:
                human_msg = HumanMessage(
                    content=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{st.session_state.image_data}"
                            }
                        },
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                )
            else:
                # Follow up questions - text only
                human_msg = HumanMessage(content=question)

            # Show user question
            with st.chat_message("user"):
                st.write(question)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = llm.invoke(
                        st.session_state.messages + [human_msg]
                    )
                    st.write(response.content)

            # Save to history
            st.session_state.messages.append(human_msg)
            st.session_state.messages.append(
                AIMessage(content=response.content)
            )

    else:
        st.info("👈 Please upload a document first!")

    # Clear chat button
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()