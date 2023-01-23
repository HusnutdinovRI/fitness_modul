from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = ('Тип тренировки: {};'
                    ' Длительность: {:.3f} ч.;'
                    ' Дистанция: {:.3f} км;'
                    ' Ср. скорость: {:.3f} км/ч;'
                    ' Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    """Константа для перевода значений из метров километры"""

    MIN_IN_H: int = 60
    """Константа для перевода значений из минут в часы"""

    LEN_STEP: float = 0.65
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
        raise NotImplementedError('Переопроедлите метод get_spent_calories '
                                  f'в {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())

    def __str__(self) -> str:
        return self.__class__.__name__


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
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

    KHP_TO_MPS: float = 0.278
    """Контстанта для перевода значений из км/ч в м/с"""

    SM_TO_M: int = 100
    """Контстанта для перевода значений из сантиметров в метры"""

    CALORIES_WALK_MULTIPLIER: float = 0.035
    CALORIES_WALK_SHIFT: float = 0.029
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
    LEN_STEP: float = 1.38
    CALORIES_SWIMMING_MULTIPLIER: float = 1.1
    CALORIES_SWIMMING_SHIFT: int = 2

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
    trainig_action: dict[str, Training] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking}

    try:
        training_class: Training = trainig_action[workout_type](*data)
    except KeyError:
        print("Неверная кодировка тренировки во входящих данных.")
    else:
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
