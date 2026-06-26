# Multimodal AI Financial Assistant

An AI-powered financial assistant that analyzes financial documents 
(invoices, receipts, credit card statements) using vision AI and 
supports multi-turn conversations.

## Features
- Upload financial documents as images (JPG, PNG)
- AI reads and understands the document visually
- Multi-turn chat — ask follow-up questions naturally
- Built with LLaMA 4 multimodal model via Groq API

## Tech Stack
- Python, Streamlit
- LangChain (message handling)
- Groq API (meta-llama/llama-4-scout-17b-16e-instruct)
- PIL (image processing)

## How It Works
1. Upload a financial document image
2. Ask any question about it
3. AI analyzes the image and answers
4. Continue asking follow-up questions in chat

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file and add: `GROQ_API_KEY=your-key-here`
4. Run: `streamlit run app.py`
