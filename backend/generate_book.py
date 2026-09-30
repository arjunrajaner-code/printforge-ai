import os
import glob

from plan_generator import generate_page_plan
from image_generator import generate_image


# ==========================================
# PRINTFORGE AI - BOOK GENERATOR
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

GENERATED_DIR = os.path.join(
    BASE_DIR,
    "generated"
)


# ==========================================
# CLEAN OLD GENERATED IMAGES
# ==========================================

def clean_generated_images():

    os.makedirs(
        GENERATED_DIR,
        exist_ok=True
    )

    patterns = [
        "*.png",
        "*.jpg",
        "*.jpeg"
    ]

    deleted = 0

    for pattern in patterns:

        files = glob.glob(
            os.path.join(
                GENERATED_DIR,
                pattern
            )
        )

        for file_path in files:

            try:

                os.remove(file_path)
                deleted += 1

            except Exception as e:

                print(
                    f"Could not delete {file_path}: {e}"
                )


    print(
        f"🧹 Cleaned {deleted} old image(s)."
    )


# ==========================================
# GENERATE BOOK
# ==========================================

def generate_book(
    idea,
    num_pages,
    print_size="letter",
    aspect_ratio="letter",
    resolution="300",
    file_format="png",
    illustration_style="clean-line-art",
    image_quality="high"
):

    print("\n================================")
    print("🎨 PRINTFORGE AI")
    print("================================")
    print(
        f"Idea: {idea}"
    )
    print(
        f"Pages: {num_pages}"
    )
    print("================================\n")


    # ======================================
    # CLEAN PREVIOUS BOOK
    # ======================================

    clean_generated_images()


    # ======================================
    # GENERATE PAGE PLAN
    # ======================================

    print(
        "\n🧠 Generating page plan...\n"
    )


    prompts = generate_page_plan(
        idea,
        num_pages
    )


    print(
        f"✅ Generated {len(prompts)} page prompts.\n"
    )


    successful_images = []


    # ======================================
    # GENERATE EACH IMAGE
    # ======================================

    for i, prompt in enumerate(
        prompts,
        start=1
    ):

        print(
            f"🎨 Generating page {i}/{num_pages}..."
        )

        print(
            f"Prompt: {prompt}"
        )


        try:

            path = generate_image(
                prompt,
                i,
                print_size=print_size,
                aspect_ratio=aspect_ratio,
                resolution=resolution,
                file_format=file_format,
                illustration_style=illustration_style,
                image_quality=image_quality
)


            if path and os.path.exists(path):

                successful_images.append(
                    path
                )

                print(
                    f"✅ Saved: {path}\n"
                )

            else:

                print(
                    f"⚠️ Page {i} was generated but file was not found.\n"
                )


        except Exception as e:

            print(
                f"❌ Failed page {i}: {e}\n"
            )


    # ======================================
    # RESULT
    # ======================================

    print("--------------------------------")
    print("🎨 IMAGE GENERATION COMPLETED!")
    print(
        f"Successful pages: "
        f"{len(successful_images)}/{num_pages}"
    )
    print("--------------------------------")


    if not successful_images:

        print(
            "\n❌ No images were generated."
        )

        return []


    print(
        "\n📸 Images are ready for preview!"
    )


    for i, image_path in enumerate(
        successful_images,
        start=1
    ):

        print(
            f"{i}. {image_path}"
        )


    print(
        "\n================================"
    )

    print(
        "🎉 IMAGE GENERATION COMPLETED!"
    )

    print(
        "👉 Preview images in the website."
    )

    print(
        "👉 Download individual images."
    )

    print(
        "👉 Click Create PDF when ready."
    )

    print(
        "================================\n"
    )


    return successful_images


# ==========================================
# TERMINAL MODE
# ==========================================

if __name__ == "__main__":

    idea = input(
        "Describe your coloring book idea: "
    )


    num_pages = int(
        input(
            "How many pages? "
        )
    )


    generate_book(
        idea,
        num_pages
    )