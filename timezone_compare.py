import requests
import datetime
import sys
import json

class date_time_compare():

    def __init__(self):
        self.DATE_TIME = "datetime"
        self.DAY_OF_WEEK = "day_of_week"
        self.DAY_OF_YEAR = "day_of_year"
        self.DATE_LABEL = "date"
        self.TIME_LABEL = "time"
        self.WEEKDAYS_LIST = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
        ]
        self.MONTHS_LIST = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
        self.CITY_LABEL = "city"

    def fill_data(self, date_time, day_of_week, day_of_year, city):
        data = {}
        data[self.DATE_LABEL] = date_time[0]
        data[self.TIME_LABEL] = date_time[1][:5]
        data[self.DAY_OF_WEEK] = day_of_week
        data[self.DAY_OF_YEAR] = day_of_year
        data[self.CITY_LABEL] = city
        return data

    def get_requested_locale_info(self, continent, city):
        r = requests.get("http://worldtimeapi.org/api/timezone/%s/%s" % (continent, city))
        data = r.json()
        date_time = data[self.DATE_TIME].split("T")
        day_of_week = self.WEEKDAYS_LIST[data[self.DAY_OF_WEEK]]
        day_of_year = data[self.DAY_OF_YEAR]
        return self.fill_data(date_time, day_of_week, day_of_year, city)

    def get_local_time(self):
        time = datetime.datetime.now()
        str_time = str(time)
        str_time = str_time.split(' ')
        day_of_week = time.strftime("%A")
        day_of_year = time.strftime("%j")
        return self.fill_data(str_time, day_of_week, day_of_year, "your city")

    def print_time_date(self, data):
        print("It is currently %s in %s." %(data[self.TIME_LABEL], data[self.CITY_LABEL]))
        split_date = data[self.DATE_LABEL].split('-')
        month = self.MONTHS_LIST[int(split_date[1])-1]
        print("The date in %s is %s %s, %s." % (data[self.CITY_LABEL], month, split_date[2], split_date[0]))
        return

    def time_diff_calc(self, local_data, requested_data):
        local_hour = int(local_data[self.TIME_LABEL][:2])
        req_hour = int(requested_data[self.TIME_LABEL][:2])
        local_day = int(local_data[self.DAY_OF_YEAR])
        req_day = int(requested_data[self.DAY_OF_YEAR])
        str_place = ""
        res = 0
        if(local_day < req_day):
            res = ((24 - local_hour) + req_hour) * -1
        elif(local_day == req_day):
            res = local_hour - req_hour
        elif(local_day > req_day):
            res = (24 - req_hour) + local_hour
        if(res < 0):
            str_place = "behind"
            res *= -1
        elif(res == 0):
            print("This city is in the same time zone as your city.")
            return
        elif(res > 0):
            str_place = "ahead of"  
        print("Your city is %s %s by %s hours." % (str_place, requested_data[self.CITY_LABEL], str(res)))

if __name__ == "__main__":
    try:
        sys.argv[2]
    except:
        print("ERROR: please enter a continent and city at the command line. \n Example: timezone-compare.py Asia Tokyo")
        exit(1)
    comp = date_time_compare()
    requested_data = comp.get_requested_locale_info(sys.argv[1], sys.argv[2])
    local_data = comp.get_local_time()
    print(requested_data)
    print(local_data)
    comp.print_time_date(requested_data)
    comp.print_time_date(local_data)
    comp.time_diff_calc(local_data, requested_data)


