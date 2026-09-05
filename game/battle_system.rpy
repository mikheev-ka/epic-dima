# ============================================================
# БОЕВАЯ СИСТЕМА (ВСЕ БОЕВЫЕ ЦИКЛЫ) – С РАСШИРЕННЫМИ ДИАЛОГАМИ
# ============================================================
#
# Этот файл содержит все боевые механики игры:
# - одиночный бой с троллем (без Лиры),
# - совместный бой с троллем (с Лирой),
# - обработку результатов (победа, поражение, повторные попытки),
# - обыск тролля после победы на пути силы.
#
# Бой построен на пошаговой системе: игрок выбирает действие
# (атака или использование ключа), затем враг контратакует,
# и игрок уклоняется через QTE (Quick Time Event).
# Время на уклонение уменьшается с каждым раундом, усложняя бой.
#
# Используемые переменные (определены в variables.rpy):
# - hp_player, max_hp_player — здоровье игрока
# - hp_troll, max_hp_troll — здоровье врага (тролля)
# - player_damage — урон игрока (зависит от характеристик)
# - troll_damage — урон врага (зависит от характеристик)
# - key_used — был ли использован ключ (одноразово)
# - lira_joined_battle — помогала ли Лира в бою
# - battle_round — номер раунда (для динамических фраз и QTE)
# - retry_count — счётчик повторных попыток при поражении
# - enemy_name — имя врага (для отображения в HUD)
#
# Также используются списки фраз для тролля, Лиры и игрока,
# определённые в init python ниже.
# ============================================================


# ---------- ИНИЦИАЛИЗАЦИЯ СПИСКОВ ФРАЗ (Python) ----------
# Здесь определяются списки строк для диалогов персонажей в бою.
# Каждый список содержит несколько вариантов, чтобы реплики
# были разнообразнее и не повторялись.
# Фразы разбиты по этапам боя (начало, середина, конец, победа, поражение).
init python:
    # Фразы тролля в разные моменты боя
    troll_phrases_start = [
        "Ты пахнешь страхом, человек!",
        "Ха! Смешной человечек!",
        "Твоя плоть будет сладкой!",
        "Я сломаю тебя, как ветку!"
    ]
    troll_phrases_mid = [
        "Ты сильнее, чем я думал... но это тебя не спасёт!",
        "Моя очередь!",
        "Ты только разозлил меня!",
        "Сейчас я раздавлю тебя!"
    ]
    troll_phrases_low = [
        "Ты... ты ранил Тролля! Ты заплатишь за это!",
        "Я убью тебя медленно!",
        "Так нечестно!",
        "Ты будешь страдать!"
    ]
    troll_phrases_victory = [
        "Ха-ха! Ты сдох!",
        "Ещё один труп!",
        "Тролль всегда побеждает!",
        "Плоть человека – лучшая еда!"
    ]
    troll_phrases_defeat = [
        "Нет... как я мог...",
        "Ты победил... но это не конец...",
        "Тролль повержен...",
        "Я умираю... но ты тоже сгниёшь здесь..."
    ]
    # Фразы Лиры (используются в совместном бою)
    lira_phrases_start = [
        "Я прикрою тебя, Дима!",
        "Давай, покажем этому уродцу!",
        "Вместе мы сила!",
        "Не бойся, я рядом!"
    ]
    lira_phrases_mid = [
        "Мы его изматываем!",
        "Так держать!",
        "Он уже дышит тяжело!",
        "Ещё немного!"
    ]
    lira_phrases_low_hp_player = [
        "Дима, ты ранен! Держись!",
        "Я не дам тебе умереть!",
        "Пожалуйста, не сдавайся!",
        "Мы справимся, я верю!"
    ]
    lira_phrases_help = [
        "Получай, тварь!",
        "Это тебе за Диму!",
        "Умри, урод!",
        "Я тебя не боюсь!"
    ]
    lira_phrases_victory = [
        "Мы сделали это!",
        "Я знала, что мы победим!",
        "Тролль повержен! Ура!",
        "Дима, ты гений!"
    ]
    # Фразы игрока (разные действия)
    player_phrases_attack = [
        "Получай!",
        "Сдохни!",
        "Это тебе за Лиру!",
        "Я не сдамся!",
        "Хватит прятаться!"
    ]
    player_phrases_dodge = [
        "Мимо!",
        "Не так быстро!",
        "Попробуй ещё раз!",
        "Слишком медленно!"
    ]
    player_phrases_get_hit = [
        "Ах, чёрт!",
        "Больно... но я ещё жив!",
        "Ты сильнее, чем я думал...",
        "Ничего, я отомщу!"
    ]
    player_phrases_key = [
        "Вот это да!",
        "Ключ работает!",
        "Ослепляющий свет!",
        "Это тебя отрезвит!"
    ]


