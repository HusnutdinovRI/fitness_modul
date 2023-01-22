class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: float,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    """Константа для перевода значений из метров километры"""

    MIN_IN_H = 60
    """Константа для перевода значений из минут в часы"""

    LEN_STEP = 0.65
    """Расстояние преодолеваемое за одно действие"""

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
        return InfoMessage(self.__str__(), self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())

    def __str__(self) -> str:
        return self.__class__.__name__


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    """Контстанты для подсчёта каллорий при беге"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT
                ) * self.weight / self.M_IN_KM * (
                    self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KHP_TO_MPS = 0.278
    """Контстанта для перевода значений из км/ч в м/с"""

    SM_TO_M = 100
    """Контстанта для перевода значений из сантиметров в метры"""

    CALORIES_WALK_MULTIPLIER = 0.035
    CALORIES_WALK_SHIFT = 0.029
    """Контстанты для подсчёта каллорий при ходьбе"""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WALK_MULTIPLIER * self.weight + ((
            self.get_mean_speed() * self.KHP_TO_MPS)**2
            / self.height * self.SM_TO_M) * self.CALORIES_WALK_SHIFT
            * self.weight) * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_SWIMMING_MULTIPLIER = 1.1
    CALORIES_SWIMMING_SHIFT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + self.CALORIES_SWIMMING_MULTIPLIER
                ) * self.CALORIES_SWIMMING_SHIFT * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainig_action = {'SWM': Swimming,
                      'RUN': Running,
                      'WLK': SportsWalking}

    training_class: Training = trainig_action[workout_type](*data)

    return training_class


def main(training: Training) -> None:

    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    result: str = info.get_message()
    print(result)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
