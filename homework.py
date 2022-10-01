from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFO: str = (
        'Тип тренировки: {0}; '
        'Длительность: {1:.3f} ч.; '
        'Дистанция: {2:.3f} км; '
        'Ср. скорость: {3:.3f} км/ч; '
        'Потрачено ккал: {4:.3f}.')

    def get_message(self) -> str:
        return self.INFO.format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories)


@dataclass
class Training:
    """Базовый класс тренировки."""
    training_type = 'Default'
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
            self.training_type,
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    training_type = 'Running'
    LEN_STEP = 0.65
    KOEFF1 = 18
    KOEFF2 = 20

    def get_spent_calories(self):
        mass = self.weight
        koeff = self.M_IN_KM
        time = self.duration
        first = self.KOEFF1 * self.get_mean_speed() - self.KOEFF2
        return first * mass / koeff * (time * self.TIME_IN_MIN)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'SportsWalking'

    KOEFF1 = 0.035
    KOEFF2 = 0.029
    KOEFF3 = 2

    action: float
    duration: float
    weight: float
    height: float

    def get_spent_calories(self):
        first = self.KOEFF1 * self.weight
        second = (self.get_mean_speed() ** self.KOEFF3 // self.height)
        third = self.KOEFF2 * self.weight
        fourth = (self.duration * self.TIME_IN_MIN)
        return (first + second * third) * fourth


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'Swimming'

    LEN_STEP = 1.38
    KOEFF1 = 1.1
    KOEF2 = 2

    action: float
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self):
        first = self.length_pool * self.count_pool / self.M_IN_KM
        second = self.duration
        return first / second

    def get_spent_calories(self):
        return (self.get_mean_speed() + self.KOEFF1) * self.KOEF2 * self.weight


WORKOUT_TYPES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking}


def read_package(workout_type: str, data) -> Training:
    """Прочитать данные полученные от датчиков."""
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