# ---------- БОЙ С ТРОЛЛЕМ (ОДИНОЧНЫЙ) ----------
# Эта метка вызывается из веток path_strength или path_fear,
# когда игрок сражается один (без Лиры).
# Она инициализирует бой: показывает спрайты, HUD, запускает цикл.
label battle_loop:
    show gg battle at left_battle
    show troll troll_normal at right_battle
    show screen battle_hud          # Отображаем интерфейс боя (здоровье)
    $ battle_round = 0              # Сбрасываем счётчик раундов
    # Первая реплика тролля (случайная из начала)
    $ t_phrase = renpy.random.choice(troll_phrases_start)
    troll "[t_phrase]"
    jump battle_loop_core           # Переход в основной цикл боя


# ---------- ОСНОВНОЙ ЦИКЛ БОЯ (ОДИНОЧНЫЙ) ----------
# Здесь происходит каждый раунд: проверка состояния, выбор игрока,
# атака, ход врага, QTE.
label battle_loop_core:
    $ battle_round += 1             # Увеличиваем номер раунда

    # Проверка, не умер ли игрок или враг (после предыдущих действий)
    if hp_player <= 0:
        hide screen battle_hud
        jump battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win

    # Динамические фразы тролля в зависимости от его HP
    # (чтобы бой был более живым)
    if hp_troll > 70:
        if renpy.random.randint(1, 3) == 1:
            $ t_phrase = renpy.random.choice(troll_phrases_start)
            troll "[t_phrase]"
    elif hp_troll > 30:
        if renpy.random.randint(1, 2) == 1:
            $ t_phrase = renpy.random.choice(troll_phrases_mid)
            troll "[t_phrase]"
    else:
        if renpy.random.randint(1, 2) == 1:
            $ t_phrase = renpy.random.choice(troll_phrases_low)
            troll "[t_phrase]"
            # Показываем спрайт получения урона для драматичности
            show troll troll_hit at right_battle
            pause 0.3
            show troll troll_normal at right_battle

    # Меню выбора действия игрока
    "Твой ход. Что будешь делать?"
    menu:
        "⚔ Атаковать":
            jump battle_attack_core
        "🔑 Использовать ключ" if has_key and not key_used:
            jump battle_key_core


# ---------- АТАКА ИГРОКА (ОДИНОЧНЫЙ) ----------
# Игрок наносит урон, равный player_damage + случайное число (0-3).
# После атаки проверяется, не убит ли враг, иначе переход к ходу тролля.
label battle_attack_core:
    show gg fight2 at left_battle
    $ damage = player_damage + renpy.random.randint(0, 3)
    $ hp_troll -= damage

    # Реплика игрока при атаке
    $ p_phrase = renpy.random.choice(player_phrases_attack)
    gg "[p_phrase]"
    "Ты наносишь [damage] урона. (Тролль: [hp_troll] HP)"
    # Анимация получения урона троллем
    show troll troll_hit at right_battle
    pause 0.5
    show troll troll_normal at right_battle
    show gg battle at left_battle

    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win

    jump battle_troll_turn_core   # Переход к ходу тролля


# ---------- ИСПОЛЬЗОВАНИЕ КЛЮЧА (ОДИНОЧНЫЙ) ----------
# Если у игрока есть ключ и он ещё не использован,
# можно применить его в бою. Ключ наносит тройной урон,
# но используется только один раз за бой.
# Также добавляется эффект вспышки и диалог.
label battle_key_core:
    with flash                      # Эффект вспышки
    $ key_used = True               # Отмечаем, что ключ использован
    $ hp_troll -= player_damage * 3

    $ k_phrase = renpy.random.choice(player_phrases_key)
    gg "[k_phrase]"
    "Ключ вспыхивает ослепительным светом! Тролль в ужасе отшатывается!"
    show gg fight at left_battle
    show troll troll_hit at right_battle
    pause 0.5
    # После вспышки продолжаем музыку боя
    play music music_battle loop
    show gg battle at left_battle
    show troll troll_normal at right_battle

    "Тройной урон! [player_damage*3] урона. (Тролль: [hp_troll] HP)"

    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win

    jump battle_troll_turn_core


