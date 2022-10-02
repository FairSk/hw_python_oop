from dataclasses import asdict, dataclass, fields


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO = (
        'Тип тренировки: {0}; '
        'Длительность: {1:.3f} ч.; '
        'Дистанция: {2:.3f} км; '
        'Ср. скорость: {3:.3f} км/ч; '
        'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        return self.INFO.format(*asdict(self).values())


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    TIME_IN_MIN = 60

    action: float
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65
    SPEED_MULTIPLIER = 18
    DELTA_MULTIPLIER = 20

    def get_spent_calories(self):
        return ((self.SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 - self.DELTA_MULTIPLIER)
                * self.weight / self.M_IN_KM
                * self.TIME_IN_MIN * self.duration)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'SportsWalking'

    WEIGHT_MULTIPLIER_1 = 0.035
    WEIGHT_MULTIPLIER_2 = 0.029

    height: float

    def get_spent_calories(self):
        return ((self.WEIGHT_MULTIPLIER_1 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.WEIGHT_MULTIPLIER_2 * self.weight)
                * (self.duration * self.TIME_IN_MIN))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    WEIGHT_MULTIPLIER_1 = 1.1
    WEIGHT_MULTIPLIER_2 = 2

    length_pool: float
    count_pool: int

    def get_mean_speed(self):
        return (
            (self.length_pool
             * self.count_pool
             / self.M_IN_KM
             / self.duration))

    def get_spent_calories(self):
        return ((self.get_mean_speed()
                 + self.WEIGHT_MULTIPLIER_1)
                * self.WEIGHT_MULTIPLIER_2
                * self.weight)


WORKOUT_TYPES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking}


def read_package(workout_type: str, data) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUT_TYPES.keys():
        raise NotImplementedError('Unknown training type')

    elif len(data) != len(fields(WORKOUT_TYPES[workout_type])):
        raise KeyError('Wrong number of given parameters')

    return WORKOUT_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
