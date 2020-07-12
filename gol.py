from collections import deque
import numpy as np
import matplotlib.pyplot as plt

# CONST
# Размер поля
FIELD_SIZE = 120
# Процент живых клеток на поле
LIFE_PRT = 5


class Field:
    def __init__(self):
        # очередь для проверки на стабильность поля
        self.same = deque([_ for _ in range(5)], maxlen=10)
        # Создаем одномерный массив из 0/1 с вероятностями p и решейпим его в 2Д
        self.fieldmap = np.array([np.random.choice([0, 1], size=FIELD_SIZE ** 2,
                                                   p=[1 - LIFE_PRT / 100, LIFE_PRT / 100])])
        self.fieldmap.shape = (self.fieldmap.size // FIELD_SIZE, FIELD_SIZE)

    def new_turn(self):
        for ix, iy in np.ndindex(self.fieldmap.shape):
            # сохраняем значение клетки и сумму ее окружения
            cell = self.fieldmap[ix, iy]
            arnd = self.fieldmap[ix - 1: ix + 2, iy - 1: iy + 2].sum() - cell
            # если клетка мертвая и вокруг 3 живых - создаем жизнь
            if arnd == 3 and not cell:
                self.fieldmap[ix, iy] = 1
            # иначе если вокруг живой клетки меньше 2х или больше 3х клеток - убиваем
            elif cell and (arnd < 2 or arnd > 3):
                self.fieldmap[ix, iy] = 0


new_field = Field()
# Цикл до тех пор пока на поле есть живые и живых менее 39% (эмпирическим путем выясненная величина,
# стабильное состояние игрового поля). Кроме того, заканчиваем, если в течение 10 ходов ничего не
# поменялось
while new_field.fieldmap.sum() and (new_field.fieldmap.sum() < FIELD_SIZE ** 2 * .39) \
        and len(set(new_field.same)) > 1:
    current_sum = new_field.fieldmap.sum()
    new_field.same.append(current_sum)
    plt.spy(new_field.fieldmap, markersize=2)
    plt.title(f'{(current_sum * 100 / FIELD_SIZE ** 2):.2f}%')
    plt.draw()
    plt.pause(0.0411)
    plt.clf()
    new_field.new_turn()
