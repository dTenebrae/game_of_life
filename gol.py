from collections import deque
import argparse
import numpy as np
import matplotlib.pyplot as plt


class Field:
    def __init__(self):
        # очередь для проверки на стабильность поля
        self.same = deque([_ for _ in range(5)], maxlen=10)
        # Создаем одномерный массив из 0/1 с вероятностями p
        # Вероятность мертвой клетки 1 - LIFE_PRT (то есть клетка будет иметь значение 0,
        # с вероятностью 95%). Живой - соостветственно наоборот
        self.fieldmap = np.array([np.random.choice([0, 1], size=FIELD_SIZE ** 2,
                                                   p=[1 - LIFE_PRT / 100, LIFE_PRT / 100])])
        # решейпим поле в 2D
        self.fieldmap.shape = (self.fieldmap.size // FIELD_SIZE, FIELD_SIZE)

    def new_turn(self):
        # Итерируемся по полю
        for ix, iy in np.ndindex(self.fieldmap.shape[0], self.fieldmap.shape[1]):
            # сохраняем значение клетки и сумму ее окружения
            cell = self.fieldmap[ix, iy]
            # берем 9 клеток (8 из окружения и сама клетка), суммируем (так как значения 0, 1)
            # вычитаем исследуемую клетку
            arnd = self.fieldmap[ix - 1: ix + 2, iy - 1: iy + 2].sum() - cell
            # если клетка мертвая и вокруг 3 живых - создаем жизнь
            if arnd == 3 and cell == 0:
                self.fieldmap[ix, iy] = 1
            # иначе если вокруг живой клетки меньше 2х или больше 3х клеток - убиваем
            # итого получается, что не охваченные условиями клетки остаются в прежних состояниях
            elif cell and (arnd < 2 or arnd > 3):
                self.fieldmap[ix, iy] = 0


def parse_args():
    parser = argparse.ArgumentParser(description="Conway's Game of Life yet another implementation")
    parser.add_argument(
        '-f',
        '--field-size',
        type=int,
        default=128,
        help="Field size in cells. You need to specify just one side, since it's square anyway... Default is 128x128"
    )
    parser.add_argument(
        '-l',
        '--life-proc',
        type=int,
        default=5,
        help="Percent of alive cells. Default value is 5"
    )
    parser.add_argument(
        '-t',
        '--time',
        type=int,
        default=40,
        help="Pause between ticks in milliseconds. Default value is 40"
    )
    parser.add_argument(
        '-s',
        '--seed',
        type=int,
        default=None,
        help="Seed for random number generator. Default value is None, for random start every time"
    )

    return parser.parse_args()


if __name__ == "__main__":
    # ####### initial values ###########
    args = parse_args()
    # Размер поля
    FIELD_SIZE = args.field_size
    # Процент живых клеток на поле
    LIFE_PRT = args.life_proc
    # seed для генератора случайных чисел
    SEED = args.seed
    # cколько времени стоим на паузе, переводим из миллисекунда в секунды
    PAUSE = args.time / 1000
    # выбираем сид, с которым будем инициализироваться
    np.random.seed(SEED)
    # ##################################

    new_field = Field()
    # Цикл до тех пор пока на поле есть живые и живых менее 39% (эмпирическим путем выясненная величина,
    # стабильное состояние игрового поля). Кроме того, заканчиваем, если в течение 10 ходов ничего не
    # поменялось

    # Вынес из условия цикла, чтобы не плодить ненужные расчеты
    overpopulated = FIELD_SIZE ** 2 * .39
    current_sum = new_field.fieldmap.sum()

    while current_sum and current_sum < overpopulated and len(set(new_field.same)) > 1:
        # spy - предназначен для отрисовки разреженных матриц, но сгодится и для нас
        plt.spy(new_field.fieldmap, markersize=2)
        plt.title(f'{(current_sum * 100 / FIELD_SIZE ** 2):.2f}%')
        plt.draw()
        plt.pause(PAUSE)
        plt.clf()
        new_field.new_turn()
        current_sum = new_field.fieldmap.sum()
        new_field.same.append(current_sum)
