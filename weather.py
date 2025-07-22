import csv
from datetime import datetime

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and Celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees Celcius."
    """
    return f"{temp}{DEGREE_SYMBOL}"

def convert_date(iso_string):
    """Converts and ISO formatted date into a human-readable format.

    Args:
        iso_string: An ISO date string.
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    dt = datetime.fromisoformat (iso_string)
    return dt.strftime("%A %d %B %Y");          
  
def convert_f_to_c(temp_in_fahrenheit):
    """Converts a temperature from Fahrenheit to Celcius.

    Args:
        temp_in_fahrenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees Celcius, rounded to 1 decimal place.
    """
    temp_in_celsius = (float(temp_in_fahrenheit) -32) * 5/9
    return round(temp_in_celsius,1)

def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """

    if not weather_data:
        return "No daily weather data available."

    numeric_data = [float(x) for x in weather_data]
    return sum(numeric_data) / len(numeric_data)


def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    data = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if row:
                date = row[0]
                min_temp = int(row[1])
                max_temp = int(row[2])
                data.append([date, min_temp, max_temp])
    return data

def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minimum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """

    numeric_data = [float(x) for x in weather_data]

    if not numeric_data:
        return ()

    min_value = min(numeric_data)
    last_index = len(numeric_data) - 1 - numeric_data[::-1].index(min_value)
    return min_value, last_index


def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    numeric_data = [float(x) for x in weather_data]

    if not numeric_data:
        return ()

    max_value = max(numeric_data)
    last_index = len(numeric_data) - 1 - numeric_data[::-1].index(max_value)
    return max_value, last_index

def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information."""
    

    if not weather_data:
        return "No daily weather data available."

    min_temp = float('inf')
    max_temp = float('-inf')
    min_day = ""
    max_day = ""
    total_min = 0
    total_max = 0

    for day in weather_data:
        date_str, min_f, max_f = day
        min_c = convert_f_to_c(min_f)
        max_c = convert_f_to_c(max_f)

        total_min += min_c
        total_max += max_c

        if min_c < min_temp:
            min_temp = min_c
            min_day = date_str
        if max_c > max_temp:
            max_temp = max_c
            max_day = date_str

    avg_min = round(total_min / len(weather_data), 1)
    avg_max = round(total_max / len(weather_data), 1)

    min_day_formatted = datetime.fromisoformat(min_day).strftime("%A %d %B %Y")
    max_day_formatted = datetime.fromisoformat(max_day).strftime("%A %d %B %Y")

    summary = (
        f"{len(weather_data)} Day Overview\n"
        f"  The lowest temperature will be {format_temperature(min_temp)}, and will occur on {min_day_formatted}.\n"
        f"  The highest temperature will be {format_temperature(max_temp)}, and will occur on {max_day_formatted}.\n"
        f"  The average low this week is {format_temperature(avg_min)}.\n"
        f"  The average high this week is {format_temperature(avg_max)}.\n"
    )

    return summary


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    if not weather_data:
        return "No daily weather data available."

    daily_summaries = []
    for i, day in enumerate(weather_data):
        date_str, min_f, max_f = day
        date = datetime.fromisoformat(date_str).strftime("%A %d %B %Y")
        min_c = round(convert_f_to_c(min_f), 1)
        max_c = round(convert_f_to_c(max_f), 1)

        summary_lines = [
            f"---- {date} ----",
            f"  Minimum Temperature: {format_temperature(min_c)}",
            f"  Maximum Temperature: {format_temperature(max_c)}"
        ]

        # ✅ Add hyphen to the end of the last line of the last summary
        if i == len(weather_data) - 1:
            summary_lines[-1] += "-"

        daily_summaries.append("\n".join(summary_lines))

    # ✅ Include the header and join all summaries
    return f"{len(weather_data)} Day Overview\n\n" + "\n\n".join(daily_summaries)





