import os
import fitz
import base64
import anthropic
import streamlit as st
import logging
from dotenv import load_dotenv
from chromadb import Client, Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from PIL import Image
import io
import uuid
import glob

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class PDFChatSystem:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.chroma_client = Client(Settings(
            persist_directory="db",
            is_persistent=True
        ))
        self.collection = self.chroma_client.get_or_create_collection("pdf_documents")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    def process_pdfs(self, pdf_files):
        for pdf_file in pdf_files:
            self.process_pdf(pdf_file)

    def process_pdf(self, pdf_file):
        logger.info(f"Processing PDF: {pdf_file.name}")
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text
            text = page.get_text()
            chunks = self.text_splitter.split_text(text)
            
            # Store text chunks
            for chunk_idx, chunk in enumerate(chunks):
                self.store_chunk(
                    text=chunk,
                    metadata={
                        "source": pdf_file.name,
                        "page": page_num,
                        "type": "text",
                        "chunk_idx": chunk_idx
                    }
                )
            
            # Extract and process images
            images = page.get_images()
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Process image with Claude Vision
                image_analysis = self.analyze_image_with_claude(image_bytes)
                
                # Store image analysis
                self.store_chunk(
                    text=image_analysis,
                    metadata={
                        "source": pdf_file.name,
                        "page": page_num,
                        "type": "image_analysis",
                        "image_index": img_index
                    }
                )
        logger.info(f"Finished processing PDF: {pdf_file.name}")

    def store_chunk(self, text, metadata):
        embedding = self.embedding_model.encode(text).tolist()
        chunk_id = str(uuid.uuid4())
        self.collection.add(
            ids=[chunk_id],
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding]
        )
        logger.debug(f"Stored chunk: {metadata}")

    def analyze_image_with_claude(self, image_bytes):
        try:
            # Open the image using Pillow
            img = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if it's not already (e.g., if it's RGBA)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save the image as JPEG in a bytes buffer
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)
            
            # Encode the JPEG image to base64
            base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            message = self.client.messages.create(
                model=os.getenv("ANTHROPIC_MODEL"),
                max_tokens=1024,
                system="You are a helpful assistant that analyzes images.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": "Please describe all text and visual content in this image in detail."
                            }
                        ],
                    }
                ],
            )
            logger.debug("Image analyzed with Claude")
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error analyzing image with Claude: {str(e)}")
            return f"Error analyzing image: {str(e)}"

    def chat(self, query, chat_history):
        logger.info(f"Received query: {query}")
        # Retrieve relevant chunks
        results = self.collection.query(
            query_texts=[query],
            n_results=5
        )

        # Prepare context
        context = "\n\n".join(results['documents'][0])
        sources = [f"{m['source']} (Page {m['page']})" for m in results['metadatas'][0]]

        # Prepare chat history for Claude
        claude_messages = [
            {"role": "user" if i % 2 == 0 else "assistant", "content": msg}
            for i, msg in enumerate(chat_history)
        ]
        claude_messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}\n\nPlease answer the question based on the context provided. Include relevant citations in your response."})

        # Generate response with Claude
        message = self.client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL"),
            max_tokens=1024,
            system="You are a helpful assistant that answers questions based on the provided context. Always cite your sources.",
            messages=claude_messages,
        )

        response = message.content[0].text
        logger.info("Generated response from Claude")
        return response, sources

def main():
    st.title("PDF Chat System")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    pdf_chat = PDFChatSystem()

    # File uploader for multiple PDFs
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    # Folder input for batch processing
    folder_path = st.text_input("Or enter a folder path containing PDFs:")

    if st.button("Process PDFs"):
        with st.spinner("Processing PDFs..."):
            if uploaded_files:
                pdf_chat.process_pdfs(uploaded_files)
            elif folder_path:
                pdf_files = [open(f, "rb") for f in glob.glob(os.path.join(folder_path, "*.pdf"))]
                pdf_chat.process_pdfs(pdf_files)
                for f in pdf_files:
                    f.close()
            st.success("PDFs processed successfully!")

    st.subheader("Chat with your PDFs")
    query = st.text_input("Enter your question:")
    if query:
        with st.spinner("Generating response..."):
            response, sources = pdf_chat.chat(query, st.session_state.chat_history)
        st.write("Response:", response)
        st.write("Sources:")
        for source in sources:
            st.write(f"- {source}")
        
        # Update chat history
        st.session_state.chat_history.extend([query, response])

    # Display chat history
    st.subheader("Chat History")
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write("You:", message)
        else:
            st.write("Assistant:", message)

if __name__ == "__main__":
    main()