# ---------- ХОД ТРОЛЛЯ (ОДИНОЧНЫЙ) ----------
# Тролль атакует, игрок должен увернуться через QTE.
# Время на QTE уменьшается с каждым раундом (усложняется),
# но не меньше 0.7 секунды.
# При успехе игрок не получает урона, при неудаче — получает troll_damage.
label battle_troll_turn_core:
    $ battle_round += 1

    if hp_player <= 0:
        hide screen battle_hud
        jump battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win

    # Расчёт времени QTE: чем больше раундов, тем меньше времени.
    # Минимум 0.7 секунды.
    $ qte_time = max(0.7, 1.5 - (battle_round - 1) * 0.08)

    # Вызов экрана QTE (custom_screens.rpy), который возвращает "success" или "fail"
    call screen dodge_choice(time=qte_time, round=battle_round)
    $ result = _return

    if result == "success":
        $ p_phrase = renpy.random.choice(player_phrases_dodge)
        gg "[p_phrase]"
        "Ты успешно уклоняешься от удара тролля!"
        show gg dodge at left_battle
        pause 0.8
        show gg battle at left_battle
    else:
        $ hp_player -= troll_damage
        $ p_phrase = renpy.random.choice(player_phrases_get_hit)
        gg "[p_phrase]"
        "Тролль бьёт с силой [troll_damage]! (Ты: [hp_player] HP)"
        show gg impact3 as gg at left_battle
        pause 0.8
        show gg battle at left_battle

    if hp_player <= 0:
        hide screen battle_hud
        jump battle_lose

    jump battle_loop_core   # Возвращаемся в начало цикла


# ---------- БОЙ С ТРОЛЛЕМ (С ЛИРОЙ) ----------
# Эта метка вызывается из ветки path_friendship, когда Лира помогает.
# Отличается наличием реплик Лиры, её помощи и немного другими параметрами.
label battle_loop_with_lira:
    $ qte_time = 1.5
    # Первая реплика Лиры
    $ l_phrase = renpy.random.choice(lira_phrases_start)
    lira "[l_phrase]"
    if girl_affinity >= 3:
        lira "Я буду следить за его движениями!"

    show gg battle at left_battle
    show troll troll_normal at right_battle
    show screen battle_hud
    $ battle_round = 0

    jump battle_loop_core_lira


# ---------- ОСНОВНОЙ ЦИКЛ БОЯ (С ЛИРОЙ) ----------
# Аналогичен одиночному, но с дополнительными репликами Лиры
# и возможностью её вмешательства при низком здоровье игрока.
label battle_loop_core_lira:
    $ battle_round += 1

    if hp_player <= 0:
        hide screen battle_hud
        jump battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win_friendship

    # РЕПЛИКИ ТРОЛЛЯ (аналогично одиночному)
    if hp_troll > 70:
        if renpy.random.randint(1, 2) == 1:
            $ t_phrase = renpy.random.choice(troll_phrases_start)
            troll "[t_phrase]"
    elif hp_troll > 30:
        if renpy.random.randint(1, 2) == 1:
            $ t_phrase = renpy.random.choice(troll_phrases_mid)
            troll "[t_phrase]"
    else:
        if renpy.random.randint(1, 2) == 1:
            $ t_phrase = renpy.random.choice(troll_phrases_low)
            troll "[t_phrase]"

    # РЕПЛИКИ ЛИРЫ (в зависимости от HP тролля)
    if hp_troll > 70:
        if renpy.random.randint(1, 3) == 1:
            $ l_phrase = renpy.random.choice(lira_phrases_start)
            lira "[l_phrase]"
    elif hp_troll > 30:
        if renpy.random.randint(1, 2) == 1:
            $ l_phrase = renpy.random.choice(lira_phrases_mid)
            lira "[l_phrase]"
    else:
        if renpy.random.randint(1, 2) == 1:
            lira "Он почти повержен! Давай, добей его!"

    # Лира помогает при опасности (если HP игрока ≤ 20 и она ещё не помогала)
    if hp_player <= 20 and not lira_joined_battle:
        $ lira_joined_battle = True
        show lira angry at center_pos
        with dissolve
        "Лира видит, что ты слабеешь, и бросается вперёд!"
        $ hp_troll -= 20
        $ l_phrase = renpy.random.choice(lira_phrases_help)
        lira "[l_phrase]"
        hide lira angry
        with dissolve

    "Твой ход. Что будешь делать?"
    menu:
        "⚔ Атаковать":
            jump battle_attack_lira_core
        "🔑 Использовать ключ" if has_key and not key_used:
            jump battle_key_lira_core


