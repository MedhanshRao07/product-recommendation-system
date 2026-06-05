# Hybrid Ecommerce Recommendation System

## 1. Project Overview
A sophisticated, hybrid ecommerce recommendation engine that delivers highly personalized product suggestions. By combining content-based filtering (TF-IDF and Cosine Similarity) with popularity and interaction-based signals, the system mitigates the cold-start problem while providing diverse, accurate, and relevant recommendations. It is built with a modular Python/Flask backend and a modern React/Tailwind CSS frontend.

## 2. Features
- **Hybrid Recommendation Engine**: Blends content similarity (TF-IDF) with popularity and user interaction metrics for robust, multi-signal scoring.
- **Personalized Suggestions**: Analyzes aggregate user browsing history to recommend products tailored to individual preferences dynamically.
- **Cold-Start Handling**: Leverages popularity scores for new users and diverse attribute matching (category, brand, price) for new items without historical interactions.
- **Diversity Filtering**: Caps recommendations from the same brand to ensure visual and choice diversity in the generated suggestions.
- **RESTful API Architecture**: Clean, modular API endpoints for decoupled frontend-backend communication.
- **Ecommerce Functionality**: Comprehensive product catalog browsing, detailed product views, and foundational interaction tracking.
- **Modern User Interface**: Responsive, interactive, and visually appealing frontend built with React and Tailwind CSS.

## 3. Recommendation Engine Architecture
The recommendation system uses a Hybrid Scoring Model combining multiple signals to compute a final recommendation score between a source product and a candidate product. The orchestration happens in the `engine.py` module:

```math
Final Score = (0.40 \times \text{TF-IDF Similarity}) + (0.20 \times \text{Category Match}) + (0.15 \times \text{Brand Match}) + (0.10 \times \text{Price Similarity}) + (0.15 \times \text{Popularity Score})
```

- **TF-IDF & Cosine Similarity**: Extracts text features from product attributes (descriptions, names, categories) using Term Frequency-Inverse Document Frequency (TF-IDF). Cosine similarity then measures the multi-dimensional angle between these feature vectors to identify mathematically similar content.
- **Popularity-Based Recommendations**: Weighs global product interactions (e.g., views, ratings) to recommend trending and highly rated items. This is essential for handling cold-start scenarios when user history is absent.
- **Attribute Matching**: Incorporates hard and soft matching on categories, brands, and dynamic price proximity to fine-tune the final score.

## 4. Technologies Used
**Backend:**
- Python 3
- Flask (REST API Framework)
- MySQL & Flask-SQLAlchemy (Database & ORM)
- Scikit-learn & NumPy (Machine Learning & Matrix Operations)
- Flask-JWT-Extended (Authentication)

**Frontend:**
- React.js (UI Library)
- Tailwind CSS (Utility-first CSS Framework)
- Axios (HTTP Client for API Communication)
- React Router (Client-side Navigation)

## 5. Datasets Used
*Note: This project operates on a custom or synthetic ecommerce dataset. The dataset must contain primary product metadata (descriptions, prices, categories, brands) and simulated or real user interaction logs (views, clicks, ratings) for the popularity metrics to function correctly.*

## 6. System Workflow

**Backend API & Matrix Workflow:**
1. **Data Ingestion**: Products are loaded from the MySQL database into memory on startup.
2. **Model Initialization**: The `TFIDFRecommender` singleton uses `scikit-learn` to build the TF-IDF matrix lazily and computes baseline popularity scores.
3. **Request Handling**: API routes (e.g., `/api/recommendations/...`) receive context (product ID or user ID) and trigger the recommendation services.
4. **Scoring & Filtering**: The engine computes the hybrid score against all candidate products, sorts them descendingly, applies the diversity filter (max 2 items per brand), and returns the top-N results as JSON.

**Personalization Workflow:**
When a user views multiple items, the system aggregates their history, computing an average TF-IDF similarity against candidate products and blending it with global popularity scores. This ensures the feed adapts in real-time as the user navigates the store.

## 7. Folder Structure Overview
```text
product_rec/
├── backend/
│   ├── app.py                 # Flask application factory
│   ├── config.py              # Configuration variables
│   ├── database/              # DB connection and initialization
│   ├── models/                # SQLAlchemy database schema models
│   ├── recommendation/        # Core ML Models
│   │   ├── collaborative.py   # Collaborative filtering module
│   │   ├── content_based.py   # TF-IDF and Cosine Similarity logic
│   │   ├── engine.py          # Hybrid orchestrator and scoring logic
│   │   └── popularity.py      # Global scoring module
│   ├── routes/                # API endpoints and controllers
│   └── services/              # Business logic layer
├── frontend/
│   ├── package.json           # Node.js dependencies
│   ├── public/                # Static assets
│   ├── src/                   # React components, contexts, and pages
│   └── tailwind.config.js     # Tailwind styling rules
├── datasets/                  # Directory for raw and processed data
└── requirements.txt           # Python backend dependencies
```

## 8. Installation Steps

### Prerequisites
- Python 3.8+
- Node.js & npm
- MySQL Server

### Backend Setup
1. Clone the repository and navigate to the project root.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your MySQL database. Create a `.env` file inside the `backend/` directory with your database credentials (refer to `.env.example`).
5. Run the backend server:
   ```bash
   python run.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## 9. Screenshots

![Home Page Placeholder](https://via.placeholder.com/1000x500.png?text=Home+Page+with+Popularity+Recommendations)
*Figure 1: Home Page displaying popularity-based recommendations.*

![Product Detail Placeholder](https://via.placeholder.com/1000x500.png?text=Product+Detail+with+Similar+Items)
*Figure 2: Product Detail Page showing content-based similar items below the main product.*

## 10. Future Scope
- **Advanced Collaborative Filtering**: Transitioning to Matrix Factorization (SVD) or deep learning approaches (NeuMF) for more robust user-item interaction modeling.
- **Real-time Event Streaming**: Integrating Kafka or RabbitMQ to update popularity metrics dynamically based on live user clicks.
- **A/B Testing Framework**: Deploying multiple scoring weights simultaneously to optimize conversion rates dynamically in production.
- **Vector Database Integration**: Utilizing tools like Pinecone or Milvus to speed up cosine similarity computations and enable scaling to millions of products.
