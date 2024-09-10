from flask import Flask, request, render_template
from repo import *
from mission import *
import cProfile

app = Flask(__name__)
repository = SqliteDroneRepository()
drone_controller = DroneController()
context = DroneContext()
PATH = 'templates/mission.html'


@app.route('/')
@app.route('/home')
def index():
    """
    Функция вызова начальной страницы
    :return: Начальная страница index.html
    """
    app.logger.info('Запуск начальной страницы приложения')
    return render_template('index.html')


@app.route('/drones', methods=['GET'])
def get_drones():
    """
    Функция вывода списка всех дронов
    :return: Страница со списком всех дронов
    """
    app.logger.info('Запуск функции get_drones')
    data = repository.get_all_drones()
    return render_template('all_drones.html', data=data)


@app.route('/drones/<drone_id>', methods=['GET', 'POST', 'UPDATE', 'DELETE'])
def actions_drone_by_id(drone_id):
    """
    Метод получения, обновления и удаления конкретного дрона
    :return: Информация о дроне, обновление или удаление дрона
    """
    pass


@app.route('/drone', methods=['GET', 'POST'])
def create_drone():
    """
        Функция создания нового дрона.
        :return: JSON-ответ с сообщением об успешном добавлении дрона и статус-код 201,
                 или ошибка 404, если не передан id дрона
    """
    app.logger.info('Запуск функции create_drones')
    if request.method == 'POST':
        max_altitude = int(request.form['max_altitude'])
        max_speed = int(request.form['max_speed'])
        max_flight_time = int(request.form['max_flight_time'])
        serial_number = request.form['serial_number']
        model = request.form['model']
        manufacturer = request.form['manufacturer']
        new_drone = Drone(max_altitude, max_speed, max_flight_time, serial_number, model, manufacturer)
        repository.add_drone(new_drone)
        return render_template('index.html')
    else:
        return render_template('add_drone.html')


@app.route('/drones/recon')
def recon_mission():
    """
    Функция выполнения разведовательной миссии
    :return: Страница вывода действий по стратегии
    """
    app.logger.info('Запуск функции recon_mission')
    with open(PATH, 'w', encoding='utf-8') as func:
        func.write('<!DOCTYPE html>\n<html lang="ru">\n<head>\n<meta charset="UTF-8">\n'
                '<title>Основная страница index</title>\n</head>\n<body>')
        func.write('<p style="font-weight: bold; font-size: 18px">====Разведка======</p>')

    context.set_strategy(ReconMissionStrategy())
    context.add_command(Takeoff(drone_controller))
    context.add_command(MoveForward(drone_controller, 100))
    context.add_command(MoveForward(drone_controller, 20))
    context.execute()

    with open(PATH, 'a', encoding='utf-8') as func:
        func.write('\n<a href="http://127.0.0.1:5000/">Вернуться на главную страницу</a>\n</body>\n</html>')
    return render_template('mission.html')


@app.route('/drone/patrol')
def patrol_mission():
    """
    Функция выполнения миссии патрулирования
    :return: Страница вывода действий по стратегии
    """
    app.logger.info('Запуск функции patrol_mission')
    with open(PATH, 'w', encoding='utf-8') as func:
        func.write('<!DOCTYPE html>\n<html lang="ru">\n<head>\n<meta charset="UTF-8">\n'
                '<title>Основная страница index</title>\n</head>\n<body>')
        func.write('<p style="font-weight: bold; font-size: 18px">====Патрулирование======</p>')

    context.set_strategy(PatrolMissionStrategy(n_patrols=3))
    context.add_command(Takeoff(drone_controller))
    for _ in range(3):
        context.add_command(MoveForward(drone_controller, 50))
        context.add_command(Turn(drone_controller, 90))
    context.execute()

    with open(PATH, 'a', encoding='utf-8') as func:
        func.write('\n<a href="http://127.0.0.1:5000/">Вернуться на главную страницу</a>\n</body>\n</html>')
    return render_template('mission.html')


if __name__ == '__main__':
    with cProfile.Profile() as pr:
        app.logger.info('Start cProfile')
        app.run(debug=True)
        app.logger.info('Stop cProfile')
        pr.print_stats()