# ---------- АТАКА ИГРОКА (С ЛИРОЙ) ----------
# Аналогично одиночной атаке, но после атаки переход к ходу тролля с Лирой.
label battle_attack_lira_core:
    show gg fight2 at left_battle
    $ damage = player_damage + renpy.random.randint(0, 3)
    $ hp_troll -= damage
    $ p_phrase = renpy.random.choice(player_phrases_attack)
    gg "[p_phrase]"
    "Ты наносишь [damage] урона! (Тролль: [hp_troll] HP)"
    show troll troll_hit at right_battle
    pause 0.5
    show troll troll_normal at right_battle
    show gg battle at left_battle

    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win_friendship

    jump battle_troll_lira_core


# ---------- ИСПОЛЬЗОВАНИЕ КЛЮЧА (С ЛИРОЙ) ----------
# Ключ работает так же, но Лира комментирует это событие.
label battle_key_lira_core:
    with flash
    $ key_used = True
    $ hp_troll -= player_damage * 3

    show lira smile at center_pos
    with dissolve
    $ k_phrase = renpy.random.choice(player_phrases_key)
    gg "[k_phrase]"
    "Ключ взрывается светом! Лира в восторге кричит: 'Что это было?!'"
    show gg fight at left_battle
    show troll troll_hit at right_battle
    pause 0.5
    play music music_battle loop
    show gg battle at left_battle
    show troll troll_normal at right_battle
    hide lira smile
    with dissolve

    "Тройной урон! [player_damage*3] урона. (Тролль: [hp_troll] HP)"

    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win_friendship

    jump battle_troll_lira_core


# ---------- ХОД ТРОЛЛЯ (С ЛИРОЙ) ----------
# Аналогичен одиночному ходу, но с чуть большим временем на QTE
# (чтобы компенсировать сложность совместного боя).
label battle_troll_lira_core:
    $ battle_round += 1

    if hp_player <= 0:
        hide screen battle_hud
        jump battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump battle_win_friendship

    # Время QTE для боя с Лирой – чуть больше, но тоже уменьшается
    $ qte_time = max(0.8, 1.8 - (battle_round - 1) * 0.07)

    call screen dodge_choice(time=qte_time, round=battle_round)
    $ result = _return

    if result == "success":
        $ p_phrase = renpy.random.choice(player_phrases_dodge)
        gg "[p_phrase]"
        "Ты уклоняешься от удара тролля!"
        show gg dodge at left_battle
        pause 0.8
        show gg battle at left_battle
    else:
        $ hp_player -= troll_damage
        $ p_phrase = renpy.random.choice(player_phrases_get_hit)
        gg "[p_phrase]"
        "Тролль бьёт с силой [troll_damage]! (Ты: [hp_player] HP)"
        show gg impact3 as gg at left_battle
        pause 0.8
        show gg battle at left_battle

    if hp_player <= 0:
        hide screen battle_hud
        jump battle_lose

    jump battle_loop_core_lira


# ---------- РЕЗУЛЬТАТЫ БОЯ ----------

# ---------- ПОБЕДА В ОДИНОЧНОМ БОЮ ----------
# Игрок победил тролля. Проигрывается фраза поражения тролля,
# устанавливаются флаги победы, показывается анимация падения.
# Затем в зависимости от выбранного пути (current_path)
# либо обыск тролля (если путь силы), либо прямой побег.
label battle_win:
    stop music
    play music music_zvuk loop
    $ t_phrase = renpy.random.choice(troll_phrases_defeat)
    troll "[t_phrase]"
    "Тролль падает. Земля содрогается от его веса. Я стою, опираясь на железо, и чувствую, как дыхание возвращается."
    $ troll_defeated = True
    $ escape_success = True
    hide screen battle_hud
    # Анимация падения тролля (несколько спрайтов)
    show troll troll_fall1 at right_battle
    pause 0.8
    show troll troll_fall2 at right_battle
    pause 0.8
    show gg angry at left_battle
    pause 1.0

    "Победа. Но цена её — моя кровь на полу. Я смотрю на поверженное чудовище и не чувствую радости."

    if current_path == "strength":
        jump search_troll
    else:
        jump escape_alone


