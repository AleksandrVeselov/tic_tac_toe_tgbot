
game_filed = [[0] * 3 for _ in range(3)]  # игровое поле в виде матрицы с цифрами


def is_winner(board: list[list[int]], letter: int) -> bool:
    """
    Функция проверки выигрышной ситуации
    :param board: игровое поле в виде списка списков с числами 0, 1, 2
    :param letter: число - символ игрока (1) или компьютера (2)
    :return: True или False
    """

    # проверка строк
    for row in board:
        if all([element == letter for element in row]):
            return True

    main_diag = []  # главная диагональ
    secondary_diag = []  # побочная диагональ

    # Проверка колонок и диагоналей
    for row in range(3):
        col = []  # список значений в колонке
        for column in range(3):
            col.append(board[column][row])

            # Добавление в список значения на главной диагонали
            if row == column:
                main_diag.append(board[row][column])

            # Добавление в список значения на побочной диагонали
            if row + column + 1 == 3:
                secondary_diag.append(board[row][column])

        # проверка столбца
        if all([element == letter for element in col]):
            return True

    # проверка главной и побочной диагоналей
    if all([element == letter for element in main_diag]) or all([element == letter for element in secondary_diag]):
        return True

    return False


def get_field_copy(field: list[list]) -> list[list]:
    """
    Функция делает копию игрового поля
    :param field: текущее состояние игрового поля
    :return: копия текущего состояния игрового поля
    """
    field_copy = [[element for element in row] for row in field]
    return field_copy


def computer_move(game_field: list[list[int]], letter=(1, 2)) -> tuple[int, int]:
    """
    Алгоритм просчета хода компьютера
    :param game_field: текущее состояние игрового поля
    :param letter: игрока и компьютера соответственно
    :return: координаты хода компьютера
    """

    # Проверка есть ли победный ход
    for i in range(0, 3):
        for j in range(0, 3):
            field_copy = get_field_copy(game_field)  # Создание копии игрового поля
            if is_space_free(field_copy, (i, j)):  # Проверка свободна ли клетка
                make_move(field_copy, letter[1], (i, j))  # Если свободна пробуем сделать туда ход
                if is_winner(field_copy, letter[1]):  # Проверка есть ли выигрыш
                    return i, j

    # Проверка есть ли победный ход у игрока
    for i in range(0, 3):
        for j in range(0, 3):
            field_copy = get_field_copy(game_field)  # Создание копии игрового поля
            if is_space_free(field_copy, (i, j)):  # Проверка свободна ли клетка
                make_move(field_copy, letter[0], (i, j))  # Если свободна пробуем сделать туда ход
                if is_winner(field_copy, letter[0]):  # Проверка есть ли выигрыш
                    return i, j

    # Проверка свободны ли угловые клетки
    corner_moves = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for move in corner_moves:
        if is_space_free(game_field, move):
            return move

    # Проверка свободен ли центр игрового поля
    if is_space_free(game_field, (1, 1)):
        return 1, 1

    # Делаем ход посередине одной из строк или столбцов
    center_moves = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for move in center_moves:
        if is_space_free(game_field, move):
            return move


def is_board_full(game_field: list[list]) -> bool:
    """
    Проверка есть ли свободные клетки на игровом поле
    :param game_field: Текущее состояние игрового поля
    :return: Свободна ли клетка
    """
    for i in range(3):
        for j in range(3):
            if is_space_free(game_field, (i, j)):
                return False
    else:
        return True


def make_move(field: list[list[int]], letter: int, move: tuple[int, int]) -> None:
    """
    Ставит в переданное ей игровое поле 2 по соответствующим координатам
    :param field: текущее состояние игрового поля
    :param letter: символ за который играет компьютер (по умолчанию передается 2)
    :param move: координаты хода
    :return: None
    """

    field[move[0]][move[1]] = letter


def is_space_free(board: list[list], move: tuple[int, int]) -> bool:
    """
    Проверка, свободна ли клетка с переданными координатами
    :param board: текущее состояние игрового поля
    :param move: кортеж с координатами хода
    :return: свободна клетка с переданными координатами (==0) или нет (==1 или ==2)
    """
    return board[move[0]][move[1]] == 0

