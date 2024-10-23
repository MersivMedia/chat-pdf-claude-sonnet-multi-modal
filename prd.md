I would like to build a multi-modal RAG application to chat with pdf documents. the pdf documents contain images that have words. I would like to transcribe the words from the images and then store all transcriptions with their associated image pages in a vector database. I would like the application to have a persisted index so that the documents only need to be parsed once and then are re-used when opening the application again. When chatting with the documents, any answer provided by the LLM should also cite the reference source from the documents and pull that page. I also want to use the latest anthropic claude model with vision. the latest claude model is:     model="claude-3-5-sonnet-20241022". 1. please provide the best architecture to achieve my goals. Give me a highly detailed technical outline 2. please include any code to get started. 3. suggest any additional features that might be helpful for my application. 

**Key Components:**

1. **Document Processing:**
- Use PyMuPDF (fitz) for PDF parsing
- Claude Sonnet or Tesseract for OCR
- LangChain for document chunking
- Sentence transformers for embedding generation

2. **Storage:**
- Chroma DB for vector storage (supports persistence)
- SQLite for metadata storage

3. **RAG Implementation:**
- Anthropic's Claude-3 for response generation
- Hybrid search (semantic + keyword)
- Source tracking and citation


here are the claude vision docs:

Build with Claude
Vision
The Claude 3 family of models comes with new vision capabilities that allow Claude to understand and analyze images, opening up exciting possibilities for multimodal interaction.

This guide describes how to work with images in Claude, including best practices, code examples, and limitations to keep in mind.

​
How to use vision
Use Claude’s vision capabilities via:

claude.ai. Upload an image like you would a file, or drag and drop an image directly into the chat window.
The Console Workbench. If you select a model that accepts images (Claude 3 models only), a button to add images appears at the top right of every User message block.
API request. See the examples in this guide.
​
Before you upload
​
Evaluate image size
You can include multiple images in a single request (up to 5 for claude.ai and 100 for API requests). Claude will analyze all provided images when formulating its response. This can be helpful for comparing or contrasting images.

For optimal performance, we recommend resizing images before uploading if they exceed size or token limits. If your image’s long edge is more than 1568 pixels, or your image is more than ~1,600 tokens, it will first be scaled down, preserving aspect ratio, until it’s within the size limits.

If your input image is too large and needs to be resized, it will increase latency of time-to-first-token, without giving you any additional model performance. Very small images under 200 pixels on any given edge may degrade performance.

To improve time-to-first-token, we recommend resizing images to no more than 1.15 megapixels (and within 1568 pixels in both dimensions).
Here is a table of maximum image sizes accepted by our API that will not be resized for common aspect ratios. With the Claude 3.5 Sonnet model, these images use approximately 1,600 tokens and around $4.80/1K images.

Aspect ratio	Image size
1:1	1092x1092 px
3:4	951x1268 px
2:3	896x1344 px
9:16	819x1456 px
1:2	784x1568 px
​
Calculate image costs
Each image you include in a request to Claude counts towards your token usage. To calculate the approximate cost, multiply the approximate number of image tokens by the per-token price of the model you’re using.

If your image does not need to be resized, you can estimate the number of tokens used through this algorithm: tokens = (width px * height px)/750

Here are examples of approximate tokenization and costs for different image sizes within our API’s size constraints based on Claude 3.5 Sonnet per-token price of $3 per million input tokens:

Image size	# of Tokens	Cost / image	Cost / 1K images
200x200 px(0.04 megapixels)	~54	~$0.00016	~$0.16
1000x1000 px(1 megapixel)	~1334	~$0.004	~$4.00
1092x1092 px(1.19 megapixels)	~1590	~$0.0048	~$4.80
​
Ensuring image quality
When providing images to Claude, keep the following in mind for best results:

Image format: Use a supported image format: JPEG, PNG, GIF, or WebP.
Image clarity: Ensure images are clear and not too blurry or pixelated.
Text: If the image contains important text, make sure it’s legible and not too small. Avoid cropping out key visual context just to enlarge the text.
​
Prompt examples
Many of the prompting techniques that work well for text-based interactions with Claude can also be applied to image-based prompts.

These examples demonstrate best practice prompt structures involving images.

Just as with document-query placement, Claude works best when images come before text. Images placed after text or interpolated with text will still perform well, but if your use case allows it, we recommend an image-then-text structure.
​
About the prompt examples
These prompt examples use the Anthropic Python SDK, and fetch images from Wikipedia using the httpx library. You can use any image source.

The example prompts use these variables.

Python

import base64
import httpx

image1_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
image1_media_type = "image/jpeg"
image1_data = base64.b64encode(httpx.get(image1_url).content).decode("utf-8")

image2_url = "https://upload.wikimedia.org/wikipedia/commons/b/b5/Iridescent.green.sweat.bee1.jpg"
image2_media_type = "image/jpeg"
image2_data = base64.b64encode(httpx.get(image2_url).content).decode("utf-8")
To utilize images when making an API request, you can provide images to Claude as a base64-encoded image in image content blocks. Here is simple example in Python showing how to include a base64-encoded image in a Messages API request:

Python

import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image1_media_type,
                        "data": image1_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image."
                }
            ],
        }
    ],
)
print(message)
See Messages API examples for more example code and parameter details.


Example: One image


Example: Multiple images


Example: Multiple images with a system prompt


Example: Four images across two conversation turns

​
Limitations
While Claude’s image understanding capabilities are cutting-edge, there are some limitations to be aware of:

People identification: Claude cannot be used to identify (i.e., name) people in images and will refuse to do so.
Accuracy: Claude may hallucinate or make mistakes when interpreting low-quality, rotated, or very small images under 200 pixels.
Spatial reasoning: Claude’s spatial reasoning abilities are limited. It may struggle with tasks requiring precise localization or layouts, like reading an analog clock face or describing exact positions of chess pieces.
Counting: Claude can give approximate counts of objects in an image but may not always be precisely accurate, especially with large numbers of small objects.
AI generated images: Claude does not know if an image is AI-generated and may be incorrect if asked. Do not rely on it to detect fake or synthetic images.
Inappropriate content: Claude will not process inappropriate or explicit images that violate our Acceptable Use Policy.
Healthcare applications: While Claude can analyze general medical images, it is not designed to interpret complex diagnostic scans such as CTs or MRIs. Claude’s outputs should not be considered a substitute for professional medical advice or diagnosis.
Always carefully review and verify Claude’s image interpretations, especially for high-stakes use cases. Do not use Claude for tasks requiring perfect precision or sensitive image analysis without human oversight.

