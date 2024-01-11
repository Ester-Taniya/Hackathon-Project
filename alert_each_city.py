from DB_conect import get_db_connection


class City:
    def __init__(self, en_name, city_id, time):
        self.en_name = en_name
        self.city_id = city_id
        self.time = time
        self.conn = get_db_connection()

    def show_city(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT city_id FROM city WHERE en_name = %s", (self.en_name,))
            row = cursor.fetchall()
            if row:
                self.city_id = row[0][0]
                return self.city_id
            else:
                return None

    def show_list_cities(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT en_name FROM city WHERE en_name LIKE %s", (f"%{self.en_name[0]}",))
            row = cursor.fetchall()
            if row:
                list_cities = row
                return list_cities
            else:
                return None

    def all_alerts_in_cities(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM alerts WHERE EXTRACT(HOUR FROM time) = %s;", (self.time,))
            row = cursor.fetchall()
            if row:
                all_alerts_in_hour = row
                return all_alerts_in_hour
            else:
                return None

    def hour_alerts_in_city(self):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM alerts WHERE city_id = %s AND EXTRACT(HOUR FROM time) = %s;", (self.city_id, self.time,))
            row = cursor.fetchall()
            if row:
                hour_alerts_in_city = row
                return hour_alerts_in_city
            else:
                return None

if __name__ == "__main__":
    citi1=City('Haifa',0,0)