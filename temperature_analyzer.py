class TemperatureAnalyzer:
    """
    Manages the temperature analuzis for patients.
     The temperature_analyzer script implements the following requirements:
     1/ The system should accept temperature readings in Celsius or Fahrenheit.
     2/ The system should convert the temperature to Celsius for analysis (if provided in Fahrenheit).
     3/ The system should classify the patient's status based on body temperature and age-dependent thresholds.
     4/ The system should support displaying the status (if enabled) and logging it to a file (if enabled).

    Attributes:
        LOW_FEVER_THRESHOLD (float): Threshold for low fever (38.0).
        HIGH_FEVER_THRESHOLD (float): Threshold for high fever (39.4).
        BABY_FEVER_THRESHOLD (float): Lower threshold for babies < 3 years (37.4).
        MIN_CELSIUS (int): Minimum valid Celsius reading (-50).
        MAX_CELSIUS (int): Maximum valid Celsius reading (150).
        MIN_FAHRENHEIT (int): Minimum valid Fahrenheit reading (-58).
        MAX_FAHRENHEIT (int): Maximum valid Fahrenheit reading (302).
    """

    LOW_FEVER_THRESHOLD = 38
    HIGH_FEVER_THRESHOLD = 39.4
    BABY_FEVER_THRESHOLD = 37.4

    MIN_CELSIUS = -50
    MAX_CELSIUS = 150

    MIN_FAHRENHEIT = -58
    MAX_FAHRENHEIT = 302


    def __init__(self, debug=False, default_unit="C"):
        """
        Initializes the temperature analyzer.

        :param debug: (bool) Enable debug mode to print.
        :param default_unit: (str) Default temperature unit to use.
        """

        self.last_status = None
        self.tmp_cache = None
        self.debug_mode = debug
        self.default_unit = default_unit


    def convert_to_celsius(self, temp, unit=None):
        """
        Validates the temperature range and converts it to Celsius.

        :param temp : (float) Temperature value.
        :param unit: (str) C or F to indicate unit.
        :return: (float) Temperature in Celsius.
        """

        if unit == "None":
            unit = self.default_unit

        if unit == "C":
            if temp < self.MIN_CELSIUS or temp > self.MAX_CELSIUS:
                print("Warning: Unrealistic temperature detected.")
                raise ValueError("Unrealistic temperature detected.")
            self.tmp_cache = temp
            return temp
        elif unit == "F":
            if temp < self.MIN_FAHRENHEIT or temp > self.MAX_FAHRENHEIT:
                print("Warning: Unrealistic temperature detected.")
                raise ValueError("Unrealistic temperature detected.")

            c = (temp - 32) * 5/9
            self.tmp_cache = c
            return c


    def has_fever(self, temp, scale="C"):
        """
        Checks if the temperature is a fever.

        :param temp: (float) Temperature value.
        :param scale: (str) Unit of the temperature
        :return: (bool) Whether the fever exists. True if detected, False if not.
        """

        try:
            if scale == "C":
                fever = temp > self.LOW_FEVER_THRESHOLD
            else:
                c = self.convert_to_celsius(temp, scale)
                fever = c > self.LOW_FEVER_THRESHOLD

            return fever
        except (ValueError, TypeError) as e:
            print("Error calculating fecer status:", e)
            raise e


    def analyze_patient(self, temp, age, verbose=0, emergency_mode=False, log=False, log_file="temp_log.txt", unit=None):
        """
        Analyzes a patient temperature based on their temperature and age.

        :param temp: (float) Temperature value.
        :param age: (int) Age value of patient.
        :param verbose: (int) Level of the detail of the output. 0 is None, 1 is Basic and 3 is High level of detail.
        :param emergency_mode: (bool) Checks for hypothermia if true (<30C).
        :param log: (bool) Writes results to file if it is true.
        :param log_file: (str) Filename for the log file.
        :param unit: (str) Unit of the temperature.
        :return: (str) Diagnosis status like Normal or Fever.
        """

        if age < 0:
            raise ValueError("Age cannot be negative.")

        temp = self.convert_to_celsius(temp, unit)

        if emergency_mode and temp < 30:
            self.last_status = "HYPOTHERMIA?"
            return self.last_status



        if age < 3:
            threshold = self.BABY_FEVER_THRESHOLD
        else:
            threshold = self.HIGH_FEVER_THRESHOLD

        if temp > threshold:
            status = "FEVER"
        elif temp > threshold - 0.2:
            status = "ALMOST FEVER"
        else:
            status = "NORMAL"

        self.last_status = status

        if log:
            try:
                with open(log_file, "a") as f:
                    f.write(f"TEMP={temp}, AGE={age}, STATUS={status}\n")
            except IOError as e:
                print("Error opening and writing to log file:", e)

        if verbose > 0:
            print("Patient status:", status)

        if verbose > 2:
            print(f" Detailed Analysis: Temp={temp:.2f}C (Threshold={threshold})")

        return status


    def get_status_report(self, include_temp=False, format="long"):
        """
        Creates a status report.

        :param include_temp: (bool) If true it adds the cached Celsius value to the result.
        :param format: (str) Format of the result.
        :return: (dict) It contains raw_status, display_text and the format used.
        """

        response = {
            "raw_status": self.last_status,
            "format_used": format
        }

        if include_temp:
            response["temp_celsius"] = self.tmp_cache
        elif format == "code":
            response["display_text"] = self.last_status[:2]
        else:
            response["display_text"] = f"Current status: {self.last_status}"

        return response


if __name__ == "__main__":

    temp = 109.7
    age = 5

    print("Analyzing temperature:", temp)

    # initialize analyzer
    analyzer = TemperatureAnalyzer(debug=False, default_unit="C")

    result = analyzer.analyze_patient(
        temp,
        age,
        verbose=3,
        emergency_mode=False,
        log=True,
        unit="C",
        log_file="temp_log.txt"
    )

    print("Result:", result)
    print("Last status:", analyzer.last_status)
    print("Status report:", analyzer.get_status_report(include_temp=True))
