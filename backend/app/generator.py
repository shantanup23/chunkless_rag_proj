import os
import glob
import json
from PIL import Image
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

from google import genai
from google.genai import types

from .schemas import MockTestPayload

load_dotenv()
# The client automatically picks up GEMINI_API_KEY from the environment
client = genai.Client()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def generate_mock_test(markdown_content: str, topic_prompt: str, doc_id: str = None, chat_history: list = None) -> MockTestPayload:
    prompt_content = f"""You are a strict academic evaluator. Your task is to generate an educational mock test based ONLY on the provided Syllabus Markdown and attached images.
If the requested topic is NOT present in the syllabus, set 'is_topic_relevant' to False and provide a rejection reason.
If it is relevant, generate the test strictly adhering to the schema.

--- SYLLABUS MARKDOWN ---
{markdown_content[:30000]} 
--- END SYLLABUS ---

User Request: {topic_prompt}"""

    content_list = [prompt_content]
    
    if doc_id:
        ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "extracted_assets")
        image_paths = glob.glob(os.path.join(ASSETS_DIR, f"{doc_id}_*.png"))
        for img_path in image_paths[:5]: # Limit to 5 images to avoid massive payloads
            try:
                img = Image.open(img_path)
                content_list.append(img)
            except Exception as e:
                print(f"Failed to load image {img_path}: {e}")

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=content_list,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MockTestPayload,
        )
    )
    
    # Parse the returned JSON text directly into our Pydantic model
    return MockTestPayload.model_validate_json(response.text)

