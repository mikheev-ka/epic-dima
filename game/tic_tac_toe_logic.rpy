# ============================================================
# МИНИ-ИГРА «КРЕСТИКИ-НОЛИКИ» (TIC-TAC-TOE)
# ============================================================
# Правила: игрок (X) против компьютера (O).
# Поле 3×3, ход по клику, компьютер ходит случайно.
# Завершение: победа/поражение/ничья.
# Ничья → реванш или выход.
# ============================================================

# ---------- ИНИЦИАЛИЗАЦИЯ PYTHON-МОДУЛЯ ----------
# Здесь мы импортируем стандартный модуль random для случайного выбора
# клетки компьютером, а также определяем вспомогательные функции.
init python:
    import random

    # ----- ФУНКЦИЯ ПРОВЕРКИ ПОБЕДИТЕЛЯ -----
    # Принимает список board из 9 элементов (символы 'X', 'O' или пробел).
    # Проверяет все выигрышные линии: строки, столбцы, диагонали.
    # Если находит три одинаковых непустых символа, возвращает этот символ ('X' или 'O').
    # Иначе возвращает None — победителя нет.
    def check_ttt_winner(board):
        """Возвращает 'X', 'O' или None (если победителя нет)"""
        win_lines = [
            [0,1,2], [3,4,5], [6,7,8],  # строки
            [0,3,6], [1,4,7], [2,5,8],  # столбцы
            [0,4,8], [2,4,6]            # диагонали
        ]
        for line in win_lines:
            a, b, c = line
            if board[a] == board[b] == board[c] and board[a] != " ":
                return board[a]
        return None

    # ----- ФУНКЦИЯ ПРОВЕРКИ НИЧЬЕЙ -----
    # Возвращает True, если все клетки заняты (нет пробелов) и при этом
    # нет победителя (check_ttt_winner вернул None).
    # Это состояние ничьей (заполненное поле без выигрышной линии).
    def is_ttt_draw(board):
        """Возвращает True, если все клетки заняты и нет победителя"""
        return " " not in board and check_ttt_winner(board) is None

    # ----- ХОД КОМПЬЮТЕРА (СЛУЧАЙНЫЙ) -----
    # Находит все индексы клеток, где стоит пробел, и выбирает один случайно.
    # Возвращает индекс или None, если свободных клеток нет.
    def ttt_computer_move(board):
        """Возвращает индекс свободной клетки или None"""
        free = [i for i, cell in enumerate(board) if cell == " "]
        if free:
            return random.choice(free)
        return None


# ---------- ПЕРЕМЕННЫЕ СОСТОЯНИЯ ----------
# Все переменные объявлены с default для сохранения состояния между сессиями.
# ttt_board — список из 9 элементов, представляющий игровое поле.
# ttt_turn — чей сейчас ход: "player" или "computer".
# ttt_winner — результат: "player", "computer", "draw" или None (игра продолжается).
# ttt_game_over — флаг завершения партии (True/False).
# ttt_stake — ставка в игре (влияет на денежный выигрыш/проигрыш).
# ttt_computer_thinking — блокировка повторных вызовов хода компьютера (таймер).
# ttt_result_phrase — случайная фраза, сопровождающая итог игры.
default ttt_board = [" "] * 9
default ttt_turn = "player"          # "player" или "computer"
default ttt_winner = None            # "player", "computer", "draw" или None
default ttt_game_over = False
default ttt_stake = 30
default ttt_computer_thinking = False  # блокировка во время хода компьютера
default ttt_result_phrase = ""        # фиксированная фраза результата

# Списки фраз для разных исходов (глобальные, чтобы быть доступными в функциях).
# Они заданы через default, чтобы можно было изменять во время игры (например, добавлять новые).
default win_phrases = [
    "Отличная стратегия!", "Гений!", "Вы непобедимы!",
    "Красивая партия!", "Противник повержен!", "Блестящий ход!",
    "Мастерство высшего класса!", "Вы обыграли машину!",
    "Так держать!", "Победа за вами!"
]
default lose_phrases = [
    "Ой, в этот раз не повезло...", "Компьютер оказался сильнее",
    "Попробуйте ещё раз!", "Тактика требует доработки",
    "Удача была на стороне машины", "Не расстраивайтесь, бывает",
    "Следующий раз обязательно выиграете",
    "Искусственный интеллект непреклонен",
    "Хорошая попытка, но недостаточно", "Поражение – это опыт"
]
default draw_phrases = [
    "Боевая ничья!", "Силы равны", "Могло быть лучше, но и так неплохо",
    "Равный бой", "Дружба победила!", "Ничья – честный исход",
    "Сыграли вничью, достойно", "Компьютер не уступает, вы тоже",
    "В следующий раз повезёт", "Мир во всём мире"
]

