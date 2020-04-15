from builtins import type

from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')

# 1.) List all shows and the number of episodes for each show.
# group by always based on id, not title (because id is unique, title can be ambigous)
def get_all_shows_and_episodes():
    return data_manager.execute_select('''
    SELECT COUNT(shows.id) AS count_of_episodes, shows.title
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY shows.title ASC;
    ''')

# 2.) List the top 10 actors who played the most characters.
def top_ten_actors_most_characters():
    return data_manager.execute_select('''
    SELECT actors.name, COUNT(actors.id) AS count_of_characters
    FROM actors
    INNER JOIN show_characters ON actors.id = show_characters.actor_id
    GROUP BY actors.id
    ORDER BY count_of_characters DESC 
    LIMIT 10;
    ''')
# group by only possible by PRIMARY KEY???

# 3.) Search shows which have minimum the given amount of [seasons] and/or [episodes].
# Modify your previous page and query to display the number of shows matching the search grouped by genres.
def get_all_shows_and_episodes(min_seasons, min_episodes):
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.season_id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    HAVING COUNT(DISTINCT seasons.id) >= %(min_seasons)s OR COUNT(episodes.season_id) >= %(min_episodes)s
    ORDER BY shows.title ASC;
    ''', {
        'min_seasons': min_seasons,
        'min_episodes': min_episodes
    })



# 1.) List the top 10 rated shows which implements the given [genre]! Display the shows title,
# starting date and rating in an ordered list.
def top_shows_by_genre(genre):
    data_manager.execute_select('''
    SELECT shows.title, ROUND(shows.rating, 2), shows.year
    FROM shows
    INNER JOIN show_genres ON shows.id = show_genres.show_id
    INNER JOIN genres ON show_genres.genre_id = genres.id
    WHERE genres.name LIKE %(genre)s
    ORDER BY shows.rating DESC
    LIMIT 10;
    ''')


# 2.) List all years between 1970 and 2010. Add a column of average rating of all shows started
# that year. Also add a column containing the number of shows started that year.
def get_shows_in_years(years_from, year_to):
    return data_manager.execute_select('''
    SELECT EXTRACT(YEAR from year) AS year, ROUND(AVG(rating), 2) AS rating, COUNT(shows.id) AS show_id
    FROM shows
    WHERE EXTRACT(YEAR from year) BETWEEN %(from)s AND %(to)s
    GROUP BY year
    ORDER BY year
    ''', {
        'from': years_from,
        'to': year_to
    })

# 3.) List the top 10 longest shows by total runtime (how long would it take to watch all episodes)
#  Collect all actors played in these shows ordered by name [separate query]
def get_longest_shows():
    data_manager.execute_select('''
    SELECT shows.title, COUNT(episodes.id) * shows.runtime AS total_runtime
    FROM shows
    JOIN seasons ON shows.id = seasons.show_id
    JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY runtime DESC
    LIMIT 10;
    ''')


def get_all_actors_in_longest_shows():
    data_manager.execute_select('''
    SELECT DISTINCT actors.name
    FROM shows
    INNER JOIN show_characters ON shows.id = show_characters.show_id
    INNER JOIN actors ON show_characters.actor_id = actors.id;
    ''')

# 4.)  List all shows containing the given [search string].
def search_by_title(title: str):
    return data_manager.execute_select('''
    SELECT *
    FROM shows
    WHERE title ILIKE %(title)s
    ''', {'title': title})



# 5.) Collect all actors with their name, age (or age at death, if deceased) and number
# of shows the actor played in. Order the most active actor on top of the result.
def get_all_actors():
    return data_manager.execute_select('''
    SELECT COUNT(show_characters.actor_id) AS number_of_shows, actors.name
    FROM show_characters
    INNER JOIN actors ON show_characters.actor_id = actors.id
    INNER JOIN shows ON show_characters.show_id = shows.id
    GROUP BY actors.name
    ORDER BY number_of_shows DESC;
    ''')

def get_all_actors():
    return data_manager.execute_select('''
    SELECT COUNT(show_characters.actor_id) AS number_of_shows, actors.name, 
    CASE 
        WHEN actors.death IS NOT NULL THEN DATE_PART('year', actors.death) - DATE_PART('year', actors.birthday)
        ELSE CURRENT_DATE('year') - DATE_PART('year', actors.birthday)
    END AS age
    FROM show_characters
    INNER JOIN actors ON show_characters.actor_id = actors.id
    INNER JOIN shows ON show_characters.show_id = shows.id
    GROUP BY actors.id
    ORDER BY number_of_shows DESC;
    ''')


# 6.) List all actors' name and birthday, who were born after “[year]-01-01”. For every
# actor list a number which means how many characters they played. For every actor list
# their shows' average rating.

def get_actors_birthday_characters_rating(year):
    return data_manager.execute_select('''
    SELECT actors.name, actors.birthday, COUNT(show_characters.id) AS number_of_characters, ROUND((AVG(shows.rating)), 2) AS rating
    FROM actors
    INNER JOIN show_characters ON actors.id = show_characters.actor_id
    INNER JOIN shows ON shows.id = show_characters.show_id
    WHERE DATE_PART('year', actors.birthday) > %(year)s
    GROUP BY actors.id
    ORDER BY actors.birthday ASC;
    ''', {'year': year})



 # 7.) List all shows using the given [genre].
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



# 8.) List all actors name and age, who played in shows released in the given [year].
# Order them by age, and the older person should be on the top.

def get_actors_name_age_in_shows_released_given_year(released_year):
    return data_manager.execute_select('''
    SELECT shows.title, shows.year AS released_year, actors.name, 
    CASE 
        WHEN actors.death IS NOT NULL THEN DATE_PART('year', actors.death) - DATE_PART('year', actors.birthday)
        ELSE 2020 - DATE_PART('year', actors.birthday)
    END AS age
    FROM shows
    INNER JOIN show_characters ON shows.id = show_characters.show_id
    INNER JOIN actors ON show_characters.actor_id = actors.id
    WHERE DATE_PART('year', shows.year) = %(year)s
    ''', {
        'released_year': released_year
    })




# 9.)  Query the characters matching the modified input.
# Extend the query with some more details: Title of the show and the real name of the actor

# 10.) Calculate the highest number of seasons the database knows about.
# Python/Jinja: Add a range input to the top of default index page, above the list of shows. It should allow the
# user to select a value between 1 and the highest season number.
def get_highest_number_of_seasons(range_input):
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(*) as number_of_seasons
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    GROUP BY shows.id
    HAVING COUNT(*) <= %(range_input)s
    ORDER BY number_of_seasons DESC;
    ''', {
        'range_input': range_input
          })