# ---------- ПОБЕДА В БОЮ С ЛИРОЙ ----------
# Аналогично одиночной победе, но с добавлением реплик Лиры
# и переходом к совместному выходу (exit_choice_together).
label battle_win_friendship:
    stop music
    play music music_zvuk loop
    $ t_phrase = renpy.random.choice(troll_phrases_defeat)
    troll "[t_phrase]"
    $ l_phrase = renpy.random.choice(lira_phrases_victory)
    lira "[l_phrase]"
    "Тролль повержен. Мы стоим рядом, тяжело дыша. Лира улыбается, и в её глазах мелькает надежда."
    $ troll_defeated = True
    $ escape_success = True
    $ girl_ally = True
    hide screen battle_hud
    # Анимация падения тролля
    show troll troll_fall1 at right_battle
    pause 0.8
    show troll troll_fall2 at right_battle
    pause 0.8
    scene bg dungeon_girl with fade
    show gg angry at left_battle
    show lira stand at right_battle
    pause 1.0

    lira "Мы сделали это! Я думала, умрём."
    gg "Вместе сильнее. Пошли."
    jump exit_choice_together


# ---------- ПОРАЖЕНИЕ В БОЮ ----------
# Игрок проиграл (HP ≤ 0). Проигрывается фраза победы тролля,
# показывается анимация падения игрока.
# Если есть попытки (retry_count < 2), предлагается ретрай,
# иначе — переход к плохой концовке.
label battle_lose:
    stop music
    play music music_bad_ending loop
    hide screen battle_hud
    $ t_phrase = renpy.random.choice(troll_phrases_victory)
    troll "[t_phrase]"
    "Мир меркнет. Я падаю без сил. Противник нависает..."
    # Анимация падения игрока
    show gg fall1 at left_battle
    pause 0.8
    show gg fall2 at left_battle
    pause 0.8
    show gg fall3 at left_battle
    pause 0.8
    show gg fall4 at left_battle
    pause 0.8
    show troll troll_victory at right_battle
    pause 1.0

    if retry_count < 2:
        menu:
            "Попробовать ещё раз? (Осталось [2-retry_count] попыток)":
                jump retry_battle
            "Принять поражение.":
                jump bad_end
    else:
        "Ты использовал все шансы. Поражение окончательно."
        jump bad_end


# ---------- ПОВТОРНАЯ ПОПЫТКА БОЯ ----------
# При ретрае здоровье игрока восстанавливается до 25,
# здоровье тролля до 40, сбрасывается счётчик раундов,
# и бой начинается заново (с начала battle_loop).
label retry_battle:
    $ retry_count += 1
    play music music_battle loop
    "Встаёшь. Бой продолжается! Ты чувствуешь, что силы на исходе, но не можешь сдаться."
    $ hp_player = 25
    $ hp_troll = 40
    $ battle_round = 0
    jump battle_loop


# ---------- ОБЫСК ТРОЛЛЯ (ПУТЬ СИЛЫ) ----------
# Эта метка вызывается после победы над троллем, если игрок выбрал
# путь силы (path_strength). Игрок обыскивает тролля и находит
# три металлических фрагмента, из которых собирается ключ.
# Затем он может либо освободить Лиру, либо уйти одному.
label search_troll:
    scene bg dungeon_cell_real with fade
    show gg smoking at center_pos
    "Подхожу к поверженному троллю. Он пахнет смертью и гнилью. Обыскиваю его — три металлических фрагмента. Складываются в ключ с символом."
    "Он открывает клетки. Я слышу, как скрипят замки."
    "Смотрю на камеру Лиры. Она прижимается к решётке."

    menu:
        "Что делать?"
        "Освободить Лиру.":
            $ has_key = True
            $ girl_affinity += 1
            "Открываю клетку."
            show lira smile at right_pos
            lira "Ты... ты освободил меня! Я думала, сгнию."
            gg "Тролль мёртв. Идём."
            lira "Спасибо. Я не забуду."
            show lira happy at right_pos
            $ girl_ally = True
            jump exit_choice_together
        "Уйти одному.":
            $ bravery += 1
            "Бросаю ключ и ухожу."
            show lira scream at right_pos
            lira "Нет! Пожалуйста!"
            "Не оборачиваюсь. Слышу её плач. Выбираю одиночество."
            jump escape_alone