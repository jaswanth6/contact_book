from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import List
from io import BytesIO
import pdfminer.high_level
import pdfminer.layout
import base64

app = FastAPI()

@app.get("/")
def index():
    return HTMLResponse("""
        <html>
            <body>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="pdf_file">
                    <button type="submit">Convert</button>
                </form>
            </body>
        </html>
    """)

@app.post("/")
async def convert_pdf_to_text(pdf_file: UploadFile = File(...)):
    pdf_data = await pdf_file.read()
    text = extract_text_from_pdf(pdf_data)
    encoded_text = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    return HTMLResponse(f"""
        <html>
            <body>
                <p>{text} break here please to see ----------</p>
                <button onclick="copyToClipboard('{encoded_text}')">Copy</button>
            </body>
            <script>
                function copyToClipboard(text) {{
                    const textarea = document.createElement('textarea');
                    textarea.value = atob(text);
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                }}
            </script>
        </html>
    """)

def extract_text_from_pdf(pdf_data: bytes) -> str:
    output_string = BytesIO()
    laparams = pdfminer.layout.LAParams()
    pdfminer.high_level.extract_text_to_fp(BytesIO(pdf_data), output_string, laparams=laparams)
    return output_string.getvalue().decode("utf-8")




import uvicorn
uvicorn.run(app)