# 11.) Write a query that lists 50 shows from a genre (by [genre.id]) that have the most,
# but at least 20 episodes, ordered by the count of episodes.

def get_all_genres():
    return data_manager.execute_select('''
    SELECT genres.name, genres.id
    FROM genres
    ''')

def get_shows_by_genre_most_episodes(genre_id):
    return data_manager.execute_select('''
    SELECT shows.title, MAX(seasons.season_number) as seasons, COUNT(*) as episodes
    FROM shows
    INNER JOIN show_genres ON shows.id = show_genres.show_id
    INNER JOIN genres ON show_genres.genre_id = genres.id
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    WHERE genres.id = %(genre_id)s
    GROUP BY shows.id, genres.id
    HAVING COUNT(*) > 20
    ORDER BY episodes DESC
    LIMIT 50;
    ''', {
        'genre_id': genre_id
    })




# 12.) create a query to get the {shows/seasons/episodes} in a proper order from the database.
def get_shows_seasons_episodes_by_title_asc():
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY shows.title ASC;
    ''')

def get_shows_seasons_episodes_by_title_desc():
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY shows.title DESC;
    ''')

def get_shows_seasons_episodes_by_seasons_asc():
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY number_of_seasons ASC;
    ''')

def get_shows_seasons_episodes_by_seasons_desc():
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY number_of_seasons DESC;
    ''')

def get_shows_seasons_episodes_by_episodes_asc():
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY number_of_episodes ASC;
    ''')

def get_shows_seasons_episodes_by_episodes_desc():
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY number_of_episodes DESC;
    ''')

def get_shows_seasons_episodes_parametrizes():
    return data_manager.execute_select('''
    SELECT shows.title, COUNT(DISTINCT seasons.id) AS number_of_seasons, COUNT(episodes.id) AS number_of_episodes
    FROM shows
    INNER JOIN seasons ON shows.id = seasons.show_id
    INNER JOIN episodes ON seasons.id = episodes.season_id
    GROUP BY shows.id
    ORDER BY  
        CASE 
            WHEN THEN shows.title
        END ASC,
        CASE
            WHEN %(order)s THEN shows.title
        END DESC 
    ''')











