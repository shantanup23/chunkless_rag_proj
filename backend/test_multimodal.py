import instructor
import google.generativeai as genai
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

client = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="models/gemini-1.5-flash"),
    mode=instructor.Mode.GEMINI_JSON,
)

class ImageDescription(BaseModel):
    description: str

img = Image.new('RGB', (60, 30), color = 'red')

try:
    resp = client.messages.create(
        messages=[
            {
                "role": "user",
                "content": [
                    "What color is this image?",
                    img
                ]
            }
        ],
        response_model=ImageDescription,
    )
    print("Test 1 (PIL.Image direct):", resp)
except Exception as e:
    print("Test 1 failed:", e)

