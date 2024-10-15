class InfoMessage:
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    LEN_STEP = 0.65  # Расстояние за один шаг
    M_IN_KM = 1000  # Перевод из метров в километры
    MIN_IN_H = 60  # Перевод из часов в минуты

    def __init__(self, action, duration, weight):
        self.action = action  # Количество действий (шагов, гребков)
        self.duration = duration  # Время тренировки в часах
        self.weight = weight  # Вес спортсмена в кг

    def get_distance(self):
        """Расчёт дистанции в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self):
        """Расчёт средней скорости движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Расчёт количества потраченных калорий (должен быть переопределён в подклассах)."""
        raise NotImplementedError('Метод должен быть переопределён')

    def show_training_info(self):
        """Возвращает объект сообщения о тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) *
            self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


class SportsWalking(Training):
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height  # Рост в сантиметрах

    def get_spent_calories(self):
        speed_m_per_sec = self.get_mean_speed() * self.KMH_IN_MSEC
        height_in_m = self.height / self.CM_IN_M
        return (
            (self.CALORIES_WEIGHT_MULTIPLIER * self.weight +
             (speed_m_per_sec ** 2 / height_in_m) *
             self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight) *
            self.duration * self.MIN_IN_H
        )



class Swimming(Training):
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # Длина бассейна в метрах
        self.count_pool = count_pool  # Количество переплываний бассейна

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool) / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) *
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight * self.duration
        )


def read_package(workout_type, data):
    workout_classes = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type in workout_classes:
        return workout_classes[workout_type](*data)
    return None


def main(training):
    if training is not None:
        message = training.show_training_info()
        print(message.get_message())
    else:
        print("Неизвестный тип тренировки.")


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
