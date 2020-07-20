import requests
import datetime
import sys
import json

def get_day_of_week(num):
    days_of_week = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]
    return days_of_week[num]

def fill_data(date_time, day_of_week, DATE_LABEL, TIME_LABEL, WEEKDAY_LABEL):
    data = {}
    data[DATE_LABEL] = date_time[0]
    data[TIME_LABEL] = date_time[1][:5]
    data[WEEKDAY_LABEL] = day_of_week
    return data

def get_requested_locale_info(continent, city, DATE_LABEL, TIME_LABEL, WEEKDAY_LABEL):
    r = requests.get("http://worldtimeapi.org/api/timezone/%s/%s" % (continent, city))
    data = r.json()
    DATE_TIME = "datetime"
    WEEKDAY = "day_of_week"
    date_time = data[DATE_TIME].split("T")
    day_of_week = get_day_of_week(data[WEEKDAY])
    return fill_data(date_time, day_of_week, DATE_LABEL, TIME_LABEL, WEEKDAY_LABEL)

def get_local_time(DATE_LABEL, TIME_LABEL, WEEKDAY_LABEL):
    time = datetime.datetime.now()
    str_time = str(time)
    str_time = str_time.split(' ')
    day_of_week = time.strftime("%A")
    return fill_data(str_time, day_of_week, DATE_LABEL, TIME_LABEL, WEEKDAY_LABEL)

if __name__ == "__main__":
    try:
        sys.argv[2]
    except:
        print("ERROR: please enter a continent and city at the command line. \n Example: timezone-compare.py Asia Tokyo")
        exit(1)
    DATE_LABEL = "date"
    TIME_LABEL = "time"
    WEEKDAY_LABEL = "weekday"
    requested_data = get_requested_locale_info(sys.argv[1], sys.argv[2], DATE_LABEL, TIME_LABEL, WEEKDAY_LABEL)
    local_data = get_local_time(DATE_LABEL, TIME_LABEL, WEEKDAY_LABEL)
    print(requested_data)
    print(local_data)


