
from alert_each_city import City

# Greeting the user
print("Hello! Welcome to the Alert Predictor!")
print("DISCLAIMER: This program provides the probability of an air raid based on alarm history.")
print("ALL INFORMATION IS ADVISORY.")

# Asking for the city name
city_name = input("Enter the name of your city: ").capitalize()

city = City(city_name, 0, 0)

city_id = city.show_city()
if city_id is not None:
    print(f"Let's see what happens in {city_name}")
    time = input("Enter the hour (0-24) you want to check: ")

    while not time.isdigit() or int(time) not in range(0, 24):
        print("Sorry, wrong input. Please enter a valid hour (0-24).")
        time = input("Enter the hour (0-24) you want to check: ")

    time = int(time)
elif city_id is None:
    print(f"Sorry, {city_name} not found. Maybe you meant:")
    city.show_list_cities()
else:
    print("Sorry, something went wrong. Try again next time.")

city_check = City(city_name, city_id, time)

total_alerts_in_hour = city_check.all_alerts_in_cities()
city_hour_alerts = city_check.hour_alerts_in_city()


if total_alerts_in_hour == 0:
    print("No historical data available for the selected hour.")
else:
    percentage_alerts_outcomes = (city_hour_alerts / total_alerts_in_hour) * 100



if 10 < percentage_alerts_outcomes < 30:
    print("It will be a pretty good hour.")
elif 30 < percentage_alerts_outcomes < 50:
    print("It will be quite a quiet hour.")
elif 50 < percentage_alerts_outcomes < 70:
    print("There is a possibility of an air raid.")
else:
    print("Be careful, maybe you should consider staying home.")

    city_check.conn.close()

 