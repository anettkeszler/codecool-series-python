from flask import Flask, render_template, url_for, request
from data import queries
import json


app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/genrestic', methods=['GET', 'POST'])
def get_shows_by_genre():
    options = queries.get_genres()
    if request.method == 'POST':
        genre = request.form['genre-input']
        genres = queries.get_shows_by_genre(genre)
        return render_template('genrestic.html', options=options, genres=genres)

    return render_template('genrestic.html', options=options)


@app.route('/longest_shows_in_a_genre')
def get_longest_shows_by_genre():
    genres = queries.get_all_genres()
    return render_template('longest_shows_in_a_genre.html', genres=genres)

@app.route('/genres/<genre_id>')
def get_genres(genre_id):
    genre = json.dumps(queries.get_shows_by_genre_most_episodes(genre_id))
    return genre


@app.route('/nice-list-of-avg-actors', methods=['POST', 'GET'])
def get_actors_birthday_characters_rating():
    if request.method == 'POST':
        birthday = request.form['year-input']
        actors = queries.get_actors_birthday_characters_rating(birthday)
        return render_template('nice_list_of_avg_actors.html', actors=actors, birthday=birthday)


    return render_template('nice_list_of_avg_actors.html')

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
