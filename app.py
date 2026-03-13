from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_it'

OMDB_API_KEY = 'YOUR_API_KEY' 
OMDB_BASE_URL = 'http://www.omdbapi.com/'

# Load datasets
def load_datasets():
    hollywood_df = pd.read_csv('dataset.csv')
    
    # For now, using hollywood dataset as template
    # You'll replace these with actual Bollywood and Web Series datasets
    try:
        bollywood_df = pd.read_csv('bollywood.csv')
    except FileNotFoundError:
        bollywood_df = pd.DataFrame()
    
    try:
        webseries_df = pd.read_csv('webseries.csv')
    except FileNotFoundError:
        webseries_df = pd.DataFrame()
    
    return hollywood_df, bollywood_df, webseries_df

hollywood_movies, bollywood_movies, webseries = load_datasets()

# Combine all datasets for search and filter
def get_all_movies():
    dfs = []
    if not hollywood_movies.empty:
        hollywood_copy = hollywood_movies.copy()
        hollywood_copy['category'] = 'Hollywood'
        dfs.append(hollywood_copy)
    if not bollywood_movies.empty:
        bollywood_copy = bollywood_movies.copy()
        bollywood_copy['category'] = 'Bollywood'
        dfs.append(bollywood_copy)
    if not webseries.empty:
        webseries_copy = webseries.copy()
        webseries_copy['category'] = 'Web Series'
        dfs.append(webseries_copy)
    
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# Get movie details from OMDb API
def get_omdb_details(movie_title):
    try:
        url = OMDB_BASE_URL
        params = {
            'apikey': OMDB_API_KEY,
            't': movie_title,
            'plot': 'full'
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('Response') == 'True':
            # Extract relevant information
            poster = data.get('Poster') if data.get('Poster') != 'N/A' else None
            
            # Parse cast (Actors field)
            cast = data.get('Actors', '').split(', ')[:5] if data.get('Actors') != 'N/A' else []
            
            # Get director
            director = data.get('Director', 'N/A')
            
            # Get IMDB link
            imdb_id = data.get('imdbID')
            imdb_link = f"https://www.imdb.com/title/{imdb_id}" if imdb_id else None
            
            # Get runtime (convert "142 min" to 142)
            runtime_str = data.get('Runtime', 'N/A')
            runtime = int(runtime_str.split()[0]) if runtime_str != 'N/A' and runtime_str.split()[0].isdigit() else None
            
            # Get release date
            release_date = data.get('Released', 'N/A')
            
            return {
                'poster': poster,
                'cast': cast,
                'director': director,
                'imdb_link': imdb_link,
                'runtime': runtime,
                'release_date': release_date,
                'plot': data.get('Plot', ''),
                'rated': data.get('Rated', 'N/A'),
                'awards': data.get('Awards', 'N/A'),
                'trailer': None  # OMDb doesn't provide trailers
            }
    except Exception as e:
        print(f"OMDb API Error: {e}")
    
    return None

# Content-based recommendation
def recommend_movies(movie_title, dataset, num_recommendations=8):
    if dataset.empty or movie_title not in dataset['title'].values:
        return []
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(dataset['overview'].fillna(''))
    
    movie_idx = dataset[dataset['title'] == movie_title].index[0]
    similarity_scores = cosine_similarity(tfidf_matrix[movie_idx], tfidf_matrix).flatten()
    
    similar_idx = similarity_scores.argsort()[-(num_recommendations + 1):-1][::-1]
    recommendations = dataset.iloc[similar_idx][['title', 'genre']].to_dict('records')
    
    # Add posters
    for movie in recommendations:
        omdb_data = get_omdb_details(movie['title'])
        movie['poster'] = omdb_data['poster'] if omdb_data else None
    
    return recommendations

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    # Get popular movies for landing page
    all_movies = get_all_movies()
    if not all_movies.empty and 'popularity' in all_movies.columns:
        popular = all_movies.nlargest(12, 'popularity')[['title', 'genre', 'vote_average', 'category']].to_dict('records')
        
        for movie in popular:
            omdb_data = get_omdb_details(movie['title'])
            movie['poster'] = omdb_data['poster'] if omdb_data else None
    else:
        popular = []
    
    return render_template('index.html', movies=popular, username=session.get('username'))

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('welcome.html')

@app.route('/hollywood')
def hollywood():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    movies = hollywood_movies.head(20)[['title', 'genre', 'vote_average']].to_dict('records')
    
    for movie in movies:
        omdb_data = get_omdb_details(movie['title'])
        movie['poster'] = omdb_data['poster'] if omdb_data else None
    
    return render_template('category.html', movies=movies, category='Hollywood', username=session.get('username'))

@app.route('/bollywood')
def bollywood():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    if bollywood_movies.empty:
        return render_template('category.html', movies=[], category='Bollywood', 
                             message="Bollywood dataset coming soon!", username=session.get('username'))
    
    movies = bollywood_movies.head(20)[['title', 'genre', 'votes']].to_dict('records')
    
    for movie in movies:
        omdb_data = get_omdb_details(movie['title'])
        movie['poster'] = omdb_data['poster'] if omdb_data else None
    
    return render_template('category.html', movies=movies, category='Bollywood', username=session.get('username'))

@app.route('/webseries')
def web_series():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    if webseries.empty:
        return render_template('category.html', movies=[], category='Web Series', 
                             message="Web Series dataset coming soon!", username=session.get('username'))
    
    series = webseries.head(20)[['title', 'genre', 'vote_count']].to_dict('records')
    
    for show in series:
        omdb_data = get_omdb_details(show['title'])
        show['poster'] = omdb_data['poster'] if omdb_data else None
    
    return render_template('category.html', movies=series, category='Web Series', username=session.get('username'))

@app.route('/search')
def search():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    query = request.args.get('q', '').lower()
    all_movies = get_all_movies()
    
    if query and not all_movies.empty:
        results = all_movies[all_movies['title'].str.lower().str.contains(query, na=False)]
        movies = results[['title', 'genre', 'vote_average', 'category']].head(20).to_dict('records')
        
        for movie in movies:
            omdb_data = get_omdb_details(movie['title'])
            movie['poster'] = omdb_data['poster'] if omdb_data else None
    else:
        movies = []
    
    return render_template('search.html', movies=movies, query=query, username=session.get('username'))


@app.route('/filter')
def filter_movies():
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    all_movies = get_all_movies()
    
    # Get filter parameters
    genre = request.args.get('genre', '')
    min_rating_str = request.args.get('min_rating')
    category = request.args.get('category', '')
    
    filtered = all_movies.copy()
    
    if genre and 'genre' in filtered.columns:
        filtered = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]
    
    if min_rating_str and 'vote_average' in filtered.columns:
        try:
            min_rating = float(min_rating_str)
            numeric_vote_average = pd.to_numeric(filtered['vote_average'], errors='coerce')
            filtered = filtered[numeric_vote_average >= min_rating]
        except(ValueError, TypeError):
            pass
    
    if category and category.strip() and 'category' in filtered.columns:
        filtered = filtered[filtered['category'] == category]
    
    movies = filtered[['title', 'genre', 'vote_average', 'category']].head(20).to_dict('records')
    
    for movie in movies:
        omdb_data = get_omdb_details(movie['title'])
        movie['poster'] = omdb_data['poster'] if omdb_data else None
    
    # --- HERE IS THE KEY CHANGE FOR THE NEW ERROR ---
    # Ensure the genre column is all strings before processing
    if 'genre' in all_movies.columns:
        all_movies['genre'] = all_movies['genre'].astype(str)
        genres = sorted(all_movies['genre'].str.split(',').explode().str.strip().unique().tolist())
    else:
        genres = []
    # --- END OF KEY CHANGE ---
    
    return render_template('filter.html', movies=movies, genres=genres, username=session.get('username'))

