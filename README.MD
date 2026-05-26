# 🎬 Movie Recommendation System

A comprehensive Flask-based movie recommendation system with content-based filtering, supporting Hollywood, Bollywood, and Web Series categories.

## ✨ Features

- **Smart Search**: Search across all movie categories
- **Advanced Filtering**: Filter by genre, rating, and category
- **Personalized Recommendations**: AI-powered content-based recommendations
- **Detailed Movie Information**: Cast, director, ratings, trailers, and IMDB links
- **User Session**: Personalized greeting with username
- **TMDB Integration**: Rich movie data with posters and additional details
- **Responsive Design**: Modern, mobile-friendly interface

## 🚀 Tech Stack

**Backend:**
- Flask (Python Web Framework)
- Pandas (Data Processing)
- Scikit-learn (TF-IDF Vectorizer, Cosine Similarity)
- OMDB API (Movie Data)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Font Awesome Icons

## 📁 Project Structure

```
movie-recommender/
│
├── app.py                      # Main Flask application
├── dataset.csv                 # Hollywood movies dataset
├── bollywood.csv              # Bollywood movies dataset (to be added)
├── webseries.csv              # Web series dataset (to be added)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
└── templates/
    ├── base.html             # Base template with navbar
    ├── welcome.html          # Welcome page with name input
    ├── index.html            # Landing page
    ├── category.html         # Hollywood/Bollywood/Web Series pages
    ├── search.html           # Search results page
    ├── filter.html           # Advanced filter page
    ├── movie_detail.html     # Movie details page
    └── about.html            # About page
```

## 📊 Dataset Requirements

### Current Dataset (dataset.csv)
My current `dataset.csv` should have these columns:
- `id`
- `title`
- `genre`
- `original_language`
- `overview`
- `popularity`
- `release_date`
- `vote_average`
- `vote_count`

### Recommended Datasets to Add

**1. Hollywood Movies Dataset:**
- **Source**: [Kaggle - Hollywood Movies](https://www.kaggle.com/datasets)
- **Search for**: "Hollywood movies dataset" or "Hollywood movies dataset 5000"
- **Required columns**: title, genre, overview, vote_average, vote_count
- **Save as**: `dataset.csv`

**2. Bollywood Movies Dataset:**
- **Source**: [Kaggle - Bollywood Movies](https://www.kaggle.com/datasets)
- **Search for**: "Bollywood movies dataset" or "Indian movies dataset"
- **Required columns**: title, genre, overview, vote_average, vote_count
- **Save as**: `bollywood.csv`

**3. Web Series Dataset:**
- **Source**: [Kaggle - TV Shows/Netflix Dataset](https://www.kaggle.com/datasets)
- **Search for**: "TV series dataset" or "Netflix shows dataset"
- **Popular options**:
  - Netflix Movies and TV Shows
  - TV Shows Dataset from TMDB
- **Save as**: `webseries.csv`

**Alternative**: Use TMDB API to fetch data programmatically

## 🔧 Installation & Setup

### 1. Clone or Download the Project

```bash
# Create project directory
mkdir movie-recommender
cd movie-recommender
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get TMDB API Key

1. Go to [OMDB Website](https://www.themoviedb.org/)
2. Create a free account
3. Go to Settings → API
4. Request an API key (free for non-commercial use)
5. Copy your API key


Open your browser and navigate to the URL.

## 📖 Usage Guide

### 1. **Welcome Page**
- Enter your name when prompted
- Name will be stored in session and displayed in navbar

### 2. **Home Page**
- View popular movies across all categories
- Use search bar to find specific movies

### 3. **Category Pages**
- **Hollywood**: Browse Hollywood movies
- **Bollywood**: Browse Bollywood movies
- **Web Series**: Browse web series

### 4. **Search**
- Search across all categories
- Real-time results as you type

### 5. **Filter Page**
- Filter by Genre (Drama, Action, Comedy, etc.)
- Filter by Minimum Rating (5.0+, 7.0+, 9.0+)
- Filter by Category (Hollywood, Bollywood, Web Series)

### 6. **Movie Detail Page**
- View complete movie information
- Watch trailers (YouTube)
- Visit IMDB page
- Get similar movie recommendations


### Modify Number of Recommendations

In `app.py`, change the `num_recommendations` parameter:

```python
recommendations = recommend_movies(movie_title, dataset, num_recommendations=8)
```

### Change Session Secret Key

For production, use a secure secret key in `app.py`:

```python
app.secret_key = 'your-secure-random-secret-key-here'
```

## 📝 Dataset Format Example

Your CSV files should look like this:

```csv
id,title,genre,overview,popularity,vote_average,vote_count,release_date
278,The Shawshank Redemption,"Drama,Crime","Framed in the 1940s for...",94.075,8.7,21862,1994-09-23
```

# Future Enhancements:
   - User authentication & profiles
   - Collaborative filtering
   - Movie ratings & reviews
   - Watchlist feature
   - More advanced ML models

## 📚 How the Recommendation Algorithm Works

1. **TF-IDF Vectorization**: Converts movie overviews into numerical vectors
2. **Cosine Similarity**: Calculates similarity scores between movies
3. **Ranking**: Movies with highest similarity scores are recommended
4. **Filtering**: Removes the selected movie and returns top N recommendations

# Team codeorbit_❤️
    CHETAN | PRAFULL | GIRISH | DIPALEE | VARSHA
