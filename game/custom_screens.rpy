# ============================================================
# КАСТОМНЫЕ ЭКРАНЫ (QTE, БОЕВОЙ HUD)
# ============================================================
#
# Этот файл содержит пользовательские экраны, используемые в игре:
# - экран быстрого выбора пути (qte_choice) с таймером,
# - экран уклонения в бою (dodge_choice) с тремя вариантами,
# - устаревший экран уклонения (dodge_qte) для совместимости,
# - боевой HUD (battle_hud) для отображения здоровья,
# - заглушка для старого экрана крестиков-ноликов,
# - стили для кнопок QTE и HUD.
#
# Все экраны используют переменные, определённые в других файлах
# (например, hp_player, hp_troll, max_hp_player, enemy_name и т.д.).
# ============================================================

# ---------- QTE ЭКРАН (ВЫБОР ПУТИ) ----------
# Этот экран появляется в самом начале подземелья, когда игроку нужно
# выбрать стратегию поведения перед встречей с троллем.
# У него есть 10 секунд, чтобы выбрать один из пяти путей.
# Если время истекает, автоматически выбирается путь "fear" (страх).
screen qte_choice():
    # Переменная time_left хранит оставшееся время в секундах.
    # Изначально установлена на 10.0 секунд.
    default time_left = 10.0

    # Таймер, который срабатывает каждые 0.05 секунды.
    # Он уменьшает time_left на 0.05, пока время > 0.
    # Когда время достигает 0, возвращает результат "fear" (путь страха).
    timer 0.05 repeat True action If(time_left > 0, SetScreenVariable("time_left", time_left - 0.05), Return("fear"))

    # --- Таймер (полупрозрачный, в правом верхнем углу) ---
    # Отображает оставшееся время в виде полосы и цифр.
    frame:
        background "#1a1a1a80"
        xalign 1.0
        yalign 0.02
        xpadding 20
        ypadding 10
        hbox:
            spacing 15
            text "Осталось:" color "#aaaaaa" size 18
            bar:
                value time_left
                range 10.0
                xsize 200
                ysize 12
                left_bar "#cc0000"
                right_bar "#333333"
            text "[int(time_left)] сек" color "#cc0000" size 18 bold True

    # --- Кнопки выбора (каждая в своей полупрозрачной рамке) ---
    # Пять вариантов: сила, дружба, интеллект (загадки), хитрость, страх.
    # Каждая кнопка при нажатии возвращает соответствующую строку
    # в метку, вызвавшую экран (в dungeon_exploration.rpy).
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 12

        textbutton "Вступить в бой" action Return("strength"):
            style "qte_choice_button"
            text_style "qte_menu_choice"
        textbutton "Составить план" action Return("friendship"):
            style "qte_choice_button"
            text_style "qte_menu_choice"
        textbutton "Перехитрить тролля" action Return("riddle"):
            style "qte_choice_button"
            text_style "qte_menu_choice"
        textbutton "Обыскать камеру" action Return("cunning"):
            style "qte_choice_button"
            text_style "qte_menu_choice"
        textbutton "Сдаться" action Return("fear"):
            style "qte_choice_button"
            text_style "qte_menu_choice"


# ---------- QTE УКЛОНЕНИЕ (ВЫБОР ИЗ ТРЁХ ВАРИАНТОВ) ----------
# Этот экран используется в боях с троллем и Кириллом.
# Игроку нужно за ограниченное время выбрать правильное действие,
# чтобы увернуться от атаки врага.
# Время уменьшается с каждым раундом (чем дальше бой, тем сложнее).
# Правильный вариант выбирается случайно при каждом вызове экрана.
screen dodge_choice(time=1.5, round=1):
    # time - максимальное время на принятие решения (передаётся из боя).
    # round - номер раунда (не используется в логике, но может быть полезно).
    default time_left = time
    default finished = False
    # wrong_choice - случайное число от 1 до 3, определяющее, какой из трёх
    # вариантов будет неправильным (то есть приведёт к провалу).
    # Если игрок выбирает вариант с этим числом, он не уклоняется.
    default wrong_choice = renpy.random.randint(1, 3)  # 1-уклон, 2-блок, 3-присесть

    # Таймер уменьшает time_left, и если время истекло, возвращает "fail".
    # При этом finished устанавливается в True, чтобы избежать повторных вызовов.
    timer 0.05 repeat True action If(
        time_left > 0 and not finished,
        SetScreenVariable("time_left", time_left - 0.05),
        If(
            not finished,
            [
                SetScreenVariable("finished", True),
                Return("fail")
            ]
        )
    )

    # --- Таймер (в правом верхнем углу, как в qte_choice) ---
    # Отображает оставшееся время.
    frame:
        background "#1a1a1a80"
        xalign 1.0
        yalign 0.02
        xpadding 20
        ypadding 10
        hbox:
            spacing 15
            text "Осталось:" color "#aaaaaa" size 18
            bar:
                value time_left
                range time
                xsize 200
                ysize 12
                left_bar "#cc0000"
                right_bar "#333333"
            text "[int(time_left)] сек" color "#cc0000" size 18 bold True

    # --- Кнопки выбора (по центру, как в qte_choice) ---
    # Три варианта: Уклониться, Блокировать, Присесть.
    # При нажатии проверяется, не истекло ли время, и если нет,
    # то сравнивается выбранный индекс с wrong_choice.
    # Если индекс совпадает - возвращается "fail", иначе "success".
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 12

        textbutton "Уклониться" action If(
            not finished,
            [
                SetScreenVariable("finished", True),
                If(
                    wrong_choice == 1,
                    Return("fail"),
                    Return("success")
                )
            ]
        ):
            style "qte_choice_button"
            text_style "qte_menu_choice"

        textbutton "Блокировать" action If(
            not finished,
            [
                SetScreenVariable("finished", True),
                If(
                    wrong_choice == 2,
                    Return("fail"),
                    Return("success")
                )
            ]
        ):
            style "qte_choice_button"
            text_style "qte_menu_choice"

        textbutton "Присесть" action If(
            not finished,
            [
                SetScreenVariable("finished", True),
                If(
                    wrong_choice == 3,
                    Return("fail"),
                    Return("success")
                )
            ]
        ):
            style "qte_choice_button"
            text_style "qte_menu_choice"


