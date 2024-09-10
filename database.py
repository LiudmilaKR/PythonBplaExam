from abc import ABC, abstractmethod
import sqlite3
import mysql.connector
import logging


class BDFactory(ABC):
    """
    Создание подключения к различным базам данных (интерфейс фабрики)
    """
    @abstractmethod
    def connect(self):
        """
        Абстрактный метод подключения к различным базам данных
        """
        pass


class SQLiteFactory(BDFactory):
    """
    Реализация конкретной фабрики для SQLite
    """
    def connect(self):
        """
        Метод подключения к SQLite
        """
        logging.info('Запуск метода connect для SQLiteFactory')
        return sqlite3.connect('bpla.db')


class MySQLFactory(BDFactory):
    """
    Реализация конкретной фабрики для MySql
    """
    def connect(self):
        """
        Метод подключения к MySql
        """
        logging.info('Запуск метода connect для MySQLFactory')
        return mysql.connector.connect(host='127.0.0.1', user='newuser', passwd='12357***', database='bpla')


class PostgresSQLFactory(BDFactory):
    """
    Реализация конкретной фабрики для PostgresSql
    """
    def connect(self):
        """
        Метод подключения к PostgresSql
        """
        pass


class QueryBuilder:
    """
    Класс для создания SQL-запросов
    """
    def __init__(self):
        """
        Конструктор класса QueryBuilder
        """
        self._query = {
            'select': '',
            'where': '',
            'order_by': '',
            'insert_into': None,
            'values': None
        }
        self._params = []

    def select(self, table, columns='*'):
        """
        Метод создания части запроса выбора данных из базы данных
        :param table: Наименование таблицы, из которой производится запрос
        :param columns: Столбцы для запроса
        :return: Экземляр класса QueryBuilder
        """
        logging.info('Запуск метода select для QueryBuilder')
        self._query['select'] = f'SELECT {columns} FROM {table}'
        return self

    def where(self, condition):
        """
        Метод создания части запроса условий выбора данных из базы данных
        :param condition: Условия запроса
        :return: Экземляр класса QueryBuilder
        """
        logging.info('Запуск метода where для QueryBuilder')
        self._query['where'] = f'WHERE {condition}'
        return self

    def order_by(self, order, ord='ASC'):
        """
        Метод создания части запроса сортировки данных из базы данных
        :param order: Параметры сортировки
        :param ord: Метод сортировки (ASC - по возрастанию, DESC - по убыванию)
        :return: Экземляр класса QueryBuilder
        """
        logging.info('Запуск метода order_by для QueryBuilder')
        self._query['order_by'] = f'ORDER BY {order} {ord}'
        return self

    def values(self, *values):
        """
        Метод добавления значений для вставки данных в базу данных
        :param values: Параметры для вставки в базу данных
        :return: Экземляр класса QueryBuilder
        """
        logging.info('Запуск метода values для QueryBuilder')
        self._params.extend(values)
        return self

    def add_params(self, *parameters):
        """
        Метод для добавления дополнительных параметров
        :param parameters: Дополнитеьлные параметры для вставки в базу данных
        :return: Экземляр класса QueryBuilder
        """
        logging.info('Запуск метода add_params для QueryBuilder')
        self._params.extend(parameters)
        return self

    def get_params(self):
        """
        Метод для получения списка параметров
        :return: Список параметров
        """
        logging.info('Запуск метода get_params для QueryBuilder')
        return self._params

    def insert_into(self, table, columns):
        """
        Метод создания части запроса для вставки данных в базу данных
        :param table: Наименование таблицы, в которую добавляются данные
        :param columns: Столбцы, в которые добавляются данные
        :return: Экземляр класса QueryBuilder
        """
        logging.info('Запуск метода insert_into для QueryBuilder')
        cols = ','.join(columns)
        placeholders = ','.join(['?'] * len(columns))
        self._query['insert_into'] = f'INSERT INTO {table} ({cols})'
        self._query['values'] = f'VALUES ({placeholders})'
        return self

    def get_query(self):
        """
        Метод создания итогового запроса
        :return: Экземляр класса QueryBuilder
        """
        logging.info('Запуск метода get_query для QueryBuilder')
        query = ''
        if self._query['select']:
            query = f'{self._query["select"]}'
        if self._query['where']:
            query += f'\n{self._query["where"]}'
        if self._query['order_by']:
            query += f'\n{self._query["order_by"]}'
        if self._query['insert_into']:
            query = f'{self._query['insert_into']} {self._query['values']}'
        return query


class DBConnectionManager:
    """
    Класс управления соединением с базой данных
    """
    def __init__(self, bd: BDFactory):
        """
        Конструктор класса DBConnectionManager
        :param bd: база данных
        """
        self._bd = bd
        self._connection = None

    def get_connection(self):
        """
        Метод подключения к базе данных
        :return: Подключение к базе данных
        """
        logging.info('Запуск метода get_connection для DBConnectionManager')
        if self._connection is None:
            self._connection = self._bd.connect()
        return self._connection

    def close_connection(self):
        """
        Метод закрытия подключения к базе данных
        """
        logging.info('Запуск метода close_connection для DBConnectionManager')
        if self._connection:
            self._connection.close()
            self._connection = None
