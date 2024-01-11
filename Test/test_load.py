import json
from datetime import datetime

from DB_conect import get_db_connection

# Connect to database
conn = get_db_connection()
cursor = conn.cursor()

# Function to fetch data from a local JSON file
def fetch_data_from_file():
    try:
        with open('/Users/tatanabobyleva/Downloads/red_alerts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '/Users/tatanabobyleva/Downloads/red_alerts.json' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


# Function to format time
def format_time(entry):
    for alert in entry['alerts']:
        # Format time as real date-time
        dt_object = datetime.fromtimestamp(alert['time'])
        alert['time'] = dt_object.strftime("%Y-%m-%d %H:%M:00")

    return entry

# Specify the path to your local JSON file
json_file_path = '/Users/tatanabobyleva/Downloads/red_alerts.json'
formatted_data = [format_time(entry) for entry in fetch_data_from_file()]

# Class to represent an alert item
class AlertItem:
    def __init__(self, ID, City, Time):
        self.ID = ID
        self.City = City
        self.Time = Time

    def save(self):
        try:
            # Use a context manager for handling the database connection
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO alerts (id, city, time) VALUES (%s, %s, %s)",
                    (self.ID, self.City, self.Time),
                )
            conn.commit()
        except Exception as e:
            print(f"Error saving data: {e}")
            conn.rollback()

    def update(self):
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'UPDATE alerts SET city_id = city.city_id FROM city WHERE alerts.city = city.hb_name AND alerts.city_id IS NULL;'
                )
            conn.commit()
        except Exception as e:
            print(f"Error updating data: {e}")
            conn.rollback()

# Output the formatted data with each city separately
for entry in formatted_data:
    for alert in entry['alerts']:
        for city in alert['cities']:
            # Filter data only for the current date
    
                ID = entry['id']
                City = city.split(' -')[0]
                Time = alert['time']
                item = AlertItem(ID, City, Time)
                #item.save()
                #print('Data saved')
                print(f'({ID}, "{City}", "{Time}"),')
                #item.update()

# Close the database connection
cursor.close()
conn.close()
