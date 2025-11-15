Visual Product Matcher
AI-powered web application for finding visually similar products using deep learning.

✨ Features
📸 Image Upload: Support both file upload and image URL input

🔍 Visual Search: Find similar products using ResNet50 + FAISS

⚡ Fast: <100ms search time with FAISS vector database

📱 Mobile Responsive: Works seamlessly on all devices

🎯 Adjustable: Filter by similarity threshold

🎨 Modern UI: Clean, intuitive interface

🚀 Quick Start
Prerequisites
Python 3.8+

pip

Virtual environment (recommended)

Installation
Clone or create project

bash
mkdir visual-product-matcher
cd visual-product-matcher
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set up environment

bash
cp .env.example .env
Add product images

Place product images in data/product_images/ directory

Supports: JPG, PNG, GIF, WEBP

Generate embeddings

bash
python scripts/generate_embeddings.py
Run application

bash
python app/app.py
Access the app
Open your browser: http://localhost:5000

📁 Project Structure
text
visual-product-matcher/
├── app/                    # Flask application
│   ├── models/             # ML models
│   ├── utils/              # Utility functions
│   └── database/           # Vector database
├── static/                 # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── uploads/
├── templates/              # HTML templates
├── data/                   # Product data
│   ├── product_images/     # Product catalog
│   └── embeddings/         # FAISS index
├── scripts/                # Setup scripts
└── requirements.txt        # Dependencies
🛠️ Tech Stack
Backend
Flask 3.0.0: Web framework

PyTorch 2.1.0: Deep learning

FAISS 1.7.4: Vector search

Pillow 10.1.0: Image processing

Frontend
HTML5/CSS3: Modern web standards

Vanilla JavaScript: No dependencies

🔍 How It Works
Upload Image: User uploads product image

Feature Extraction: ResNet50 extracts 2048-dim features

Vector Search: FAISS finds similar products

Display Results: Shows matches with similarity scores

📊 API Endpoints
POST /api/upload
Upload image and get similar products

Parameters: file (multipart) or image_url

Returns: JSON with similar products

GET /api/products
Get all products in database

Returns: JSON array of products

🚢 Deployment
Vercel
bash
vercel
Netlify
bash
netlify deploy
Heroku
bash
heroku create
git push heroku main
🤝 Contributing
Fork repository

Create feature branch: git checkout -b feature/YourFeature

Commit changes: git commit -m 'Add YourFeature'

Push branch: git push origin feature/YourFeature

Open Pull Request

📄 License
MIT License - see LICENSE file

👨‍💻 Author
Your Name - GitHub

🙏 Acknowledgments
ResNet50 by Microsoft Research

FAISS by Facebook AI Research

Flask framework

PyTorch team

Built with ❤️ using Flask, PyTorch & FAISS