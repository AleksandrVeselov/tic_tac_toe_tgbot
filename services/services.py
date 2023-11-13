game_filed = [[0] * 3 for _ in range(3)]  # игровое поле в виде матрицы с цифрами


class Game:

    def __init__(self):
        self.game_field = [[' '] * 3 for _ in range(3)]  # игровое поле в виде матрицы с цифрами
        self.queue_flag = 1  # флаг очереди: 1 - ход игрока, 2 - ход компьютера
        self.human_letter = 1  # фигура игрока (1 - Х)
        self.computer_letter = 2  # фигура компьютера (2 - О)

    def is_winner(self, letter: int, field_copy=None) -> bool:
        """
        Функция проверки выигрышной ситуации
        :param field_copy: Копия игрового поля
        :param letter: число - символ игрока (1) или компьютера (2)
        :return: True или False
        """
        game_field = field_copy if field_copy else self.game_field

        # проверка строк
        for row in game_field:
            if all([element == letter for element in row]):
                return True

        main_diag = []  # главная диагональ
        secondary_diag = []  # побочная диагональ

        # Проверка колонок и диагоналей
        for row in range(3):
            col = []  # список значений в колонке
            for column in range(3):
                col.append(game_field[column][row])

                # Добавление в список значения на главной диагонали
                if row == column:
                    main_diag.append(game_field[row][column])

                # Добавление в список значения на побочной диагонали
                if row + column + 1 == 3:
                    secondary_diag.append(game_field[row][column])

            # проверка столбца
            if all([element == letter for element in col]):
                return True

        # проверка главной и побочной диагоналей
        if all([element == letter for element in main_diag]) or all([element == letter for element in secondary_diag]):
            return True

        return False

    @staticmethod
    def get_field_copy(field: list[list]) -> list[list]:
        """
        Функция делает копию игрового поля
        :param field: текущее состояние игрового поля
        :return: копия текущего состояния игрового поля
        """
        field_copy = [[element for element in row] for row in field]
        return field_copy

    def computer_move(self) -> tuple[int, int]:
        """
        Алгоритм просчета хода компьютера
        :return: координаты хода компьютера
        """

        # Проверка есть ли победный ход
        for i in range(0, 3):
            for j in range(0, 3):
                field_copy = self.get_field_copy(self.game_field)  # Создание копии игрового поля
                if self.is_space_free((i, j), field_copy):  # Проверка свободна ли клетка
                    self.make_move(self.computer_letter, (i, j), field_copy)  # Если свободна пробуем сделать туда ход
                    if self.is_winner(self.computer_letter, field_copy):  # Проверка есть ли выигрыш
                        return i, j

        # Проверка есть ли победный ход у игрока
        for i in range(0, 3):
            for j in range(0, 3):
                field_copy = self.get_field_copy(self.game_field)  # Создание копии игрового поля
                if self.is_space_free((i, j), field_copy):  # Проверка свободна ли клетка
                    self.make_move(self.human_letter, (i, j), field_copy)  # Если свободна пробуем сделать туда ход
                    if self.is_winner(self.human_letter, field_copy):  # Проверка есть ли выигрыш
                        return i, j

        # Проверка свободны ли угловые клетки
        corner_moves = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for move in corner_moves:
            if self.is_space_free(move):
                return move

        # Проверка свободен ли центр игрового поля
        if self.is_space_free((1, 1)):
            return 1, 1

        # Делаем ход посередине одной из строк или столбцов
        center_moves = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for move in center_moves:
            if self.is_space_free(move):
                return move

    def is_board_full(self) -> bool:
        """
        Проверка есть ли свободные клетки на игровом поле
        :return: Свободна ли клетка
        """
        for i in range(3):
            for j in range(3):
                if self.is_space_free((i, j)):
                    return False
        else:
            return True

    def make_move(self, letter: int, move: tuple[int, int], field_copy=None) -> None:
        """
        Ставит в переданное ей игровое поле 2 по соответствующим координатам
        :param field_copy: Копия игрового поля
        :param letter: фигура игрока или компьютера
        :param move: координаты хода
        :return: None
        """

        if field_copy:
            field_copy[move[0]][move[1]] = letter
        else:
            self.game_field[move[0]][move[1]] = letter

    def is_space_free(self, move: tuple[int, int], field_copy=None) -> bool:
        """
        Проверка, свободна ли клетка с переданными координатами
        :param field_copy: Копия игрового поля
        :param move: кортеж с координатами хода
        :return: свободна клетка с переданными координатами (==0) или нет (==1 или ==2)
        """

        if field_copy:
            return field_copy[move[0]][move[1]] == ' '

        return self.game_field[move[0]][move[1]] == ' '

    def reload_field(self):
        """сброс состояния игрового поля"""
        self.game_field = [[' '] * 3 for _ in range(3)]
