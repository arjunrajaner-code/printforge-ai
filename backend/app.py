import re

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import os

from generate_book import generate_book
from pdf_generator import create_pdf


# ==========================================
# PRINTFORGE AI - BACKEND
# IMAGE PREVIEW + IMAGE DOWNLOAD + PDF
# ==========================================

app = Flask(__name__)
CORS(app)


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

GENERATED_DIR = os.path.join(
    BASE_DIR,
    "generated"
)


# Create generated folder if it doesn't exist
os.makedirs(
    GENERATED_DIR,
    exist_ok=True
)


# ==========================================
# HOME / FRONTEND
# ==========================================

@app.route("/")
def home():

    return send_file(
        os.path.join(
            FRONTEND_DIR,
            "index.html"
        )
    )


# ==========================================
# FRONTEND FILES
# ==========================================

@app.route("/<path:filename>")
def frontend_files(filename):

    file_path = os.path.join(
        FRONTEND_DIR,
        filename
    )

    if os.path.isfile(file_path):

        return send_file(
            file_path
        )

    return jsonify({
        "error": "File not found"
    }), 404


# ==========================================
# GENERATE COLORING BOOK IMAGES
# ==========================================

@app.route(
    "/generate",
    methods=["POST"]
)
def generate():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400


        idea = data.get(
            "idea",
            ""
        ).strip()

        print_size = data.get("printSize", "letter")
        aspect_ratio = data.get("aspectRatio", "letter")
        resolution = data.get("resolution", "300")
        file_format = data.get("fileFormat", "png")
        illustration_style = data.get("illustrationStyle", "clean-line-art")
        image_quality = data.get("imageQuality", "high")


        import re

        page_patterns = [
            r'\b(\d+)\s*[-]?\s*pages?\b',
            r'\b(\d+)\s+coloring\s+pages?\b',
            r'\bpages?\s*[:=]\s*(\d+)\b'
        ]

        page_match = None

        for pattern in page_patterns:
            page_match = re.search(pattern, idea, re.IGNORECASE)
            if page_match:
                break

        if not page_match:
            return jsonify({
                "success": False,
                "error": "Please specify the number of pages in your prompt. Example: Create a 3-page coloring book."
            }), 400

        pages = int(page_match.group(1))


        # ==================================
        # VALIDATE IDEA
        # ==================================

        if not idea:

            return jsonify({
                "success": False,
                "error":
                    "Please enter a coloring book idea."
            }), 400


        # ==================================
        # VALIDATE PAGE COUNT
        # ==================================

        if pages < 1 or pages > 36:

            return jsonify({
                "success": False,
                "error":
                    "Pages must be between 1 and 36."
            }), 400


        print("\n================================")
        print("🎨 PRINTFORGE AI")
        print("================================")
        print(f"Idea: {idea}")
        print(f"Pages: {pages}")
        print("================================\n")


        # ==================================
        # GENERATE IMAGES
        # ==================================

        generate_book(
    idea,
    pages,
    print_size=print_size,
    aspect_ratio=aspect_ratio,
    resolution=resolution,
    file_format=file_format,
    illustration_style=illustration_style,
    image_quality=image_quality
)


        # ==================================
        # FIND GENERATED IMAGES
        # ==================================

        image_files = sorted(

            [

                file

                for file in os.listdir(
                    GENERATED_DIR
                )

                if file.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg"
                    )
                )

            ]

        )


        if not image_files:

            return jsonify({
                "success": False,
                "error":
                    "No images were generated."
            }), 500


        # ==================================
        # CREATE IMAGE URL LIST
        # ==================================

        image_urls = [

            f"/images/{filename}"

            for filename in image_files

        ]


        print(
            f"Generated images: {len(image_urls)}"
        )


        # ==================================
        # RETURN IMAGES TO FRONTEND
        # ==================================

        return jsonify({

            "success": True,

            "message":
                "Images generated successfully!",

            "images":
                image_urls,

            "count":
                len(image_urls)

        })


    except Exception as e:

        print("\n❌ GENERATION ERROR:")
        print(e)


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ==========================================
# SERVE GENERATED IMAGES
# ==========================================

@app.route(
    "/images/<filename>"
)
def serve_image(filename):

    return send_from_directory(

        GENERATED_DIR,

        filename

    )


# ==========================================
# CREATE PDF
# ==========================================

@app.route(
    "/create-pdf",
    methods=["POST"]
)
def create_pdf_route():

    try:

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No image data received."

            }), 400


        # ==================================
        # GET IMAGE LIST
        # ==================================

        images = data.get(
            "images",
            []
        )


        if not images:

            return jsonify({

                "success": False,

                "error":
                    "No images available for PDF."

            }), 400


        print("\n================================")
        print("📖 CREATING PDF")
        print("================================")
        print(
            f"Images: {len(images)}"
        )
        print("================================\n")


        # ==================================
        # CREATE PDF
        # ==================================

        create_pdf()


        # ==================================
        # CHECK PDF
        # ==================================

        pdf_path = os.path.join(

            GENERATED_DIR,

            "coloring_book.pdf"

        )


        if not os.path.exists(
            pdf_path
        ):

            return jsonify({

                "success": False,

                "error":
                    "PDF was not created."

            }), 500


        print(
            "\n🎉 PDF CREATED SUCCESSFULLY!\n"
        )


        return jsonify({

            "success": True,

            "message":
                "PDF created successfully!",

            "pdf_url":
                "/download/coloring_book.pdf"

        })


    except Exception as e:

        print("\n❌ PDF ERROR:")
        print(e)


        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ==========================================
# DOWNLOAD PDF
# ==========================================

@app.route(
    "/download/<filename>"
)
def download(filename):

    return send_from_directory(

        GENERATED_DIR,

        filename,

        as_attachment=True

    )


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print("\n================================")
    print("🎨 PRINTFORGE AI")
    print("🚀 Backend Server Starting...")
    print("================================")
    print(
        "🌐 http://127.0.0.1:5000"
    )
    print("================================\n")


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False

    )