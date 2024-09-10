from abc import ABC, abstractmethod
from database import *
from model import *


# Паттерн Абстрактная фабрика для создания подключений к базе данных
class IDroneRepository(ABC):
    """
    Абстрактный интерфейс хранилища
    """
    @abstractmethod
    def get_all_drones(self):
        """
        Абстрактый метод получения из репозитория списка всех дронов
        :return: Список всех дронов в репозитории
        """
        pass

    @abstractmethod
    def get_drone_by_id(self, drone_id: int):
        """
        Абстрактый метод получения конкретного дрона из репозитория
        :param drone_id: Id дрона для получения
        :return: Полученный дрон
        """
        pass

    # @abstractmethod
    # def update_drone_status(self, id: int, status: str):
    #     """Обновляем статус дрона по id (ожидание, в полете, зарядка)"""
    #     pass

    @abstractmethod
    def add_drone(self, drone: Drone):
        """
        Абстрактый метод добавления дрона в репозиторий
        :param drone: Экземпляр класса Drone
        """
        pass

    # @abstractmethod
    # def remove_drone(self, id: int):
    #     pass


class MySqlDroneRepository(IDroneRepository):
    """
    Реализация репозитория через базу данных MySql
    """
    def __init__(self):
        """
        Объект, реализующий класс MySqlDroneRepository
        """
        self._drones = {}
        self.mysql_bd = MySQLFactory()

    def get_all_drones(self):
        """
        Метод получения списока всех дронов из базы данных
        :return: Список всех дронов
        """
        connect_manager = DBConnectionManager(self.mysql_bd)
        connect = connect_manager.get_connection()
        cur_cursor = connect.cursor()
        query_builder = QueryBuilder()
        query = query_builder.select('tbl_drones').get_query()
        cur_cursor.execute(query)
        result = cur_cursor.fetchall()
        connect_manager.close_connection()
        return result

    def get_drone_by_id(self, drone_id: str):
        pass

    def add_drone(self, drone: Drone):
        pass


class SqliteDroneRepository(IDroneRepository):
    """
    Реализация репозитория через базу данных SQLite
    """
    def __init__(self):
        """
        Объект, реализующий класс SqliteDroneRepository
        """
        self._drones = {}
        self.sqlite_bd = SQLiteFactory()

    def get_all_drones(self):
        """
        Метод получения списока всех дронов из базы данных
        :return: Список всех дронов
        """
        connect_manager = DBConnectionManager(self.sqlite_bd)
        connect = connect_manager.get_connection()
        cur_cursor = connect.cursor()
        query_builder = QueryBuilder()
        query = query_builder.select('tbl_drones').get_query()
        cur_cursor.execute(query)
        result = cur_cursor.fetchall()
        connect_manager.close_connection()
        return result

    def add_drone(self, drone: Drone):
        """
        Метод добавления конкретного дрона в базу данных
        :param drone: Экземляр класса Drone
        """
        connect_manager = DBConnectionManager(self.sqlite_bd)
        connect = connect_manager.get_connection()
        cur_cursor = connect.cursor()
        try:
            query_builder = QueryBuilder()
            insert_query = query_builder.insert_into('tbl_drones',
                                                     ['max_altitude', 'max_speed', 'max_flight_time',
                                                      'serial_number', 'model', 'manufacturer']).values(
                drone.max_altitude, drone.max_speed, drone.max_flight_time, drone.serial_number, drone.model,
                drone.manufacturer).get_query()
            print(f'insert_query={insert_query}')
            params = query_builder.get_params()
            print(f'params={params}')
            cur_cursor.execute(insert_query, params)
            connect.commit()
            connect_manager.close_connection()
        except Exception as e:
            print(f'Ошибка! Незвозможно добавить запись: {e}')

    def get_drone_by_id(self, drone_id: str):
        connect_management = DBConnectionManager(self.sqlite_bd)
        connect = connect_management.get_connection()
        cur_cursor = connect.cursor()
        query_builder = QueryBuilder()
        query = query_builder.select('tbl_drones').where('id = ' + drone_id).get_query()
        cur_cursor.execute(query)
        result = cur_cursor.fetchall()
        connect_management.close_connection()
        return result
