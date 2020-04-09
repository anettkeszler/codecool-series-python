from flask import Flask, render_template, url_for, request
from data import queries

app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/get-shows-by-genre', methods=['GET', 'POST'])
def get_shows_by_genre():
    options = queries.get_genres()
    if request.method == 'POST':
        genre = request.form['genre-input']
        genres = queries.get_shows_by_genre(genre)
        return render_template('get-shows-by-genre.html', options=options, genres=genres)

    return render_template('get-shows-by-genre.html', options=options)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
