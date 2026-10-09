import instructor
import google.generativeai as genai
from pydantic import BaseModel
import os
import base64
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="models/gemini-1.5-flash"),
    mode=instructor.Mode.GEMINI_JSON,
)

class ImageDescription(BaseModel):
    description: str

img = Image.new('RGB', (60, 30), color = 'red')
buffered = io.BytesIO()
img.save(buffered, format="PNG")
encoded_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

print("Running Test: OpenAI base64 format")
try:
    resp = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What color is this image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_string}"}}
                ]
            }
        ],
        response_model=ImageDescription,
    )
    print("Test successful:", resp)
except Exception as e:
    import traceback
    traceback.print_exc()

