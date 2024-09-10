from abc import ABC, abstractmethod
import logging


PATH = 'templates/mission.html'


class DroneController:
    """
    Класс для управления дроном
    """
    def takeoff(self):
        """
        Метод для взлета дрона
        """
        logging.info('Запуск метода takeoff для DroneController')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Дрон взлетает...</p>')

    def move_forward(self, distance: float):
        """
        Метод для движения вперед на заданное расстояние.
        :param distance: Расстояние, на которое дрон должен пролететь вперед
        """
        logging.info('Запуск метода move_forward для DroneController')
        # logging.info(f'Летим вперед на {distance} метров')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Летим вперед на {{ distance }} метров</p>')

    def turn(self, degree: float):
        """
        Команда для поворота дрона на заданное количество градусов
        :param degree: Угол поворота в градусах
        """
        logging.info('Запуск метода turn для DroneController')
        # logging.info(f'Поворачиваем на {degree} градусов')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Поворачиваем на {{ degree }} градусов</p>')


class ICommand(ABC):
    """
    Интерфейс комманды
    """
    @abstractmethod
    def execute(self):
        """
        Метод для выполнения команды
        """
        pass

    def undo(self):
        """
        Метод для отмены команды
        """
        pass


class Takeoff(ICommand):
    """
    Класс команды для взлета дрона
    """
    def __init__(self, drone: DroneController):
        """
        Конструктор класса Takeoff
        :param drone: Объект, реализующий класс DroneController
        """
        self.__drone = drone

    def execute(self):
        """
        Метод выполнения команды взлета
        """
        logging.info('Запуск метода execute для команды Takeoff')
        self.__drone.takeoff()


class MoveForward(ICommand):
    """
    Класс команды движения дрона вперед
    """
    def __init__(self, drone: DroneController, distance: float) -> None:
        """
        Конструктор класса MoveForward
        :param drone: Объект, реализующий класс DroneController
        :param distance: Расстояние для движения вперед
        """
        self.__drone = drone
        self.__distance = distance

    def execute(self):
        """
        Метод выполнения движения дрона вперёд на заданное направление
        """
        logging.info('Запуск метода execute для команды MoveForward')
        self.__drone.move_forward(self.__distance)


class Turn(ICommand):
    """
    Класс команды поворота дрона
    """
    def __init__(self, drone: DroneController, degree: float):
        """
        Конструкор класса Turn
        :param drone: Объект, реализующий класс DroneController
        :param degree: Угол поворота дрона
        """
        self.__drone = drone
        self.__degree = degree

    def execute(self):
        """
        Метод выполнения команды поворота дрона на заданный угол
        """
        logging.info('Запуск метода execute для команды Turn')
        self.__drone.turn(self.__degree)


class IFlightStrategy(ABC):
    """
    Интерфейс стратегии полёта
    """
    @abstractmethod
    def execute(self, commands: list):
        """
        Метод для выполнения списка команд в рамках стратегии.
        :param commands: Список команд для выполнения.
        """
        pass


class ReconMissionStrategy(IFlightStrategy):
    """
    Класс стратегии разведовательной миссии
    """
    def execute(self, commands: list):
        """
        Метод выполнения разведывательной миссии
        :param commands: Список команд
        :return: Симуляции выполнения миссии
        """
        logging.info('Запуск метода execute для миссии ReconMissionStrategy')
        logging.info('Начало выполнения разведовательной миссии')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Начало выполнения разведовательной миссии</p>')
        for command in commands:
            command.execute()
        logging.info('Окончание выполнения разведовательной миссии')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Окончание выполнения разведовательной миссии</p>')


class PatrolMissionStrategy(IFlightStrategy):
    """
    Класс стратегии миссии патрулирования
    """
    def __init__(self, n_patrols: int) -> None:
        """
        Конструктор класса PatrolMissionStrategy
        :param n_patrols: Количество патрулирований
        """
        self.__n_patrols = n_patrols

    def execute(self, commands: list):
        """
        Метод выполнения миссии патрулироваиния
        :param commands: Список команд
        :return: Симуляции выполнения миссии
        """
        logging.info('Запуск метода execute для миссии PatrolMissionStrategy')
        logging.info('Начало выполнения миссии патрулирования')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Начало выполнения миссии патрулирования</p>')
        for _ in range(self.__n_patrols):
            for command in commands:
                command.execute()
            # logging.info('Патрулирование выполнено')
        logging.info('Окончание выполнения разведовательной миссии')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Конец выполнения разведовательной миссии</p>')

    def turn(self, degree: float):
        logging.info('Запуск метода turn для миссии PatrolMissionStrategy')
        # logging.info(f'Поворачиваем на {degree} градусов')
        with open(PATH, 'a', encoding='utf-8') as func:
            func.write('\n<p>Поворачиваем на {{ degree }} градусов</p>')


class DroneContext:
    """
    Класс контекста для управления стратегиями полета дрона
    """
    def __init__(self, strategy: IFlightStrategy = None):
        """
        Контруктор класса DroneContext
        :param strategy: Объект, реализующий интерфейс IFlightStrategy
        """
        self.__strategy = strategy
        self.__commands = []

    def set_strategy(self, stratagy: IFlightStrategy):
        """
        Метод установливает стратегии полета для дрона
        :param strategy: Объект, реализующий интерфейс IFlightStrategy.
        """
        logging.info('Запуск метода set_strategy для DroneContext')
        self.__strategy = stratagy

    def add_command(self, command: ICommand):
        """
        Метод добавляет команду в список для выполнения.
        :param command: Объект, реализующий интерфейс ICommand.
        """
        logging.info('Запуск метода add_command для DroneContext')
        self.__commands.append(command)

    def execute(self):
        """
        Выполняет все команды, используя текущую стратегию полета.
        После выполнения команды очищает список.
        """
        logging.info('Запуск метода execute для DroneContext')
        self.__strategy.execute(self.__commands)
        self.__commands.clear()