# Инициализация Python-функции, которая выбирает случайную фразу из соответствующего списка
# в зависимости от переданного победителя.
init python:
    def ttt_set_phrase(winner):
        """Выбирает случайную фразу для результата и сохраняет в ttt_result_phrase"""
        global ttt_result_phrase
        if winner == "player":
            ttt_result_phrase = random.choice(win_phrases)
        elif winner == "computer":
            ttt_result_phrase = random.choice(lose_phrases)
        elif winner == "draw":
            ttt_result_phrase = random.choice(draw_phrases)


# ---------- МЕТКА ЗАПУСКА ИГРЫ (СОВМЕСТИМА С СТАРЫМИ ВЫЗОВАМИ) ----------
# Эта метка используется для запуска мини-игры из сценария.
# Принимает необязательный параметр stake (ставка), по умолчанию 30.
# Она инициализирует все переменные, показывает экран, и по завершении
# изменяет деньги игрока в зависимости от исхода:
#   - победа игрока: прибавляет удвоенную ставку (выигрыш + возврат ставки)
#   - поражение или ничья (ничья считается проигрышем, т.к. ставка не возвращается): вычитает ставку
# Возвращает строку: "player", "ai" или "draw" для использования в сценарии.
label play_checkers(stake=30):
    $ ttt_stake = stake
    $ ttt_board = [" "] * 9
    $ ttt_turn = "player"
    $ ttt_winner = None
    $ ttt_game_over = False
    $ ttt_computer_thinking = False
    $ ttt_result_phrase = ""

    call screen ttt_game_screen

    if ttt_winner == "player":
        $ money += ttt_stake * 2
        return "player"
    elif ttt_winner == "computer":
        $ money -= ttt_stake
        return "ai"
    else:
        # Если ничья или что-то пошло не так, считаем проигрышем.
        if ttt_winner == "draw":
            return "draw"
        else:
            $ money -= ttt_stake
            return "ai"


# ---------- ЭКРАН ИГРЫ ----------
# Это основной экран, отображающий поле, статус и кнопки.
# Он модальный (modal True), то есть блокирует взаимодействие с остальной игрой.
screen ttt_game_screen():
    modal True

    # --- Таймер для хода компьютера ---
    # Каждые 0.1 секунды проверяет, не пора ли компьютеру сделать ход.
    # Используется условие If: если игра не окончена (not ttt_game_over),
    # то вызывается функция ttt_computer_turn(), иначе ничего не делается.
    # repeat True — таймер будет срабатывать бесконечно, пока экран открыт.
    timer 0.1 repeat True action If(not ttt_game_over, Function(ttt_computer_turn), None)

    # --- ОСНОВНАЯ КОМПОНОВКА ---
    # Полупрозрачный фон для затемнения игрового пространства.
    frame:
        background "#00000080"
        xfill True yfill True
        xalign 0.5 yalign 0.5

        vbox:
            spacing 20
            xalign 0.5 yalign 0.5

            # Заголовок игры
            text "Крестики-нолики" size 48 bold True color "#ffcc00" xalign 0.5

            # Блок отображения статуса игры
            if ttt_game_over:
                # Если игра окончена, показываем результат и случайную фразу
                if ttt_winner == "player":
                    text "ПОБЕДА!" size 40 color "#66ff66" xalign 0.5
                    text "[ttt_result_phrase]" size 24 color "#cccccc" xalign 0.5
                elif ttt_winner == "computer":
                    text "ПОРАЖЕНИЕ..." size 40 color "#ff6666" xalign 0.5
                    text "[ttt_result_phrase]" size 24 color "#cccccc" xalign 0.5
                elif ttt_winner == "draw":
                    text "НИЧЬЯ!" size 40 color "#ffff66" xalign 0.5
                    text "[ttt_result_phrase]" size 24 color "#cccccc" xalign 0.5
            else:
                # Если игра не окончена, выводим подсказку, чей ход
                if ttt_computer_thinking:
                    text "Ход компьютера..." size 28 color "#ff9966" xalign 0.5
                else:
                    text "Ваш ход (X)" size 28 color "#66ccff" xalign 0.5

            # Игровое поле — сетка 3×3 из кнопок
            grid 3 3:
                spacing 10
                xalign 0.5
                for i in range(9):
                    button:
                        xysize (180, 180)
                        # Фон кнопки зависит от содержимого клетки:
                        # если пусто — тёмно-серый (#444), если X или O — чуть темнее (#2a2a2a)
                        background (
                            "#444" if ttt_board[i] == " " else
                            "#2a2a2a" if ttt_board[i] == "X" else
                            "#2a2a2a"
                        )
                        # При наведении меняем фон только если клетка пуста, игра не окончена,
                        # ход игрока и компьютер не думает — чтобы показать доступность.
                        hover_background (
                            "#666" if ttt_board[i] == " " and not ttt_game_over and ttt_turn == "player" and not ttt_computer_thinking else
                            None
                        )
                        # Действие: если клетка пуста, игра не окончена, ход игрока, компьютер не думает —
                        # вызываем ttt_player_move(i). Иначе — ничего не делаем (None).
                        action (
                            If(
                                not ttt_game_over and ttt_turn == "player" and not ttt_computer_thinking and ttt_board[i] == " ",
                                Function(ttt_player_move, i),
                                None
                            )
                        )
                        # Отображение символа в клетке: X — голубым, O — красным.
                        if ttt_board[i] == "X":
                            text "X" size 80 color "#66ccff" bold True xalign 0.5 yalign 0.5
                        elif ttt_board[i] == "O":
                            text "O" size 80 color "#ff6666" bold True xalign 0.5 yalign 0.5
                        else:
                            text "" size 80 xalign 0.5 yalign 0.5

            # Нижняя панель с кнопками управления
            hbox:
                spacing 30
                xalign 0.5
                if ttt_game_over:
                    # Если игра завершена:
                    # При ничьей предлагаем сыграть ещё раз (сброс) или выйти.
                    # При победе/поражении — только выйти (продолжить).
                    if ttt_winner == "draw":
                        textbutton "Сыграть ещё раз" action Function(ttt_reset_game) xsize 200
                        textbutton "Выйти" action Return() xsize 200
                    else:
                        textbutton "Продолжить" action Return() xsize 200
                else:
                    # Если игра ещё идёт, даём кнопку сдаться.
                    textbutton "Сдаться" action Function(ttt_concede) xsize 200