@app.route('/movie/<path:movie_title>')
def movie_detail(movie_title):
    if 'username' not in session:
        return redirect(url_for('welcome'))
    
    all_movies = get_all_movies()
    movie_data = all_movies[all_movies['title'] == movie_title]
    
    if movie_data.empty:
        return "Movie not found", 404
    
    movie = movie_data.iloc[0].to_dict()
    
    # Get OMDb details
    omdb_data = get_omdb_details(movie_title)
    if omdb_data:
        movie.update(omdb_data)
    
    # Get recommendations
    category = movie.get('category', 'Hollywood')
    dataset = pd.DataFrame() # Initialize an empty DataFrame    
    if category == 'Hollywood':
        dataset = hollywood_movies
    elif category == 'Bollywood':
        dataset = bollywood_movies
    else:
        dataset = webseries
    
    recommendations = recommend_movies(movie_title, dataset, num_recommendations=6)
    
    return render_template('movie_detail.html', movie=movie, recommendations=recommendations, username=session.get('username'))


@app.route('/recommend')
def recommend():
    if 'username' not in session:
        return redirect(url_for('welcome'))

    query = request.args.get('q', '')
    recommendations = []
    
    if query:
        all_movies = get_all_movies()
        # Find the movie in the combined dataset
        movie_data = all_movies[all_movies['title'].str.lower() == query.lower()]

        if not movie_data.empty:
            movie_title = movie_data.iloc[0]['title']
            # Get the category to use the correct dataset for recommendations
            category = movie_data.iloc[0].get('category', 'Hollywood')
            
            if category == 'Hollywood':
                dataset = hollywood_movies
            elif category == 'Bollywood':
                dataset = bollywood_movies
            else:
                dataset = webseries
            
            recommendations = recommend_movies(movie_title, dataset, num_recommendations=12)

    return render_template('recommendations.html', recommendations=recommendations, query=query, username=session.get('username'))

@app.context_processor
def inject_current_path():
    return {'current_path': request.path}


@app.route('/about')
def about():
    return render_template('about.html', username=session.get('username', ''))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
