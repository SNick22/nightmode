# необходимые импорты
import datetime

from flask import Flask, render_template, request, make_response, session, redirect

# инициализируем приложение
# из документации:
#     The flask object implements a WSGI application and acts as the central
#     object.  It is passed the name of the module or package of the
#     application.  Once it is created it will act as a central registry for
#     the view functions, the URL rules, template configuration and much more.
from db_util import Database

app = Flask(__name__)

# нужно добавить секретный код - только с ним можно менять данные сессии
app.secret_key = "111"

# необходимо добавлять, чтобы время сессии не ограничивалось закрытием браузера
app.permanent_session_lifetime = datetime.timedelta(days=365)

# инициализация класса с методами для работы с БД
db = Database()

# дальше реализуем методы, которые мы можем выполнить из браузера,
# благодаря указанным относительным путям


# метод для создания куки
@app.route("/add_cookie")
def add_cookie():
    resp = make_response("Add cookie")
    resp.set_cookie("test", "val")
    return resp


# метод для удаления куки
@app.route("/delete_cookie")
def delete_cookie():
    resp = make_response("Delete cookie")
    resp.set_cookie("test", "val", 0)


# реализация визитов
@app.route("/visits")
def visits():
    visits_count = session['visits'] if 'visits' in session.keys() else 0
    session['visits'] = visits_count + 1

    return f"Количество визитов: {session['visits']}"


# удаление данных о посещениях
@app.route("/delete_visits")
def delete_visits():
    session.pop('visits')
    return "ok"


# метод, который возвращает список фильмов по относительному адресу /films
@app.route("/films")
def films_list():
    # получаем GET-параметр country (Russia/USA/French
    country = request.args.get("country")
    rating = request.args.get("rating")
    if not rating:
        rating = 0
    films = db.select(rating=rating, country=country)

    # формируем контекст, который мы будем передавать для генерации шаблона
    context = {
        'films': films,
        'title': "FILMS"
    }

    # возвращаем сгенерированный шаблон с нужным нам контекстом
    return render_template("films.html", **context)


# метод, который возвращает конкретный фильмо по id по относительному пути /film/<int:film_id>,
# где film_id - id необходимого фильма
@app.route("/film/<int:film_id>")
def get_film(film_id):
    # используем метод-обертку для выполнения запросов к БД
    film = db.select(film_id)

    if len(film):
        return render_template("film.html", title=film[0]['name'], film=film[0])

    # если нужный фильм не найден, возвращаем шаблон с ошибкой
    return render_template("error.html", error="Такого фильма не существует в системе")


@app.route('/newfilm', methods=['GET'])
def new_film_form():
    context = {
        'title': 'Add film'
    }
    return render_template('newfilm.html', **context)


@app.route('/newfilm', methods=['POST'])
def add_film():
    title = request.form['title']
    rating = float(request.form['rating'])
    country = request.form['country']
    db.insert(title, rating, country)
    return redirect('/films')


@app.route('/change_mode', methods=['GET'])
def get_change_form():
    return render_template('change_mode.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
