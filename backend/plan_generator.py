import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_page_plan(idea, num_pages):
    instruction = f"""
You are helping design a printable coloring book.

Book idea: {idea}
Number of pages: {num_pages}

Return ONLY a JSON list of {num_pages} short image prompts.

Each prompt must describe ONE simple black-and-white coloring
page illustration, thick outlines, no shading, kid-friendly.

Make every page a different scene, no repeats.

Example format:
["a happy lion under a tree", "a giraffe eating leaves"]
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=instruction
    )

    text = response.text.strip()

    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


if __name__ == "__main__":
    idea = input("Describe your coloring book idea: ")
    pages = int(input("How many pages? "))

    prompts = generate_page_plan(idea, pages)

    for i, p in enumerate(prompts, start=1):
        print(f"{i}. {p}")