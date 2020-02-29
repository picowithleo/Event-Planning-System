"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = "Jinyuan Chen"
__email__ = "jinyuan.chen@uqconnect.edu.au"

from weather_data import WeatherData
from prediction import WeatherPrediction, YesterdaysWeather, SimplePrediction, SophisticatedPrediction
# Import your SimplePrediction and SophisticatedPrediction classes once defined.


# Define your Event Class here
class Event(object):
    """Holds data about a single event and provides access to that data.
    """

    def __init__(self, name, outdoors, cover_available, time):
        """Stores local references to the given parameters.

        Parameters:
            name (str): The name of the event.
            outdoors (bool): Representing whether the event is outdoors.
            cover_available (bool): Representing whether there is cover available.
            time (int): The closest hour to the starting time of the event.
        """
        self._name = name
        self._outdoors = outdoors
        self._cover_available = cover_available
        self._time = time

    def get_name(self):
        """Returns the Event name.

        Return:
             (str) the name of Event.
        """
        return self._name

    def get_time(self):
        """Returns the integer time value.

        Return:
            (int) the value of the time.
        """

        return self._time

    def get_outdoors(self):
        """Returns the Boolean outdoors value.

        Return:
            (bool) the value of outdoors.
        """
        return self._outdoors

    def get_cover_available(self):
        """Returns the Boolean cover_available value.

        Return:
            (bool) the value of cover_available.
        """
        return self._cover_available

    def __str__(self):
        """Returns a string representation of the Event in the format.

        Return:
            (str) the format of the Event.
        """
        return "Event({} @ {}, {}, {})".format(self._name,
                                               self._time,
                                               self._outdoors,
                                               self._cover_available)


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""

    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           An object of a subclass of WeatherPrediction used 
                           to predict the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
        """
        humidity_value = self._prediction_model.humidity()
        high_temperature = self._prediction_model.high_temperature()
        low_temperature = self._prediction_model.low_temperature()
        is_cloud_cover = self._prediction_model.cloud_cover()
        wind_speed = self._prediction_model.wind_speed()
        is_outdoors = self._event.get_outdoors()
        is_cover_available = self._event.get_cover_available()
        time = self._event.get_time()
        HUMIDITY_FACTOR = 70

        if humidity_value > HUMIDITY_FACTOR:
            humidity_factor = humidity_value / 20
            if high_temperature > 0:
                high_temperature = high_temperature + humidity_factor
            elif high_temperature < 0:
                high_temperature = high_temperature - humidity_factor
            if low_temperature > 0:
                low_temperature = low_temperature + humidity_factor
            elif low_temperature < 0:
                low_temperature = low_temperature - humidity_factor

        if 6 <= time <= 19 and is_outdoors and high_temperature >= 30:
            initial_temp_factor = high_temperature / -5 + 6
        elif high_temperature >= 45:
            initial_temp_factor = high_temperature / -5 + 6
        elif (0 <= time <= 5 or 20 <= time <= 23) and low_temperature < 5 and high_temperature < 45:
            initial_temp_factor = low_temperature / 5 - 1.1
        elif low_temperature > 15 and high_temperature < 30:
            initial_temp_factor = (high_temperature - low_temperature) / 5
        else:
            initial_temp_factor = 0

        temperature_factor = initial_temp_factor
        if initial_temp_factor < 0:
            if is_cover_available:
                temperature_factor = initial_temp_factor + 1
            if 3 < wind_speed < 10:
                temperature_factor = initial_temp_factor + 1
            if is_cloud_cover > 4:
                temperature_factor = initial_temp_factor + 1

        return float(temperature_factor)

    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        chance_of_rain = self._prediction_model.chance_of_rain()
        is_outdoors = self._event.get_outdoors()
        is_cover_available = self._event.get_cover_available()
        wind_speed = self._prediction_model.wind_speed()

        if chance_of_rain < 20:
            initial_rain_factor = chance_of_rain / -5 + 4
        elif chance_of_rain > 50:
            initial_rain_factor = chance_of_rain / -20 + 1
        else:
            initial_rain_factor = 0

        rain_factor = initial_rain_factor
        if is_outdoors and is_cover_available and wind_speed < 5:
            rain_factor = initial_rain_factor + 1
        if initial_rain_factor < 2 and wind_speed > 15:
            rain_factor = (initial_rain_factor + (wind_speed / -15))
            if rain_factor < -9:
                rain_factor = -9

        return float(rain_factor)

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        advisability_ranking = self._temperature_factor() + self._rain_factor()
        if advisability_ranking < -5:
            advisability_ranking = -5
        if advisability_ranking > 5:
            advisability_ranking = 5

        return advisability_ranking


class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """ Object that is the program’s user interface
        """
        self._event = None
        self._prediction_model = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        event_name = input("What is the name of the event? ")

        while True:
            outdoors = input("Is the event outdoors? ").lower()
            if outdoors == "y" or outdoors == "yes":
                outdoors = True
                break
            elif outdoors == "n" or outdoors == "no":
                outdoors = False
                break
            else:
                print("Please enter a valid value.")

        while True:
            shelter = input("Is there covered shelter? ").lower()
            if shelter == "y" or shelter == "yes":
                shelter = True
                break
            elif shelter == "n" or shelter == "no":
                shelter = False
                break
            else:
                print("Please enter a valid value.")

        while True:
            time = input("What time is the event? ")
            if time.isdigit():
                if 0 <= int(time) < 24:
                    time = int(time)
                    break
                else:
                    print("Please enter an integer time value from 0 up to, but not including 24.")
            else:
                print("Please enter an integer time value.")
                #  a reference to Event object
                # self._event is an object (Event)
        self._event = Event(event_name, outdoors, shelter, time)

        return self._event

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """

        while True:
            print("Select the weather prediction model you wish to use:")
            print("  1) Yesterday's weather.")
            print("  2) Simple prediction.")
            print("  3) Sophisticated prediction.")
            # Error handling can be added to this method.
            model_choice = input("> ")
            if model_choice == '1':
                self._prediction_model = YesterdaysWeather(weather_data)
                break
            elif model_choice == '2':
                past_n_days = input("Enter how many days of data you wish to use for making the prediction: ")
                self._prediction_model = SimplePrediction(weather_data, int(past_n_days))
                break
            elif model_choice == '3':
                past_n_days = input("Enter how many days of data you wish to use for making the prediction: ")
                self._prediction_model = SophisticatedPrediction(weather_data, int(past_n_days))
                break
            else:
                print("\nPlease enter an existed model!\n")
        # Cater for other prediction models when they are implemented.
        return self._prediction_model

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (float): Impact of the weather on the event.
                            -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        # The following print statement is an example of printing out the
        # class name of an object, which you may use for making the
        # advisability output more meaningful.
        print("Based on the", type(self._prediction_model).__name__,
              "model, the advisability of holding", self._event.get_name(), "is", impact)

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """
        print("\nHi dear, would you like to try using a different weather prediction model?")
        while True:
            user_answer = input().lower()
            if user_answer == "y" or user_answer == "yes":
                return True
            elif user_answer == "n" or user_answer == "no":
                return False
            else:
                print("Please enter 'Y' or 'Yes' or 'N' or 'No'.")


def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()


if __name__ == "__main__":
    main()
