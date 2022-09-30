class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    STR_INFO: str = ('Тип тренировки: {0}; '
                     'Длительность: {1:.3f} ч.; '
                     'Дистанция: {2:.3f} км; '
                     'Ср. скорость: {3:.3f} км/ч; '
                     'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        return self.STR_INFO.format(self.training_type,
                                    self.duration,
                                    self.distance,
                                    self.speed,
                                    self.calories)


class Training:
    """Базовый класс тренировки."""
    training_type = 'Default'
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    training_type = 'Running'
    LEN_STEP = 0.65

    def get_spent_calories(self):
        speed = self.get_mean_speed()
        mass = self.weight
        koeff = self.M_IN_KM
        time = self.duration
        return (18 * speed - 20) * mass / koeff * (time * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'SportsWalking'

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        first = 0.035 * self.weight
        second = (self.get_mean_speed()**2 // self.height)
        third = 0.029 * self.weight
        fourth = (self.duration * 60)
        return (first + second * third) * fourth


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'Swimming'

    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        first = self.length_pool * self.count_pool / self.M_IN_KM
        second = self.duration
        return first / second

    def get_spent_calories(self):
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
