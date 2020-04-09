from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

def get_shows_by_genre(genre):
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(show_characters.actor_id) AS number_of_characters
    FROM shows
    INNER JOIN show_genres ON shows.id = show_genres.show_id
    INNER JOIN genres ON show_genres.genre_id = genres.id
    INNER JOIN show_characters ON shows.id = show_characters.show_id
    WHERE genres.name = %(genre)s
    GROUP BY shows.title
    ''', {'genre': genre})

def get_genres():
    return data_manager.execute_select('''
    SELECT genres.name
    FROM genres
    ORDER BY genres.name ASC;
    ''')
