import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="films",
            user="postgres",
            password="admin",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()
        self.con.autocommit = True

    def insert(self, name, rating, country):
        self.cur.execute(f"INSERT INTO films(name, rating, country) values ('{name}', {rating}, '{country}');")

    def select(self, id=None, rating=0, country=None):
        if id:
            self.cur.execute(f"SELECT * FROM films WHERE id = {id};")
        elif country:
            self.cur.execute(f"SELECT * FROM films WHERE rating >= {rating} AND country = '{country}';")
        else:
            self.cur.execute(f"SELECT * FROM films WHERE rating >= {rating};")
        data = self.cur.fetchall()
        return self.prepare_data(data)

    def prepare_data(self, data):
        films = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                films += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return films
