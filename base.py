import sqlite3

class SQL:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def date_exists(self, date):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users WHERE date = ?', (date,)).fetchall()
            return bool(len(result))

    def add_event(self, date, event, description, year, month):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO tatneft (date, event, description, year, month) VALUES(?,?,?,?,?)",
                (date, event, description, year, month)
            )

    def add_people(self, event, people):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO people (event, people) VALUES(?,?)",
                (event, people)
            )

    def get_people(self):
        with self.connection:
            return self.cursor.execute('SELECT people FROM people').fetchall()

    def get_event(self):
        with self.connection:
            return self.cursor.execute('SELECT event FROM tatneft').fetchall()

    def get_description(self):
        with self.connection:
            return self.cursor.execute('SELECT description FROM tatneft').fetchall()

    def get_dates(self):
        with self.connection:
            return self.cursor.execute('SELECT date FROM tatneft').fetchall()

    def get_years(self):
        with self.connection:
            return self.cursor.execute('SELECT year FROM tatneft').fetchall()

    def get_months(self):
        with self.connection:
            return self.cursor.execute('SELECT month FROM tatneft').fetchall()

    def count_events_by_year(self):
        query = "SELECT year, COUNT(*) AS count FROM tatneft GROUP BY year ORDER BY year"
        with self.connection:
            return self.cursor.execute(query).fetchall()

    def top_5_people(self):
        query = """
            SELECT people, COUNT(*) AS count 
            FROM people 
            GROUP BY people 
            ORDER BY count DESC 
            LIMIT 5
        """
        with self.connection:
            return self.cursor.execute(query).fetchall()

    def close(self):
        self.connection.close()