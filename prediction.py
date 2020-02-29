"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = "Jinyuan Chen"
__email__ = "jinyuan.chen@uqconnect.edu.au"

from weather_data import WeatherData


class WeatherPrediction(object):
    """Superclass for all of the different weather prediction models."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        raise NotImplementedError

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        raise NotImplementedError

    def high_temperature(self):
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self):
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self):
        """(int) Expected humidity."""
        raise NotImplementedError

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError

    def wind_speed(self):
        """(int) Expected average wind speed."""
        raise NotImplementedError


class YesterdaysWeather(WeatherPrediction):
    """Simple prediction model, based on yesterday's weather."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return 1

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1
        LITTLE_RAIN = 3
        SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0
        MILD = 40
        PROBABLE = 75
        LIKELY = 90

        if self._yesterdays_weather.get_rainfall() < NO_RAIN:
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN:
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN:
            chance_of_rain = PROBABLE
        else:
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self):
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self):
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self):
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()


# Your implementations of the SimplePrediction and SophisticatedPrediction
# classes should go here.
class SimplePrediction(WeatherPrediction):
    """Object predicts the weather based on the average of the past n days' worth of weather data."""

    def __init__(self, weather_data, past_n_days):
        """Retrieves and stores references to the past n days' weather data.

        Parameters:
            weather_data (WeatherData): Collection of weather data.
            past_n_days:  Past number of days' weather data

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        available_day = weather_data.size()
        self._past_n_days = past_n_days

        if self._past_n_days > available_day:
            past_n_days = available_day

        self._simple_prediction_weather = self._weather_data.get_data(past_n_days)

    def get_number_days(self):
        """(int) Returns the number of days of data being used"""
        return self._past_n_days

    def chance_of_rain(self):
        """Calculate the average rainfall for the past n days

        (int) Return the percentage indicating chance of rain occurring."""

        total_rain_amount = 0
        for num_day in self._simple_prediction_weather:
            total_rain_amount += num_day.get_rainfall()
        average_rainfall = total_rain_amount / self._past_n_days
        result = average_rainfall * 9
        if result > 100:
            result = 100

        return round(result)

    def high_temperature(self):
        """(float) Return the highest temperature recorded in the past n days."""

        highest_temperature = self._simple_prediction_weather[0].get_high_temperature()
        for num_day in self._simple_prediction_weather:
            if highest_temperature <= num_day.get_high_temperature():
                highest_temperature = num_day.get_high_temperature()
        return float(highest_temperature)

    def low_temperature(self):
        """(float) Return the lowest temperature recorded in the past n days."""

        lowest_temperature = self._simple_prediction_weather[0].get_low_temperature()
        for num_day in self._simple_prediction_weather:
            if lowest_temperature >= num_day.get_low_temperature():
                lowest_temperature = num_day.get_low_temperature()
        return float(lowest_temperature)

    def humidity(self):
        """(int) Return the average of humidity data from the past n days."""

        total_humidity_amount = 0
        for num_day in self._simple_prediction_weather:
            total_humidity_amount += num_day.get_humidity()
        average_humidity = total_humidity_amount / self._past_n_days
        return round(average_humidity)

    def cloud_cover(self):
        """(int) Return the average of cloud_cover data from the past n days."""

        total_cloud_amount = 0
        for num_day in self._simple_prediction_weather:
            total_cloud_amount += num_day.get_cloud_cover()
        average_cloud_cover = total_cloud_amount / self._past_n_days
        return round(average_cloud_cover)

    def wind_speed(self):
        """(int) Return the average of wind_speed data from the past n days"""

        total_wind_amount = 0
        for num_day in self._simple_prediction_weather:
            total_wind_amount += num_day.get_average_wind_speed()
        average_wind_speed = total_wind_amount / self._past_n_days
        return round(average_wind_speed)


class SophisticatedPrediction(WeatherPrediction):
    """Object predicts the weather based on the average of the past n days' worth of weather data."""

    def __init__(self, weather_data, past_n_days):
        """Retrieves and stores references to the past n days' weather data.

                Parameters:
                    weather_data (WeatherData): Collection of weather data.
                    past_n_days:  Past number of days' weather data

                Pre-condition:
                    weather_data.size() > 0
                """
        super().__init__(weather_data)
        available_day = weather_data.size()
        self._past_n_days = past_n_days

        if self._past_n_days > available_day:
            past_n_days = available_day

        self._sophisticated_prediction_weather = self._weather_data.get_data(past_n_days)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Returns the number of days of data being used"""
        return self._past_n_days

    def chance_of_rain(self):
        """Calculate the average rainfall for the past n days

        (int) Return the percentage indicating chance of rain occurring."""

        yesterday_air_pressure = self._yesterdays_weather.get_air_pressure()
        yesterday_wind_direction = self._yesterdays_weather.get_wind_direction()

        total_rainfall_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_rainfall_amount += num_day.get_rainfall()
        average_rainfall = total_rainfall_amount / self._past_n_days

        total_pressure_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_pressure_amount += num_day.get_air_pressure()
        average_air_pressure = total_pressure_amount / self._past_n_days

        if yesterday_air_pressure < average_air_pressure:
            average_rainfall = average_rainfall * 10
        elif yesterday_air_pressure >= average_air_pressure:
            average_rainfall = average_rainfall * 7

        rainfall_result = average_rainfall
        if yesterday_wind_direction in ("NNE", "NE", "ENE", "E", "ESE", "SE", "SSE"):
            rainfall_result = average_rainfall * 1.2
        if rainfall_result > 100:
            rainfall_result = 100

        return round(rainfall_result)

    def high_temperature(self):
        """(float) Return the average high temperature recorded in the past n days."""

        yesterday_air_pressure = self._yesterdays_weather.get_air_pressure()

        total_high_temperature_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_high_temperature_amount += num_day.get_high_temperature()
        average_high_temperature = total_high_temperature_amount / self._past_n_days

        total_pressure_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_pressure_amount += num_day.get_air_pressure()
        average_air_pressure = total_pressure_amount / self._past_n_days

        high_temperature_result = average_high_temperature
        if yesterday_air_pressure > average_air_pressure:
            high_temperature_result = average_high_temperature + 2

        return float(high_temperature_result)

    def low_temperature(self):
        """(float) Return the average low temperature recorded in the past n days."""
        yesterday_air_pressure = self._yesterdays_weather.get_air_pressure()

        total_low_temperature_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_low_temperature_amount += num_day.get_low_temperature()
        average_low_temperature = total_low_temperature_amount / self._past_n_days

        total_pressure_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_pressure_amount += num_day.get_air_pressure()
        average_air_pressure = total_pressure_amount / self._past_n_days

        low_temperature_result = average_low_temperature
        if yesterday_air_pressure < average_air_pressure:
            low_temperature_result = average_low_temperature - 2

        return float(low_temperature_result)

    def humidity(self):
        """(int) Return the average of humidity data from the past n days."""

        yesterday_air_pressure = self._yesterdays_weather.get_air_pressure()
        total_humidity_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_humidity_amount += num_day.get_humidity()
        average_humidity = total_humidity_amount / self._past_n_days

        total_pressure_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_pressure_amount += num_day.get_air_pressure()
        average_air_pressure = total_pressure_amount / self._past_n_days

        humidity_result = average_humidity
        if yesterday_air_pressure < average_air_pressure:
            humidity_result = average_humidity + 15
        elif yesterday_air_pressure > average_air_pressure:
            humidity_result = average_humidity - 15
        if humidity_result < 0:
            humidity_result = 0
        if humidity_result > 100:
            humidity_result = 100

        return round(humidity_result)

    def cloud_cover(self):
        """(int) Return the average of cloud_cover from the past n days."""

        yesterday_air_pressure = self._yesterdays_weather.get_air_pressure()

        total_cloud_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_cloud_amount += num_day.get_cloud_cover()
        average_cloud_cover = total_cloud_amount / self._past_n_days

        total_pressure_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_pressure_amount += num_day.get_air_pressure()
        average_air_pressure = total_pressure_amount / self._past_n_days

        cloud_cover_result = average_cloud_cover
        if yesterday_air_pressure < average_air_pressure:
            cloud_cover_result = average_cloud_cover + 2
        if cloud_cover_result > 9:
            cloud_cover_result = 9

        return round(cloud_cover_result)

    def wind_speed(self):
        """(int) Return the average of wind_speed from the past n days"""

        yesterday_maximum_wind_speed = self._yesterdays_weather.get_maximum_wind_speed()
        total_wind_amount = 0
        for num_day in self._sophisticated_prediction_weather:
            total_wind_amount += num_day.get_average_wind_speed()
        average_wind_speed = total_wind_amount / self._past_n_days

        wind_speed_result = average_wind_speed
        if yesterday_maximum_wind_speed > 4 * average_wind_speed:
            wind_speed_result = average_wind_speed * 1.2

        return round(wind_speed_result)


if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
