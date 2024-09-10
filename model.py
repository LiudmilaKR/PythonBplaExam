class Drone:
    """
    Реализация класса Drone
    """
    def __init__(self, max_altitude: int,
                 max_speed: int, max_flight_time: int, serial_number: str,
                 model: str, manufacturer: str, drone_id=''):
        """
        Создание конструктора класса Drone
        :param max_altitude: Максимальная высота взлета дрона
        :param max_speed: Максимальная скорость движения дрона
        :param max_flight_time: Максимальное время полета дрона
        :param serial_number: Серийный номер дрона
        :param model: Модель дрона
        :param manufacturer: Производитель дрона
        :param drone_id: id дрона
        """
        self.__max_altitude = max_altitude
        self.__max_speed = max_speed
        self.__max_flight_time = max_flight_time
        self.__serial_number = serial_number
        self.__model = model
        self.__manufacturer = manufacturer

    """
    Создание геттеров для параметров дрона
    """
    @property
    def max_altitude(self):
        return self.__max_altitude

    @property
    def max_speed(self):
        return self.__max_speed

    @property
    def max_flight_time(self):
        return self.__max_flight_time

    @property
    def serial_number(self):
        return self.__serial_number

    @property
    def model(self):
        return self.__model

    @property
    def manufacturer(self):
        return self.__manufacturer
