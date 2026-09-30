import os
import requests
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = "generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY")
print("KEY LOADED:", bool(POLLINATIONS_API_KEY))

if not POLLINATIONS_API_KEY:
    raise RuntimeError("POLLINATIONS_API_KEY not found in .env")


def generate_image(
    prompt,
    page_number,
    print_size="letter",
    aspect_ratio="letter",
    resolution="300",
    file_format="png",
    illustration_style="clean-line-art",
    image_quality="high"
):

    full_prompt = f"""
Create a printable children's coloring book page.

Subject:
{prompt}

Print format:
- print size: {print_size}
- aspect ratio: {aspect_ratio}
- portrait orientation

Illustration style:
- {illustration_style}

Quality requirements:
- black and white line art
- clean bold outlines
- no color
- no shading
- no gray tones
- white background
- clear printable shapes
- no text
- no watermark

Quality level:
- {image_quality}
"""

    url = "https://gen.pollinations.ai/image/" + requests.utils.quote(
        full_prompt
    )

    params = {
    "model": "flux",
    "width": 1024,
    "height": 1324,
    "nologo": "true"
    }

    headers = {}

    if POLLINATIONS_API_KEY:
        headers["Authorization"] = f"Bearer {POLLINATIONS_API_KEY}"

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Image generation failed: "
            f"{response.status_code} - {response.text[:500]}"
        )

    file_path = os.path.join(
        OUTPUT_DIR,
        f"page_{page_number}.jpg"
    )

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


if __name__ == "__main__":

    test_prompt = """
    a cute astronaut puppy exploring the moon,
    with a small rocket and stars
    """

    path = generate_image(test_prompt, 1)

    print("Image generated successfully!")
    print(path)