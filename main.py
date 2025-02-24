from flask import Flask, render_template, request
import sqlite3



class Movie:
    def __init__(self, id, title, year, genres, country, description, duration, rating, age_rating, poster):
        self.id = id
        self.title = title
        self.year = year
        self.genres = genres
        self.country = country
        self.description = description
        self.duration = duration
        self.rating = rating
        self.age_rating = age_rating
        self.poster = poster



app = Flask(__name__)



db_name = "./films.db"

def get_films_lists(page = 1, offset = 25, limit = 25):
    con = sqlite3.connect(db_name)


    SQL = """

        SELECT * FROM movie
        LIMIT ?
        OFFSET ?
    """

    q = con.execute(SQL,[ limit, (offset *( page - 1) )])
    data = q.fetchall()
    return [Movie(*row) for row in data]




def get_films_by_search(search):
    con = sqlite3.connect(db_name)


    SQL = f"""

        SELECT * FROM movie where title like '%{search}%' or country like '%{search}%' or genres like '%{search}%'
    """

    q = con.execute(SQL)
    data = q.fetchall()
    return [Movie(*row) for row in data]



def get_film(film_id):
    con = sqlite3.connect(db_name)

    SQL = """

        SELECT * FROM movie
        where id = ?
    """

    q = con.execute(SQL, [film_id])
    data = q.fetchone()
    return Movie(*data)


@app.route("/")
@app.route("/pages/<int:page>")
def index_page(page=1):
    films = get_films_lists(page)
    return render_template("index.html", films = films, page=page )


@app.route("/films/<int:film_id>")
def film_page(film_id):
    film = get_film(film_id)
    return render_template("film.html", film = film)


@app.route('/search', methods=["POST"])
def search_page():
    search = request.form.get("search")
    films = get_films_by_search(search)
    return render_template("search.html", films = films, search = search)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