# ---------- QTE УКЛОНЕНИЕ В БОЮ (СТАРЫЙ, ОСТАВЛЯЕМ ДЛЯ СОВМЕСТИМОСТИ) ----------
# Это устаревший экран, который использовался в ранних версиях боя.
# Он оставлен для совместимости, но в текущей игре не применяется.
# Вместо него используется dodge_choice с тремя вариантами.
# Здесь кнопка "УКЛОНИТЬСЯ" появляется в случайной позиции на экране,
# что делало QTE сложнее. В новой версии выбор упрощён.
screen dodge_qte(time=1.0):
    default time_left = time
    default pos_x = renpy.random.randint(0, renpy.config.screen_width - 150)
    default pos_y = renpy.random.randint(0, renpy.config.screen_height - 40)

    timer 0.05 repeat True action If(time_left > 0, SetScreenVariable("time_left", time_left - 0.05), Return("fail"))

    frame:
        background "#1a1a1a80"
        xalign 1.0
        yalign 0.02
        xpadding 20
        ypadding 10
        hbox:
            spacing 15
            text "Осталось:" color "#aaaaaa" size 18
            bar:
                value time_left
                range time
                xsize 200
                ysize 12
                left_bar "#cc0000"
                right_bar "#333333"
            text "[int(time_left)] сек" color "#cc0000" size 18 bold True

    textbutton "УКЛОНИТЬСЯ" action Return("success"):
        xpos pos_x ypos pos_y
        style "dodge_btn"
        text_style "dodge_btn_text"


# ---------- ЭКРАН БОЕВОГО HUD ----------
# Отображается во время боя (с троллем, Кириллом и т.д.).
# Показывает текущее здоровье игрока и врага в виде полос и чисел.
# Использует переменные: hp_player, max_hp_player, hp_troll, max_hp_troll, enemy_name.
# Эти переменные инициализируются перед началом боя (в метках боя).
screen battle_hud():
    frame:
        background "#1a1a1a80"
        xalign 0.0
        yalign 0.02
        xpadding 15
        ypadding 10
        vbox:
            spacing 8
            # Блок здоровья игрока
            hbox:
                spacing 10
                text "Дима" color "#ffffff" size 18 bold True
                bar:
                    value hp_player
                    range max_hp_player
                    xsize 180
                    ysize 14
                    left_bar "#00cc00"
                    right_bar "#333333"
                text "[hp_player]/[max_hp_player]" color "#ffffff" size 16
            # Блок здоровья врага (имя берётся из переменной enemy_name)
            hbox:
                spacing 10
                text enemy_name color "#ffffff" size 18 bold True
                bar:
                    value hp_troll
                    range max_hp_troll
                    xsize 180
                    ysize 14
                    left_bar "#cc0000"
                    right_bar "#333333"
                text "[hp_troll]/[max_hp_troll]" color "#ffffff" size 16


# ---------- ЗАГЛУШКА ДЛЯ СТАРОГО ЭКРАНА ----------
# Этот экран был частью старой версии мини-игры "крестики-нолики".
# Сейчас игра использует другой экран (ttt_game_screen) из tic_tac_toe_logic.rpy.
# Заглушка оставлена, чтобы избежать ошибок, если где-то ещё есть ссылка на него.
screen tic_tac_toe_round_screen():
    pass


# ---------- СТИЛИ ----------
# Стили для кнопок и текста в кастомных экранах.
# Они определяют внешний вид элементов QTE и HUD.

# Стили кнопок меню выбора (используются в qte_choice и dodge_choice).
style menu_choice_button is choice_button
style menu_choice is choice_button_text

# Стиль текста для кнопки закрытия (не используется, но определён).
style tic_close_button_text:
    color "#ffffff"
    hover_color "#ffcc00"
    size 26
    text_align 0.5

# Стиль кнопок QTE (полупрозрачный фон, размер, отступы).
style qte_choice_button:
    background "#1a1a1a80"
    hover_background "#2a2a2a80"
    xsize 700
    xalign 0.5
    padding (10, 10)

# Стиль текста на кнопках QTE (цвет, размер, выравнивание).
style qte_menu_choice:
    color "#ffffff"
    hover_color "#0066cc"
    size 34
    xalign 0.5
    text_align 0.5

# Стиль для кнопки уклонения (старый QTE) — без фона, с полупрозрачным текстом.
style dodge_btn:
    background None
    hover_background None
    xsize 150
    ysize 40

# Стиль текста для кнопки уклонения.
style dodge_btn_text:
    color "#ffffff44"
    hover_color "#0066cc"
    size 18
    xalign 0.5
    text_align 0.5