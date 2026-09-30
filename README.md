# 🎨 PrintForge AI

AI-powered coloring book generator using Google Gemini and Pollinations AI.

## ✨ Features

- 📝 Generate coloring-book page prompts from a single idea
- 🎨 AI-generated black-and-white coloring pages
- 📄 Custom page count through the prompt
- 🖼️ Printable portrait images
- ⚙️ Image settings for print size, aspect ratio, resolution, format, style, and quality
- 📚 Generate complete coloring books
- 📥 Download generated images
- 📕 Create and download coloring-book PDF
- 🌙 Premium dark AI-studio interface
- 🔐 Environment-based API key protection

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS
- Google Gemini API
- Pollinations AI
- Pillow
- ReportLab

## 📁 Project Structure

```text
printforge-ai/
│
├── backend/
│   ├── app.py
│   ├── generate_book.py
│   ├── image_generator.py
│   ├── pdf_generator.py
│   └── plan_generator.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── prompts/
├── requirements.txt
├── .gitignore
└── README.md
🚀 Setup
1. Clone the repository
git clone https://github.com/arjunrajaner-code/printforge-ai.git
cd printforge-ai
2. Create virtual environment
python -m venv venv
3. Activate virtual environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Create .env

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
POLLINATIONS_API_KEY=your_pollinations_api_key

Never upload .env or API keys to GitHub.

6. Run the application
python -u backend/app.py

Then open:

http://127.0.0.1:5000
🎯 Example Prompt
Create a 10-page cute puppy adventure coloring book.

PrintForge AI extracts the page count from the prompt, generates page ideas using Gemini, and generates the coloring-page images using Pollinations AI.

🔑 API Requirements

PrintForge AI currently uses:

Google Gemini API — page prompt planning
Pollinations AI API — image generation

API keys must be stored in .env.

📌 Project Status

🚧 Currently under active development.

Future improvements include:

User authentication
Database integration
Project history
Cloud deployment
More image-generation controls
Improved PDF customization
👨‍💻 Author

Arjun Rajan E

GitHub: https://github.com/arjunrajaner-code# 🎨 PrintForge AI

AI-powered coloring book generator using Google Gemini and Pollinations AI.

## ✨ Features

- 📝 Generate coloring-book page prompts from a single idea
- 🎨 AI-generated black-and-white coloring pages
- 📄 Custom page count through the prompt
- 🖼️ Printable portrait images
- ⚙️ Image settings for print size, aspect ratio, resolution, format, style, and quality
- 📚 Generate complete coloring books
- 📥 Download generated images
- 📕 Create and download coloring-book PDF
- 🌙 Premium dark AI-studio interface
- 🔐 Environment-based API key protection

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask
- Flask-CORS
- Google Gemini API
- Pollinations AI
- Pillow
- ReportLab

## 📁 Project Structure

```text
printforge-ai/
│
├── backend/
│   ├── app.py
│   ├── generate_book.py
│   ├── image_generator.py
│   ├── pdf_generator.py
│   └── plan_generator.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── prompts/
├── requirements.txt
├── .gitignore
└── README.md
🚀 Setup
1. Clone the repository
git clone https://github.com/arjunrajaner-code/printforge-ai.git
cd printforge-ai
2. Create virtual environment
python -m venv venv
3. Activate virtual environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Create .env

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key
POLLINATIONS_API_KEY=your_pollinations_api_key

Never upload .env or API keys to GitHub.

6. Run the application
python -u backend/app.py

Then open:

http://127.0.0.1:5000
🎯 Example Prompt
Create a 10-page cute puppy adventure coloring book.

PrintForge AI extracts the page count from the prompt, generates page ideas using Gemini, and generates the coloring-page images using Pollinations AI.

🔑 API Requirements

PrintForge AI currently uses:

Google Gemini API — page prompt planning
Pollinations AI API — image generation

API keys must be stored in .env.

📌 Project Status

🚧 Currently under active development.

Future improvements include:

User authentication
Database integration
Project history
Cloud deployment
More image-generation controls
Improved PDF customization
👨‍💻 Author

Arjun Rajan E

GitHub: https://github.com/arjunrajaner-code
