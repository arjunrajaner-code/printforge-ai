import os

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# ==========================================
# PRINTFORGE AI - PDF GENERATOR
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

GENERATED_DIR = os.path.join(
    BASE_DIR,
    "generated"
)

OUTPUT_FILE = os.path.join(
    GENERATED_DIR,
    "coloring_book.pdf"
)


# ==========================================
# CREATE PDF FROM GENERATED IMAGES
# ==========================================

def create_pdf():

    os.makedirs(
        GENERATED_DIR,
        exist_ok=True
    )


    # ======================================
    # FIND IMAGES
    # ======================================

    image_files = sorted(

        [

            f

            for f in os.listdir(
                GENERATED_DIR
            )

            if f.lower().endswith(
                (
                    ".png",
                    ".jpg",
                    ".jpeg"
                )
            )

        ]

    )


    if not image_files:

        raise Exception(
            "No coloring images found."
        )


    print(
        f"📖 Creating PDF from "
        f"{len(image_files)} images..."
    )


    # ======================================
    # CREATE PDF
    # ======================================

    pdf = canvas.Canvas(
        OUTPUT_FILE,
        pagesize=letter
    )


    page_width, page_height = letter


    margin = 35


    max_width = (
        page_width -
        (2 * margin)
    )

    max_height = (
        page_height -
        (2 * margin)
    )


    # ======================================
    # ADD EACH IMAGE
    # ======================================

    for index, image_file in enumerate(
        image_files,
        start=1
    ):

        image_path = os.path.join(
            GENERATED_DIR,
            image_file
        )


        try:

            img = Image.open(
                image_path
            )

            img_width, img_height = (
                img.size
            )


            # ==============================
            # CALCULATE FIT
            # ==============================

            scale = min(

                max_width / img_width,

                max_height / img_height

            )


            new_width = (
                img_width * scale
            )

            new_height = (
                img_height * scale
            )


            # ==============================
            # CENTER IMAGE
            # ==============================

            x = (
                page_width -
                new_width
            ) / 2


            y = (
                page_height -
                new_height
            ) / 2


            # ==============================
            # DRAW IMAGE
            # ==============================

            pdf.drawImage(

                image_path,

                x,

                y,

                width=new_width,

                height=new_height,

                preserveAspectRatio=True,

                anchor="c"

            )


            pdf.showPage()


            print(
                f"✅ Added page {index}: "
                f"{image_file}"
            )


        except Exception as e:

            print(
                f"❌ Could not add "
                f"{image_file}: {e}"
            )


    # ======================================
    # SAVE PDF
    # ======================================

    pdf.save()


    print(
        "\n🎉 PDF CREATED SUCCESSFULLY!"
    )

    print(
        f"📄 Saved: {OUTPUT_FILE}"
    )


    return OUTPUT_FILE


# ==========================================
# TEST PDF GENERATOR
# ==========================================

if __name__ == "__main__":

    create_pdf()