import os
import pandas as pd
from flask import Flask, render_template, request
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

# Directory where your CSV file(s) are stored
dataset_directory = 'data'

def read_movies_from_csv(directory):
    all_movies = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            all_movies.append(df)
    return pd.concat(all_movies, ignore_index=True)

# Read all movies from CSV file(s) in the directory
movies_df = read_movies_from_csv(dataset_directory)

def get_contextual_recommendations(movie_title, context, movies_df):
    filtered_movies = movies_df[movies_df['title'].str.contains(movie_title, case=False)]
    
    if context['time_of_day'] == 'evening':
        filtered_movies = filtered_movies[filtered_movies['genres'].str.contains('Comedy', case=False)]
    elif context['day_of_week'] in ['Saturday', 'Sunday']:
        filtered_movies = filtered_movies[filtered_movies['genres'].str.contains('Action', case=False)]
    
    recommendations = []
    for index, row in filtered_movies.iterrows():
        recommendation = {
            'title': row['title'],
            'budget': row['budget'],
            'homepage': row['homepage'],
            'id': row['id'],
            'original_language': row['original_language'],
            'original_title': row['original_title'],

            'runtime': row['runtime'],
            'status': row['status'],
            'tagline': row['tagline'],
            'vote_average': row['vote_average'],
            'vote_count': row['vote_count']
        }
        recommendations.append(recommendation)
    
    return recommendations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form.get('movie_title')
    if not movie_title:
        return render_template('index.html', error='Please enter a movie title.')
    
    now = datetime.now(pytz.timezone('America/New_York'))  # Adjust timezone as needed
    context = {
        'time_of_day': 'evening' if 18 <= now.hour <= 23 else 'day',
        'day_of_week': now.strftime('%A'),
        'date': now.strftime('%Y-%m-%d'),
        'location': 'New York, USA'  # Hardcoded location, can be dynamic based on IP
    }


