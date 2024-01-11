import requests
import json
import schedule
import time
from datetime import datetime

from DB_conect import get_db_connection




def main():

    # 1 conect to database
    conn = get_db_connection()
    cursor = conn.cursor()


    #2 get dataset from website:
    def fetch_data():
        url = "https://api.tzevaadom.co.il/alerts-history/"
        
        # Set start_date and end_date to the current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        params = {
            'start_date': current_date,
            'end_date': current_date,
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            # Return the fetched data
            return json.loads(response.text)
        else:
            # Log details about the error
            print(f"Error {response.status_code}: Unable to fetch data.")
            print(response.text)  # Print the response content for debugging




    #ADD DATA  SET  TO DB
    class AlertItem:
        def __init__(self, ID, City, Time):
            global cursor
            self.ID = ID
            self.City = City
            self.Time = Time

        def save(self):
            # Use a context manager for handling the database connection
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO alerts (id, city, time) VALUES (%s, %s, %s)",
                    (self.ID, self.City, self.Time),
                )
                conn.commit()


        def update():
            with conn.cursor as cursor:
                cursor.execute('UPDATE alerts SET city_id = city.city_id FROM city WHERE alerts.city = city.hb_name AND alerts.city_id IS NULL;'
                )
                conn.commit()




    # Function to format time
    def format_time(entry):
        for alert in entry['alerts']:
            # Format time as real date-time
            dt_object = datetime.fromtimestamp(alert['time'])
            alert['time'] = dt_object.strftime("%Y-%m-%d %H:%M:00")

        return entry

    # Apply formatting to each entry
    formatted_data = [format_time(entry) for entry in fetch_data()]




    # Output the formatted data with each city separately
    for entry in formatted_data:
        for alert in entry['alerts']:
            for city in alert['cities']:
                # filter to data only for current_date:
                if alert['time'][:10] == datetime.now().strftime("%Y-%m-%d"):
                    ID = entry['id']
                    City = city.split(' -')[0]
                    Time = alert['time']
                    item = AlertItem(ID, City, Time)
                    item.save() 
                    print('data saved')
                    item.update()
    cursor.close()
    conn.close()

    
main()


# Schedule to run functions at 23:59 every day:
schedule.every().day.at("23:59").do(main)


# Unending cycle
while True:
    schedule.run_pending()
    time.sleep(1)