# ---------- ФУНКЦИИ УПРАВЛЕНИЯ ИГРОЙ ----------
# Все функции объявлены внутри init python, чтобы быть доступными из экрана.
init python:
    def ttt_player_move(index):
        """Обработка хода игрока по индексу клетки"""
        global ttt_board, ttt_turn, ttt_winner, ttt_game_over, ttt_computer_thinking
        # Защита от некорректных вызовов: если игра окончена, ход не игрока,
        # компьютер думает, или клетка уже занята — выходим.
        if ttt_game_over or ttt_turn != "player" or ttt_computer_thinking or ttt_board[index] != " ":
            return

        # Ставим крестик
        ttt_board[index] = "X"
        # Проверяем, не победил ли игрок
        winner = check_ttt_winner(ttt_board)
        if winner == "X":
            ttt_winner = "player"
            ttt_game_over = True
            ttt_set_phrase("player")
            return
        # Проверяем ничью после хода игрока
        elif is_ttt_draw(ttt_board):
            ttt_winner = "draw"
            ttt_game_over = True
            ttt_set_phrase("draw")
            return

        # Если игра не завершена, передаём ход компьютеру
        ttt_turn = "computer"

    def ttt_computer_turn():
        """Вызывается таймером, выполняет ход компьютера, если настала его очередь"""
        global ttt_board, ttt_turn, ttt_winner, ttt_game_over, ttt_computer_thinking
        # Если игра окончена, ход не компьютера, или компьютер уже думает — выходим.
        if ttt_game_over or ttt_turn != "computer" or ttt_computer_thinking:
            return

        # Устанавливаем флаг мышления, чтобы избежать повторных вызовов
        ttt_computer_thinking = True

        # Получаем случайный свободный индекс
        idx = ttt_computer_move(ttt_board)
        # Если свободных клеток нет (не должно случиться, т.к. проверка ничьей уже была)
        # Но на всякий случай проверяем и завершаем ничьей.
        if idx is None:
            if is_ttt_draw(ttt_board):
                ttt_winner = "draw"
                ttt_game_over = True
                ttt_set_phrase("draw")
            ttt_computer_thinking = False
            return

        # Ставим нолик
        ttt_board[idx] = "O"
        # Проверяем, победил ли компьютер
        winner = check_ttt_winner(ttt_board)
        if winner == "O":
            ttt_winner = "computer"
            ttt_game_over = True
            ttt_set_phrase("computer")
            ttt_computer_thinking = False
            return
        # Проверяем ничью после хода компьютера
        elif is_ttt_draw(ttt_board):
            ttt_winner = "draw"
            ttt_game_over = True
            ttt_set_phrase("draw")
            ttt_computer_thinking = False
            return

        # Если игра не завершена, передаём ход игроку
        ttt_turn = "player"
        ttt_computer_thinking = False

    def ttt_concede():
        """Сдача: игрок признаёт поражение, компьютер объявляется победителем"""
        global ttt_winner, ttt_game_over
        ttt_winner = "computer"
        ttt_game_over = True
        ttt_set_phrase("computer")

    def ttt_reset_game():
        """Сброс состояния для реванша (при ничьей)"""
        global ttt_board, ttt_turn, ttt_winner, ttt_game_over, ttt_computer_thinking, ttt_result_phrase
        ttt_board = [" "] * 9
        ttt_turn = "player"
        ttt_winner = None
        ttt_game_over = False
        ttt_computer_thinking = False
        ttt_result_phrase = ""