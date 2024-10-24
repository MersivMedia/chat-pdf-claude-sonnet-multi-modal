<<<<<<< HEAD
# PDF Chat System

This application allows users to chat with PDF documents, including text and images. It uses Claude 3.5 Sonnet for image analysis and text generation, and stores document content in a vector database for efficient retrieval.

## Features

- Process multiple PDF files or a folder of PDFs
- Extract text and images from PDFs
- Analyze images using Claude Vision
- Store document content in a persistent vector database
- Chat interface with persistent history
- Source citations for responses

## Prerequisites

- Python 3.8 or higher
- Anthropic API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/MersivMedia/chat-pdf-claude-sonnet-multi-modal.git
   cd chat-pdf-claude-sonnet-multi-modal
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up your `.env` file with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ```

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501).

3. Upload PDF files:
   - Use the file uploader to select one or more PDF files from your computer.
   - Alternatively, enter the path to a folder containing PDF files in the text input field.

4. Process PDFs:
   - Click the "Process PDFs" button to extract text and images from the uploaded PDFs.
   - The application will analyze the content and store it in the vector database.
   - This step may take some time depending on the number and size of the PDFs.

5. Chat with your PDFs:
   - Once the PDFs are processed, you can start asking questions in the text input field under "Chat with your PDFs".
   - Type your question and press Enter.
   - The system will search the processed PDFs for relevant information and generate a response using Claude.
   - The response will include citations to the source PDFs and page numbers.

6. View chat history:
   - The chat history is displayed below the input field, showing both your questions and the assistant's responses.
   - The chat history persists during your session, allowing for follow-up questions and context-aware responses.

7. Reuse processed PDFs:
   - The vector database persists between application restarts, so you don't need to reprocess the same PDFs every time you use the application.
   - You can add new PDFs to the existing database by uploading and processing them.

## Tips for Effective Use

- For best results, use high-quality PDFs with clear text and images.
- When asking questions, be as specific as possible to get more accurate responses.
- You can ask follow-up questions or request clarification on previous responses.
- If you're not getting the expected results, try rephrasing your question or providing more context.

## Troubleshooting

- If you encounter any errors related to the Anthropic API, make sure your API key is correctly set in the `.env` file.
- If the application is slow to process PDFs, consider breaking large documents into smaller files.
- For issues with image analysis, ensure that the images in your PDFs are of good quality and resolution.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
=======
# chat-pdf-claude-multi-modal
This application allows users to chat with PDF documents, including text and images. It uses Claude 3.5 Sonnet for image analysis and text generation, and stores document content in a vector database for efficient retrieval.
>>>>>>> origin/main
