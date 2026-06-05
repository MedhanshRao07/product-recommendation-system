# 🛍️ Suggestify — AI-Powered Product Recommendation System

Suggestify is a full-stack web application built with a Flask backend, a modern React frontend (Neobrutalism design), and a MySQL database. It features a complete ML-based hybrid recommendation system using TF-IDF and collaborative filtering.

## 📁 Project Structure

```
product_rec/
├── backend/               # Flask API (Routes, Services, DB connection)
│   └── recommendation/    # TF-IDF ML Engine
├── frontend/              # React App (Tailwind CSS, Context API)
├── datasets/              # CSVs and Database Schema
├── scripts/               # Data generation and seeding scripts
├── run.py                 # 🚀 One-command launcher
├── requirements.txt       # Python dependencies
└── .env.example           # Example environment variables
```

## 🚀 Quick Start (One Command)

We've bundled everything into a single launcher script that handles dependencies, virtual environments, and starting the servers.

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd product_rec
   ```

2. **Configure Environment:**
   ```bash
   # Copy the example env file and update your MySQL credentials
   cp .env.example backend/.env
   ```

3. **Seed Database:**
   Ensure MySQL is running, create a database called `suggestify_db`, and then run:
   ```bash
   python scripts/seed_database.py
   ```

4. **Run the App:**
   ```bash
   # Start everything (installs dependencies on first run)
   python run.py
   ```
   
   The backend will be available at `http://localhost:5000` and the frontend at `http://localhost:3000`.

## 🛠️ Launcher Options

You can manage the services individually using the launcher:
- `python run.py --backend` (Start backend only)
- `python run.py --frontend` (Start frontend only)
- `python run.py --check` (Check dependencies)
- `python run.py --install` (Install all dependencies)

## 🧠 Recommendation Engine

Suggestify uses a **Hybrid Recommendation Strategy**:
1. **Behavioral Tracking**: Logs clicks, views, searches, and purchases.
2. **Collaborative Filtering**: Analyzes item-item co-occurrence based on overall user activity patterns.
3. **Machine Learning (TF-IDF)**: Content-based filtering using cosine similarity on product metadata (tags, features, brand).
4. **Ensemble Scoring**: Combines CF, Content, Behavior, and Popularity scores into a single confidence metric.

## ✨ New Features
* **AI Shopping Assistant**: Powered by Google Gemini, the chatbot can answer product queries and directly recommend real products from the catalog.
* **Real Comparisons**: Direct outbound search links to real marketplaces like Amazon, Flipkart, and Myntra.
* **Neobrutalism UI**: A bold, high-contrast user interface that stands out.

## 🧑‍💻 Contributing
This project is structured for easy collaboration. Keep your frontend components in `frontend/src/components/`, API logic in `backend/services/`, and ML updates in `backend/recommendation/`.
