# ============================================================
# УЧАСТОК ШЕРИФА (ОДИНОЧНЫЙ И С ЛИРОЙ) – ПОЛНАЯ ВЕРСИЯ
# ============================================================
#
# Этот файл содержит сцены, связанные с посещением участка шерифа
# как в одиночку, так и вместе с Лирой. Здесь происходит:
# - допрос у шерифа (который в итоге оказывается Кириллом)
# - исследование архива с находками (фото, газетные вырезки)
# - раскрытие личности шерифа и его истинных целей
# - выбор: присоединиться к Кириллу, сражаться с ним или
#   (в случае совместного прохождения) принять участие в групповом сексе
# - боевая система с двумя фазами (обычная и усиленная форма Кирилла)
# - несколько концовок: победа, поражение с ретри, сердечный приступ,
#   жертва Лиры и другие.
#
# Механика боя аналогична бою с троллем, но с адаптацией под Кирилла:
# - фаза 1: обычный Кирилл (80 HP), фаза 2: усиленный (160 HP)
# - QTE-уклонения с уменьшающимся временем
# - возможность использовать ключ (если он есть) для нанесения тройного урона
# - в совместном бою Лира может помогать, если её привязанность достаточна
# - при поражении есть возможность ретрая (до 2 раз)
# ============================================================


# ---------- ИНИЦИАЛИЗАЦИЯ СПИСКОВ ФРАЗ (Python) ----------
# В этом блоке определяются реплики для различных ситуаций в бою с Кириллом
# и для диалогов. Каждый список содержит несколько вариантов, чтобы
# диалоги были разнообразнее и не повторялись.
init python:
    # Фразы Кирилла в начале боя (одиночный режим)
    kirill_phrases_start = [
        "Ну что, Димон, готов получить по зубам?",
        "Я всегда знал, что мы встретимся в бою.",
        "Ты думал, я просто коллега? Ха!",
        "Сейчас я покажу тебе, что такое настоящая сила!"
    ]
    # Фразы Кирилла в середине боя (когда HP ~60-80%)
    kirill_phrases_mid = [
        "Неплохо... но ты всё равно проиграешь!",
        "Ты сильнее, чем я думал, но этого мало!",
        "Моя очередь, дружище!",
        "Сейчас я тебя прикончу!"
    ]
    # Фразы Кирилла, когда его HP низкий (<25%)
    kirill_phrases_low = [
        "Ты... ты меня достал!",
        "Я не сдамся, даже если умру!",
        "Получай, гад!",
        "Ты заплатишь за каждую царапину!"
    ]
    # Фразы Кирилла при его поражении
    kirill_phrases_defeat = [
        "Нет... я проиграл...",
        "Ты победил... но это не конец...",
        "Как я мог проиграть такому...",
        "Ладно... ты сильнее..."
    ]
    # Фразы Кирилла при победе над игроком
    kirill_phrases_victory = [
        "Ха-ха! Сдох!",
        "Так тебе и надо, Димон!",
        "Я всегда выигрываю!",
        "Попробуй ещё раз, если жить надоело!"
    ]
    # Фразы Кирилла в совместном бою (с Лирой) – начало
    kirill_phrases_start_lira = [
        "О, ещё и девушка с тобой. Романтично.",
        "Лира, да? Мне рассказывали о тебе.",
        "Двое против одного? Нечестно... но мне нравится!",
        "Вы думаете, что сможете победить меня вдвоём?"
    ]
    # Фразы Кирилла в совместном бою – середина
    kirill_phrases_mid_lira = [
        "Вы неплохи, но этого недостаточно!",
        "Сейчас я раздавлю вас обоих!",
        "Ваша команда слаба!",
        "Моя очередь!"
    ]
    # Фразы Кирилла в совместном бою – низкий HP
    kirill_phrases_low_lira = [
        "Вы... вы меня достали!",
        "Я не сдамся!",
        "Получайте!",
        "Вы заплатите за всё!"
    ]
    # Фразы игрока для боя с Кириллом (атака, уклонение, получение урона, использование ключа)
    player_phrases_attack_kirill = [
        "Держи удар!",
        "Получай, Кирилл!",
        "Я не боюсь тебя!",
        "Это за все твои шутки!"
    ]
    player_phrases_dodge_kirill = [
        "Мимо!",
        "Слишком медленно!",
        "Попробуй ещё раз!",
        "Не догонишь!"
    ]
    player_phrases_get_hit_kirill = [
        "Ах, чёрт!",
        "Больно... но я не сдамся!",
        "Ты силён... но я сильнее!",
        "Ничего, я отомщу!"
    ]
    player_phrases_key_kirill = [
        "Смотри, что у меня есть!",
        "Ослепительный свет!",
        "Ключ работает!",
        "Это тебя отрезвит!"
    ]


# ---------- УЧАСТОК ШЕРИФА (ОДИНОЧНЫЙ) ----------
# Метка вызывается, когда игрок идёт в участок один (без Лиры).
# Здесь происходит допрос, после чего шериф отправляет Диму в архив,
# где тот находит улики, и в итоге раскрывается личность шерифа – Кирилл.
label police_route_alone:
    stop music
    play music music_police loop          # Запускаем фоновую музыку участка
    scene bg police with fade             # Показываем фон участка

    "Участок выглядит как любое захолустное отделение: пыльный, с тусклым светом и запахом дешёвого кофе. Единственное окно выходит на пустынную улицу, и я вижу, как ветер гонит пыль по асфальту."

    "За столом сидит шериф. Лысеющий, с мешками под глазами. Он похож на человека, который видел слишком много и перестал удивляться."

    show gg tired at left_pos
    show sheriff at right_pos

    sheriff "Проходи, садись. Рассказывай."

    "Я сажусь напротив. Стул скрипит. Тишина – тяжёлая, как его взгляд."

    # Первый выбор: как начать разговор – влияет на характеристики.
    menu:
        "Рассказать правду.":
            $ intellect += 1
            jump police_detailed_start
        "Сказать, что ничего не помню.":
            $ bravery += 1
            jump police_amnesia_start
        "Спросить, зачем я здесь.":
            $ lust += 1
            jump police_defensive_start


# Далее идут несколько меток, соответствующих разным вариантам ответов на допросе.
# Каждая метка ведёт к дальнейшим вопросам и выборам, а затем к общей ветке
# police_alone_after_troll, где шериф отправляет Диму в архив.

# police_detailed_start – игрок рассказывает правду о темнице и тролле.
label police_detailed_start:
    gg "Я очнулся в темнице. Не знаю, как туда попал. Думал, это сон – но камень был настоящим."
    sheriff "Темница. Где?"
    gg "Под землёй. Старый храм или что-то вроде. Там был тролль."
    sheriff "Тролль? Ты серьёзно?"
    gg "Я тоже думал, что это бред. Но он был реален. Я дрался с ним. Победил."
    sheriff "И как ты его победил?"
    # Вложенное меню: способ победы над троллем
    menu:
        "С помощью ключа.":
            $ intellect += 1
            jump police_key_method
        "Сила.":
            $ bravery += 1
            jump police_force_method
        "Мне помогли.":
            $ lust += 1
            jump police_help_method

# police_amnesia_start – игрок говорит, что ничего не помнит.
label police_amnesia_start:
    gg "Я не помню. Всё как в тумане. Может, меня ударили по голове."
    sheriff "Хорошо. Тогда скажи, что ты помнишь последнее, прежде чем оказаться здесь?"
    gg "Работу. Дождь. Посылку."
    sheriff "Какую посылку?"
    gg "Коробку без маркировки. Внутри был ключ."
    sheriff "Ключ? Ты его взял?"
    menu:
        "Взял.":
            $ lust += 1
            jump police_key_taken
        "Выбросил.":
            $ bravery += 1
            jump police_key_thrown
        "Не помню.":
            $ intellect += 1
            jump police_key_forgotten

# police_defensive_start – игрок защищается, не даёт прямых ответов.
label police_defensive_start:
    gg "Я не знаю, что я здесь делаю. Я просто искал выход."
    sheriff "Выход из чего?"
    gg "Из всей этой ерунды. Из темницы, из дождя – не важно."
    sheriff "Ты выглядишь как человек, который что-то ищет. Может быть, ты ищешь себя?"
    gg "Может быть. Но я не думал, что найду себя в участке."
    sheriff "Ты здесь, чтобы ответить на вопросы. Скажи, ты кого-нибудь там видел?"
    gg "Тролля. И..."
    sheriff "И?"
    menu:
        "Никого.":
            $ bravery += 1
            jump police_alone_lira_not_mention
        "Девушку.":
            $ lust += 1
            jump police_alone_lira_mention
        "Я не уверен, что это было на самом деле.":
            $ intellect += 1
            jump police_alone_doubt


# Метки для каждого варианта из police_detailed_start:
label police_key_method:
    gg "У меня был ключ. Он открывал клетки. Я использовал его как оружие – он вспыхнул и ослепил тролля."
    sheriff "Ключ. Символ на нём был?"
    gg "Да. Круг с перекрестьем."
    sheriff "Этот символ мне знаком. Он связан с культом. Ты понимаешь, что это значит?"
    gg "Нет. Но я хочу понять."
    sheriff "Тогда скажи мне, ты был один?"
    gg "Да. Один."
    sheriff "Ты уверен? Иногда наш разум вытесняет тех, кого мы не смогли спасти."
    "Эти слова бьют как пощёчина. Я сглатываю."
    gg "Я не хочу об этом говорить."
    sheriff "Хорошо. Тогда перейдём к другому. Что было дальше?"
    jump police_alone_after_troll

label police_force_method:
    gg "Я просто дрался. Я служил в армии. Химвойска. Я знаю, как убивать."
    sheriff "Тролль – не человек. Ты не мог его просто перебить кулаками."
    gg "Я нашёл железо. Кусок арматуры. Всё, что было под рукой."
    sheriff "Ты голыми руками и куском железа убил тролля?"
    gg "Да."
    sheriff "Ты либо очень сильный, либо очень отчаянный. Что тебя толкнуло на это?"
    menu:
        "Страх.":
            $ bravery += 1
            jump police_alone_after_troll
        "Я хотел выбраться.":
            $ intellect += 1
            jump police_alone_after_troll
        "Я не знаю.":
            $ lust += 1
            jump police_alone_after_troll

label police_help_method:
    gg "Мне помогала девушка."
    sheriff "Девушка? Она тоже была в темнице?"
    gg "Да. Она сидела в соседней камере."
    sheriff "И где она сейчас?"
    "Вопрос застревает в горле. Я не знаю, как ответить."
    gg "Я... я не знаю."
    sheriff "Ты оставил её там?"
    menu:
        "Я вернулся за ней, но было поздно.":
            $ bravery += 1
            jump police_alone_after_troll
        "Я не мог её спасти.":
            $ lust += 1
            jump police_alone_after_troll
        "Я её освободил.":
            $ intellect += 1
            jump police_alone_after_troll


# Метки для вариантов из police_amnesia_start:
label police_key_taken:
    gg "Взял. Это был единственный шанс."
    sheriff "И что ты сделал с ним?"
    gg "Использовал. Он открыл клетки. Помог мне выжить."
    sheriff "Ты говоришь о нём так, будто он живой."
    gg "Он был тёплым. Настоящим."
    sheriff "Тепло. Это символ жизни. Или смерти. Смотря кто его держит."
    jump police_alone_after_troll

label police_key_thrown:
    gg "Я выбросил его. Я не знал, что это за вещь."
    sheriff "И ты уверен, что не вернулся за ним?"
    gg "Нет. Я не хотел иметь с ним ничего общего."
    sheriff "Ты не хотел. Но он хотел тебя. Эти вещи сами находят своих хозяев."
    gg "Вы говорите как мой друг. Тоже любит философствовать."
    sheriff "Какой друг?"
    gg "Кирилл."
    "Шериф застывает. На секунду мне кажется, что я увидел в его глазах узнавание. Но он быстро взял себя в руки."
    sheriff "Кирилл, говоришь?"
    jump police_alone_after_troll

label police_key_forgotten:
    gg "Я не помню. Всё смешалось."
    sheriff "Ты уже сказал про коробку. Значит, ты помнишь больше, чем хочешь показать."
    gg "Я просто хочу забыть."
    sheriff "Забыть – это роскошь. Её нужно заслужить."
    jump police_alone_after_troll


# Метки для вариантов из police_defensive_start:
label police_alone_lira_not_mention:
    gg "Никого. Только тролль."
    sheriff "Только тролль. И ты его убил."
    gg "Да."
    sheriff "Один человек против тролля. Без оружия. Ты хочешь сказать, что ты – герой?"
    gg "Нет. Я просто хотел выжить."
    sheriff "Тогда почему я чувствую, что ты что-то скрываешь?"
    menu:
        "Потому что я не доверяю полиции.":
            $ bravery += 1
            jump police_alone_after_troll
        "Потому что тебе кажется.":
            $ intellect += 1
            jump police_alone_after_troll
        "Я ничего не скрываю.":
            $ lust += 1
            jump police_alone_after_troll

label police_alone_lira_mention:
    gg "Девушку. Она была в соседней камере."
    sheriff "И что с ней?"
    gg "Я пытался спасти её. Но не смог."
    sheriff "Ты оставил её?"
    gg "У меня не было выбора."
    sheriff "Выбор всегда есть. Просто не все готовы его принять."
    gg "Я знаю. Я принимаю это каждый день."
    sheriff "Что ты чувствуешь?"
    menu:
        "Вина.":
            $ bravery += 1
            jump police_alone_after_troll
        "Пустота.":
            $ intellect += 1
            jump police_alone_after_troll
        "Я не хочу говорить о чувствах.":
            $ lust += 1
            jump police_alone_after_troll

label police_alone_doubt:
    gg "Я не уверен. Может быть, это была галлюцинация. Может быть, я всё ещё сплю."
    sheriff "Ты в участке, на стуле, разговариваешь с шерифом. Это не сон. Но я понимаю, о чём ты – иногда реальность страшнее любого сна."
    gg "Я не знаю, что реально. А что – нет."
    sheriff "Ты хочешь узнать?"
    menu:
        "Да.":
            $ intellect += 1
            jump police_alone_after_troll
        "Нет.":
            $ bravery += 1
            jump police_alone_after_troll
        "Я боюсь.":
            $ lust += 1
            jump police_alone_after_troll


# ===== НОВАЯ ВЕТКА: ПОРУЧЕНИЕ В АРХИВ =====
# После допроса шериф отправляет Диму в архив за синей папкой.
# Это ключевой момент: там Дима находит улики, которые раскрывают тайну.
label police_alone_after_troll:
    "Допрос продолжается. Шериф задаёт вопросы, но я чувствую, что он уже знает на них ответы. Он просто проверяет, буду ли я врать."

    sheriff "Теперь давай поговорим о том, что ты чувствуешь сейчас."
    gg "Я хочу домой."
    sheriff "Домой? Куда?"
    gg "В свою квартиру. К своей жизни."
    sheriff "Твоя жизнь там, где ты оставил её. Ты думаешь, она тебя ждёт?"
    menu:
        "Я надеюсь.":
            $ intellect += 1
            jump police_alone_send_to_archive
        "Я не знаю.":
            $ bravery += 1
            jump police_alone_send_to_archive
        "Мне всё равно.":
            $ lust += 1
            jump police_alone_send_to_archive


label police_alone_send_to_archive:
    sheriff "Слушай, Дима. Прежде чем мы продолжим, я хочу, чтобы ты кое-что посмотрел. В архиве на складе лежит старая папка с делом о пропавших людях. Мне нужна она, чтобы сверить твои слова. Принеси её — синяя обложка, на третьей полке."
    gg "Прямо сейчас?"
    sheriff "Да. Времени мало. Я пока займусь бумагами."
    "Я встаю и выхожу из кабинета. Шериф провожает меня взглядом, в котором мне чудится что-то странное."
    jump police_alone_archive


# ---------- АРХИВ (ОДИНОЧНЫЙ) ----------
# Здесь Дима находит папку с вырезками, фото Кирилла в форме шерифа,
# и страницу из дневника о ключе.
label police_alone_archive:
    scene bg police_archive with fade
    play music music_suspense loop        # Напряжённая музыка для атмосферы архива

    "Склад-архив находится в подвале. Сыро, пахнет плесенью и старой бумагой. Стеллажи до потолка, некоторые папки рассыпаны по полу."

    "Я нахожу третью полку. Синяя папка действительно там. Беру её, но она тяжёлая. Внутри — не только документы."

    # Пасхалки – находки, которые меняют понимание сюжета
    "Пролистываю её. Здесь газетные вырезки о пропажах людей в округе за последние пять лет. Все жертвы — молодые женщины."
    "Одна из них — блондинка с косой. Я замираю. Это Лира."

    "Дальше — старая фотография. На ней Кирилл в форме шерифа, но с чёрной бородой и в тех же очках. Сзади надпись: 'Советник К., 2018'."

    "И последнее — вырванная страница из дневника. Почерк неразборчив, но я разбираю: 'Ключ — это врата. Тот, кто владеет им, может открыть проход между мирами. Жрецы ищут его уже столетия...'"

    "Я перевожу дыхание. Это не просто архив — это ключ к тайне, в которую я попал."

    scene black with fade
    "Сую папку под мышку и возвращаюсь наверх."

    jump police_alone_return_from_archive


# ---------- ВОЗВРАЩЕНИЕ И РАСКРЫТИЕ (ОДИНОЧНЫЙ) ----------
# Шериф раскрывает себя как Кирилл, предлагает выбор.
label police_alone_return_from_archive:
    scene bg police with fade
    stop music
    play music music_dark loop

    "Я подхожу к двери кабинета. Шериф сидит за столом, просматривает бумаги. Он поднимает голову, когда я вхожу."

    show gg tired at left_pos
    show sheriff at right_pos

    sheriff "А, вернулся. Папку принёс? Отлично."
    gg "Я нашёл кое-что... странное. Фотографии, записи о пропажах. И фотография Кирилла в вашей форме. Кто вы на самом деле?"
    sheriff "Ты догадался. Я — Кирилл. Тот самый. Мы работали вместе, но ты даже не подозревал, что я — часть этого мира."
    gg "Что? Но зачем? Почему ты здесь?"
    kirill "Я искал ключ, Димон. И ты принёс его мне. Этот ключ открывает врата между мирами. Я хочу получить силу, чтобы править. Но я знаю, что ты не отдашь его просто так."
    gg "Ты предлагаешь мне выбор?"
    kirill "Да. Ты можешь присоединиться ко мне. Мы вместе откроем врата, и ты получишь власть. Но это потребует жертвы — ключ забирает жизненную энергию. Если ты слаб, ты умрёшь. Но если выживешь — станешь богом."

    menu:
        "Присоединиться к Кириллу.":
            jump police_alone_join_heart_attack
        "Драться с ним.":
            # Скрываем спрайты перед боем
            hide sheriff
            hide gg
            jump police_alone_battle


# ===== НОВАЯ МЕТКА: СМЕРТЬ ОТ ПРИСТУПА (ОДИНОЧНЫЙ) =====
# Если игрок соглашается на сделку, ключ забирает его жизненную энергию,
# и Дима умирает от сердечного приступа – плохая концовка.
label police_alone_join_heart_attack:
    stop music
    play music music_bad_ending loop

    gg "Я согласен. Я хочу силы."
    kirill "Отличный выбор, друг. Тогда давай начнём ритуал."
    "Кирилл подходит ко мне, кладёт руку на плечо. Я чувствую, как ключ в кармане нагревается. Вдруг резкая боль пронзает грудь."
    gg "Что...?"
    kirill "Ты слишком слаб, Димон. Твоё сердце не выдерживает. Прощай."
    "Я падаю на колени. В глазах темнеет. Последнее, что я вижу — ухмыляющееся лицо Кирилла."
    scene black with fade
    "Дима умер от сердечного приступа. Кирилл забирает ключ и уходит в мир теней."
    jump end_chapter


# ---------- ОДИНОЧНЫЙ БОЙ С КИРИЛЛОМ (МЕХАНИКА) ----------
# Начинается боевая последовательность. Используются те же переменные,
# что и в бою с троллем, но с другими значениями и с двумя фазами.
label police_alone_battle:
    $ retry_count = 0
    hide sheriff

    # ИНИЦИАЛИЗАЦИЯ ДЛЯ HUD (ФАЗА 1)
    $ max_hp_player = 50
    $ max_hp_troll = 80
    $ enemy_name = "Кирилл"

    $ phase_two = False
    $ hp_player = 50
    $ hp_troll = 80
    $ player_damage = 8 + (bravery // 3) + (intellect // 4)   # Урон зависит от храбрости и интеллекта
    $ troll_damage = 12 - (bravery // 4)                       # Урон Кирилла снижается с храбростью

    if has_key:
        $ player_damage += 3                                   # Бонус за ключ

    $ battle_round = 0
    $ key_used = False

    "Ты сражаешься с Кириллом. Он двигается быстро, его удары точны. Это не просто драка — это схватка с собственной тенью."

    play music music_battle loop
    jump police_alone_battle_loop_phase1


# ---------- ФАЗА 1: ОБЫЧНАЯ ФОРМА КИРИЛЛА ----------
# Цикл боя: игрок атакует или использует ключ, затем Кирилл контратакует
# (игрок уклоняется через QTE). После победы в фазе 1 следует трансформация.
label police_alone_battle_loop_phase1:
    show gg battle at left_battle
    show kirill at right_battle
    show screen battle_hud                  # Отображаем HUD (здоровье, раунд)
    $ battle_round += 1

    if hp_player <= 0:
        hide screen battle_hud
        jump police_alone_battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump police_alone_battle_phase1_win

    # Динамические фразы Кирилла в зависимости от его HP
    if hp_troll > 60:
        if renpy.random.randint(1, 3) == 1:
            $ k_phrase = renpy.random.choice(kirill_phrases_start)
            kirill "[k_phrase]"
    elif hp_troll > 25:
        if renpy.random.randint(1, 2) == 1:
            $ k_phrase = renpy.random.choice(kirill_phrases_mid)
            kirill "[k_phrase]"
    else:
        if renpy.random.randint(1, 2) == 1:
            $ k_phrase = renpy.random.choice(kirill_phrases_low)
            kirill "[k_phrase]"

    "Твой ход. Что будешь делать?"
    menu:
        "⚔ Атаковать":
            jump police_alone_battle_attack_phase1
        "🔑 Использовать ключ" if has_key and not key_used:
            jump police_alone_battle_key_phase1


# Атака игрока в фазе 1
label police_alone_battle_attack_phase1:
    show gg fight2 at left_battle
    $ damage = player_damage + renpy.random.randint(0, 3)   # Случайный бонус
    $ hp_troll -= damage

    $ p_phrase = renpy.random.choice(player_phrases_attack_kirill)
    gg "[p_phrase]"
    "Наносишь [damage] урона. Кирилл пошатнулся. (Кирилл: [hp_troll] HP)"
    show kirill at right_battle
    pause 0.5
    show kirill at right_battle
    show gg battle at left_battle

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_alone_battle_phase1_win

    jump police_alone_battle_kirill_turn_phase1


# Использование ключа в фазе 1 – наносит тройной урон, но только один раз.
label police_alone_battle_key_phase1:
    stop music
    # play sound key  # Убрано по требованию (звук закомментирован)
    with flash                               # Эффект вспышки
    $ key_used = True
    $ hp_troll -= player_damage * 3

    $ k_phrase = renpy.random.choice(player_phrases_key_kirill)
    gg "[k_phrase]"
    "Ключ вспыхивает в твоей руке. Кирилл щурится, отшатываясь от света."
    show gg fight at left_battle
    show kirill at right_battle
    pause 0.5
    play music music_battle loop
    show gg battle at left_battle
    show kirill at right_battle

    "Ты наносишь [player_damage*3] урона! (Кирилл: [hp_troll] HP)"

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_alone_battle_phase1_win

    jump police_alone_battle_kirill_turn_phase1


# Ход Кирилла – игрок уклоняется через QTE
label police_alone_battle_kirill_turn_phase1:
    # Время на уклонение уменьшается с каждым раундом (но не менее 0.7 сек)
    $ qte_time = max(0.7, 1.5 - (battle_round - 1) * 0.08)

    call screen dodge_choice(time=qte_time, round=battle_round)
    $ result = _return

    if result == "success":
        $ p_phrase = renpy.random.choice(player_phrases_dodge_kirill)
        gg "[p_phrase]"
        "Уклоняешься от его контратаки!"
        show gg dodge at left_battle
        pause 0.8
        show gg battle at left_battle
    else:
        $ hp_player -= troll_damage
        $ p_phrase = renpy.random.choice(player_phrases_get_hit_kirill)
        gg "[p_phrase]"
        "Кирилл бьёт в ответ. [troll_damage] урона. (Ты: [hp_player] HP)"
        show gg impact3 as gg at left_battle
        pause 0.8
        show gg battle at left_battle

    if hp_player <= 0:
        hide screen battle_hud
        jump police_alone_battle_lose

    jump police_alone_battle_loop_phase1


# ---------- ПОБЕДА В ФАЗЕ 1 → ПЕРЕХОД К ФАЗЕ 2 (С АНИМАЦИЕЙ) ----------
# После победы в первой фазе Кирилл трансформируется в усиленную форму.
label police_alone_battle_phase1_win:
    stop music
    play music music_battle loop

    "Кирилл падает на колени. Ты тяжело дышишь, глядя на поверженного врага."

    # Анимация падения Кирилла (1 фаза)
    show kirill fall2 at right_battle
    pause 0.5
    show kirill fall3 at right_battle
    pause 0.5

    gg "Всё кончено, Кирилл."

    "Но вместо ответа он начинает смеяться. Смех — низкий, хриплый, как у того, кому больше нечего терять."

    # Трансформация во вторую фазу – показываем спрайты перерождения
    show kirill reborn1 at right_battle
    pause 0.5
    show kirill reborn2 at right_battle
    pause 0.5

    kirill "Кончено? Ты думаешь, это конец? Нет, Димон. Это только начало."

    "Он медленно поднимается. Его глаза вспыхивают зелёным. Тело покрывается тёмными венами. Он больше не похож на человека."

    hide kirill
    show kirill reborn2 at right_battle

    gg "Что... что ты такое?"

    kirill "Я — твоя тень. Твоя тёмная сторона. И я только начал."

    "Ты чувствуешь, как воздух становится тяжелее. Кирилл изменился. Теперь он — не просто человек. Он — монстр."

    "Начинается вторая фаза боя."

    # ИНИЦИАЛИЗАЦИЯ ДЛЯ HUD (ФАЗА 2) – увеличенные параметры
    $ max_hp_troll = 160
    $ enemy_name = "Кирилл"
    $ phase_two = True
    $ hp_troll = 160
    $ player_damage = 10 + (bravery // 2) + (intellect // 3)   # Урон увеличивается
    $ troll_damage = 18 - (bravery // 3)                       # Урон Кирилла тоже выше
    $ battle_round = 0
    $ key_used = False

    "Ты чувствуешь, как его сила растёт с каждым мгновением. Это будет твой самый трудный бой."

    jump police_alone_battle_loop_phase2


# ---------- ФАЗА 2: УСИЛЕННАЯ ФОРМА КИРИЛЛА ----------
# Аналогично фазе 1, но с другими значениями и более сложным QTE.
label police_alone_battle_loop_phase2:
    show gg battle at left_battle
    show kirill reborn2 at right_battle
    show screen battle_hud
    $ battle_round += 1

    if hp_player <= 0:
        hide screen battle_hud
        jump police_alone_battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump police_alone_battle_phase2_win

    # Динамические фразы для фазы 2
    if hp_troll > 120:
        if renpy.random.randint(1, 3) == 1:
            kirill "Ты думал, это будет легко? Я только разогреваюсь!"
    elif hp_troll > 60:
        if renpy.random.randint(1, 2) == 1:
            kirill "Ты силён... но я сильнее своей тени!"
    else:
        if renpy.random.randint(1, 2) == 1:
            kirill "Ты... ты меня достал! Я уничтожу тебя!"

    "Кирилл стал быстрее, сильнее. Его движения — как молнии. Каждый удар — смертоносен. Ты чувствуешь, как твоё тело сжимается от напряжения."

    menu:
        "⚔ Атаковать":
            jump police_alone_battle_attack_phase2
        "🔑 Использовать ключ" if has_key and not key_used:
            jump police_alone_battle_key_phase2


# Атака в фазе 2
label police_alone_battle_attack_phase2:
    show gg fight2 at left_battle
    $ damage = player_damage + renpy.random.randint(0, 4)
    $ hp_troll -= damage

    $ p_phrase = renpy.random.choice(player_phrases_attack_kirill)
    gg "[p_phrase]"
    "Наносишь [damage] урона. Кирилл шипит от боли, но не останавливается. (Кирилл: [hp_troll] HP)"
    show kirill fall4 at right_battle
    pause 0.5
    show kirill reborn2 at right_battle
    show gg battle at left_battle

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_alone_battle_phase2_win

    jump police_alone_battle_kirill_turn_phase2


# Использование ключа в фазе 2 – тройной урон, но Кирилл уже не так уязвим.
label police_alone_battle_key_phase2:
    stop music
    # play sound key  # Убрано по требованию
    with flash
    $ key_used = True
    $ hp_troll -= player_damage * 3

    $ k_phrase = renpy.random.choice(player_phrases_key_kirill)
    gg "[k_phrase]"
    "Ты поднимаешь ключ. Он вспыхивает ярче, чем когда-либо, но Кирилл не отшатывается. Он идёт прямо на свет."
    show gg fight at left_battle
    show kirill fall4 at right_battle
    pause 0.5
    play music music_battle loop
    show gg battle at left_battle
    show kirill reborn2 at right_battle

    "Ты наносишь [player_damage*3] урона! (Кирилл: [hp_troll] HP)"

    kirill "Слабо! Ты думаешь, этот маленький фокус остановит меня?"

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_alone_battle_phase2_win

    jump police_alone_battle_kirill_turn_phase2


# Ход Кирилла в фазе 2 – QTE с меньшим временем
label police_alone_battle_kirill_turn_phase2:
    $ qte_time = max(0.6, 1.2 - (battle_round - 1) * 0.06)

    # Перед QTE показываем спрайт супер-атаки Кирилла для драматического эффекта
    show kirill superattack1 at right_battle
    pause 0.3

    call screen dodge_choice(time=qte_time, round=battle_round)
    $ result = _return

    if result == "success":
        $ p_phrase = renpy.random.choice(player_phrases_dodge_kirill)
        gg "[p_phrase]"
        "Уклоняешься от его яростной атаки!"
        show gg dodge at left_battle
        pause 0.8
        show gg battle at left_battle
    else:
        $ hp_player -= troll_damage
        $ p_phrase = renpy.random.choice(player_phrases_get_hit_kirill)
        gg "[p_phrase]"
        "Кирилл наносит удар, от которого мир гаснет на мгновение. [troll_damage] урона. (Ты: [hp_player] HP)"
        show gg impact3 as gg at left_battle
        pause 0.8
        show gg battle at left_battle

    # Возвращаем обычный спрайт Кирилла
    show kirill reborn2 at right_battle

    if hp_player <= 0:
        hide screen battle_hud
        jump police_alone_battle_lose

    jump police_alone_battle_loop_phase2


# ---------- ФИНАЛЬНАЯ ПОБЕДА (ОДИНОЧНЫЙ) – С АНИМАЦИЕЙ ПАДЕНИЯ ----------
# После победы во второй фазе Кирилл окончательно повержен.
label police_alone_battle_phase2_win:
    stop music
    play music music_good_ending loop
    hide screen battle_hud

    "Кирилл падает на колени. Его тело начинает дрожать, тёмные вены исчезают, зелёный свет в глазах гаснет."

    # Анимация падения (финальная)
    show kirill fall4 at right_battle
    pause 0.5
    show kirill fall5 at right_battle
    pause 0.5

    $ k_phrase = renpy.random.choice(kirill_phrases_defeat)
    kirill "[k_phrase]"

    gg "Я не хотел этого. Но ты заставил меня."

    kirill "Я не заставлял. Ты сам выбрал этот путь. И ты... ты стал сильнее."

    "Он смотрит на тебя. В его глазах — уважение. И грусть."

    kirill "Теперь ты сможешь проснуться. Но запомни: я всегда буду здесь. В твоей тени."

    "Он исчезает."
    hide kirill

    jump police_alone_battle_win


# ---------- КОНЦОВКА ПОБЕДЫ (ОДИНОЧНЫЙ) ----------
# Игрок просыпается дома, но ключ остаётся – непонятно, сон это или реальность.
label police_alone_battle_win:
    hide screen battle_hud
    scene black with fade
    "Ты победил. Готов проснуться."

    scene bg room_night_real with fade
    show gg smoking at center_pos

    "Открываю глаза. Я за столом. Монитор горит, на столе — остывший кофе."

    "Всё было сном? Или я всё ещё в том мире?"

    "Я достаю из кармана ржавый ключ. Он лежит в моей руке — холодный и тяжёлый."

    "Или это я его просто вообразил? Я больше не уверен ни в чём."

    # Убрано условие с lust – теперь просто концовка
    jump end_chapter


# ---------- ПОРАЖЕНИЕ (ОДИНОЧНЫЙ) – С РЕТРИ ----------
# Если игрок проигрывает, ему даётся до 2 дополнительных попыток.
label police_alone_battle_lose:
    stop music
    play music music_bad_ending loop
    hide screen battle_hud
    scene black with fade

    $ k_phrase = renpy.random.choice(kirill_phrases_victory)
    kirill "[k_phrase]"

    if phase_two:
        kirill "Ты был сильным. Но не достаточно. Спи, брат. Твоя тень будет жить дальше."
    else:
        kirill "Ты слаб. Ты всегда был слаб. Просто прими это."

    if retry_count < 2:
        menu:
            "Попробовать ещё раз? (Осталось [2-retry_count] попыток)":
                jump police_alone_battle_retry
            "Принять поражение.":
                "Тьма забирает тебя навсегда."
                jump bad_end
    else:
        "Ты использовал все шансы. Поражение окончательно."
        "Тьма забирает тебя навсегда."
        jump bad_end


# Повторная попытка боя – восстанавливает здоровье, сбрасывает раунд.
label police_alone_battle_retry:
    $ retry_count += 1
    play music music_battle loop
    "Ты встаёшь, стирая кровь с лица. Бой продолжается! Ты чувствуешь, что силы на исходе, но не можешь сдаться."
    $ hp_player = 25
    $ hp_troll = 40
    $ phase_two = False
    $ battle_round = 0
    $ key_used = False
    jump police_alone_battle_loop_phase1


# ---------- УЧАСТОК ШЕРИФА (С ЛИРОЙ) ----------
# Этот блок запускается, если игрок пришёл в участок вместе с Лирой.
# Структура аналогична одиночному маршруту, но с учётом присутствия Лиры.
label police_together:
    stop music
    play music music_police loop
    scene bg police with fade

    "Мы заходим в участок вместе. Лира держится рядом, её плечо касается моего. Запах старого дерева, бумаги и дешёвого кофе встречает нас."

    show gg smoking at left_pos
    show lira stand at right_pos
    show sheriff scared at center_pos

    sheriff "О, ещё гости. Проходите, садитесь. Рассказывайте, что привело вас в мою берлогу."

    "Мы садимся. Я чувствую, как Лира сжимает мою руку. Она нервничает, но держится."

    gg "Мы выбрались из подземелья. Там был тролль. Мы убили его."

    sheriff "Тролль. И вы вдвоём его убили? Интересно. И что вы там искали?"

    lira "Мы не искали. Мы попали туда случайно. Нас заперли."

    sheriff "Заперли? Кто?"

    # Выбор для совместного допроса
    menu:
        "Не знаю.":
            $ intellect += 1
            jump police_together_unknown
        "Этот ключ.":
            $ bravery += 1
            jump police_together_key
        "Может быть, вы знаете?":
            $ lust += 1
            jump police_together_sheriff_knows


# Далее следуют метки для каждого варианта ответа.
# Они ведут к общему допросу police_together_interrogation.
label police_together_unknown:
    gg "Мы не знаем, кто нас запер. Мы просто очнулись там."
    sheriff "И ты, девушка, тоже не знаешь?"
    lira "Я была там дольше. Я слышала голоса, видела тени, но не знаю, кто они."
    sheriff "Тени. Ты уверена, что это были люди?"
    lira "Нет. Я не уверена ни в чём."
    sheriff "Хорошо. Тогда давайте начнём сначала. Расскажи мне, что ты помнишь о том месте."
    jump police_together_interrogation

label police_together_key:
    gg "У меня был ключ. Символ на нём – круг с перекрестьем. Он был тёплым."
    sheriff "Ключ. Это важно. Где ты его взял?"
    gg "Мне принесли его. В коробке без маркировки."
    sheriff "И ты взял его."
    gg "Да."
    sheriff "Ты знаешь, что это за символ?"
    lira "Я видела его на алтаре в храме. Это метка жрецов."
    sheriff "Жрецы? В этих краях?"
    lira "Да. Они поклоняются тьме. Ключ – это их врата."
    sheriff "Врата... Значит, вы прошли через врата."
    jump police_together_interrogation

label police_together_sheriff_knows:
    gg "Вы местный шериф. Вы должны знать, что там происходит."
    sheriff "Я знаю, что в лесу пропадают люди. Я знаю, что некоторые возвращаются с пустыми глазами. Но я не знаю, что происходит под землёй."
    lira "Вы врёте."
    sheriff "Я не вру. Я просто не знаю всего."
    lira "Тогда почему вы нас здесь держите?"
    sheriff "Я не держу вас. Вы пришли сами. И я хочу понять, кто вы и что вы видели."
    jump police_together_interrogation


# Общий допрос, после которого шериф отправляет Диму в архив, а Лира остаётся.
label police_together_interrogation:
    scene bg police with fade
    show gg thinking at left_pos
    show lira stand at right_pos
    show sheriff scared at center_pos

    sheriff "Теперь давайте поговорим о том, что вы чувствуете. Вы убили тролля. Вы выбрались. Но вы не выглядите счастливыми."
    gg "Счастье – это роскошь. Мы просто выжили."
    sheriff "А ты, девушка? Что ты чувствуешь?"
    lira "Страх. И надежду."
    sheriff "Страх и надежда – хорошее сочетание. Оно помогает жить."
    gg "Мы не за этим пришли. Мы хотим знать, что это было. И как нам вернуться домой."
    sheriff "Домой? Ты хочешь вернуться туда, откуда пришла?"
    lira "У меня нет дома. Я была пленницей."
    sheriff "А теперь ты свободна. Что ты будешь делать с этой свободой?"

    # Вместо выбора о будущем, шериф отправляет Диму в архив
    sheriff "Подождите. Я хочу, чтобы ты, Дима, сходил в архив за синей папкой. Она лежит на третьей полке. Принеси её, она поможет мне в расследовании. А ты, Лира, пока посиди здесь."
    gg "Хорошо."
    "Я встаю и выхожу. Лира остаётся с шерифом."
    jump police_together_archive


# ---------- АРХИВ (СОВМЕСТНЫЙ) ----------
# Аналогично одиночному маршруту, но с дополнительными мыслями о Лире.
label police_together_archive:
    scene bg police_archive with fade
    play music music_dark loop

    "Склад-архив. Сыро, пахнет плесенью. Свет – только одна лампочка под потолком, и она моргает, как больной глаз."

    show gg thinking at center_pos
    gg "Я на месте. Синяя папка, третья полка. Шериф сказал именно это. Но зачем ему это сейчас? Почему именно сейчас?"

    "Я нахожу синюю папку и пролистываю её. Внутри – не просто документы. Это целая история, которую кто-то тщательно прятал."

    show gg confused at center_pos
    gg "Газетные вырезки... пропавшие женщины. Все молодые. Все блондинки. И одна из них – Лира. Она была здесь, в этом списке. Значит, она не просто случайная пленница. Она – часть этой мозаики."

    "Я переворачиваю страницу и вижу фотографию. Кирилл. В форме шерифа, но с чёрной бородой и в тех же очках. На обороте – надпись: «Советник К., 2018»."

    show gg angry at center_pos
    gg "Кирилл. Он был здесь. Он был частью этого мира задолго до меня. Он не просто коллега – он игрок. А я – пешка. Он знал о ключе, о культе, обо всём. И он молчал."

    "Я листаю дальше. Вырванная страница из дневника. Почерк старый, но я разбираю слова."

    show gg thinking at center_pos
    gg "«Ключ – это врата. Тот, кто владеет им, может открыть проход между мирами. Жрецы ищут его уже столетия...» Вот оно. Ключ – не просто оружие. Это проход. И Кирилл хочет его использовать. Но зачем? Чтобы сбежать? Чтобы захватить власть?"

    "Я закрываю папку и смотрю в пустоту архива. Где-то капает вода. Где-то скребутся крысы. Тишина давит."

    show gg smoking at center_pos
    gg "Я понимаю, что шериф – это Кирилл. Он притворялся. Вёл допрос, задавал вопросы, а сам знал ответы. Он хотел проверить, насколько я опасен. И он что-то задумал с Лирой."

    gg "Он отправил меня сюда, чтобы я это нашёл. Чтобы я понял. Чтобы я сделал выбор. Или чтобы он знал, что я знаю. Чёрт..."

    "Я чувствую, как время уходит. Каждая секунда – как удар сердца в тишине. Лира там, с ним. Одна."

    show gg angry at center_pos
    gg "Я должен вернуться. И я должен быть готов к тому, что он раскроет маски. И к тому, что мне придётся выбирать – между ним и Лирой, между правдой и ложью."

    scene black with fade
    "Беру папку под мышку и быстро возвращаюсь. Свет лампы гаснет за спиной, как будто архив не хочет отпускать меня."

    jump police_together_return_from_archive


# ---------- ВОЗВРАЩЕНИЕ И РАСКРЫТИЕ (СОВМЕСТНЫЙ) ----------
# Шериф раскрывает себя, начинается сцена с попыткой домогательства к Лире,
# и игрок может наблюдать или вмешаться.
label police_together_return_from_archive:
    scene bg police with fade
    stop music
    play music music_battle loop

    "Я подхожу к двери кабинета и слышу голоса. Шериф говорит с Лирой, и я слышу её испуганный голос."
    scene bg lira_sheriff1 with fade
    sheriff "Ну же, девочка, не бойся. Дима скоро вернётся. А пока мы можем развлечься."
    lira "Отойди от меня! Я позову на помощь!"
    sheriff "Как говорится - 'Муж в дверь - жена в дверь! Ну же девочка, дай волю эмоциям.'"

    "Я заглядываю в щель. Шериф прижимает Лиру к стене. Она пытается вырваться."

    # Выбор: наблюдать или вмешаться – влияет на храбрость
    menu:
        "Наблюдать из тени (побояться).":
            $ bravery -= 1
            jump police_together_observe
        "Вмешаться.":
            $ bravery += 2
            jump police_together_intervene


# Ветка наблюдения – игрок не вмешивается, видит сексуальную сцену,
# затем шериф раскрывает себя и предлагает групповой секс.
label police_together_observe:
    "Я замираю. Сердце колотится, но я не могу пересилить страх. Я прячусь за углом и смотрю."
    scene bg lira_sheriff2 with fade
    lira "Аагх!"
    sheriff "Сейчас я с тобой поиграюсь."
    scene bg lira_sheriff3 with fade
    gg "Он же трахает ее прямо на своем столе!"
    lira "Помогите! На помощь!"
    scene bg lira_sheriff4 with fade
    play sound fuck loop volume 0.9
    "Шериф ускоряет свой темп. Он трахает Лиру на столе."
    gg "Какой кошмар."
    play sound cum
    scene black with fade
    "Шериф замечает моё присутствие."

    sheriff "А, Дима, ты уже вернулся. Заходи, не стесняйся."

    "Я вхожу. Лира стоит в углу, дрожит."
    scene bg lira_sheriff5 with fade
    kirill "Ты ведь уже догадался, да? Я — Кирилл. Тот самый. И я знаю, что ключ у тебя."

    gg "Что ты хочешь?"

    kirill "Я предлагаю тебе сделку. Мы вместе трахнем Лиру. Это объединит наши силы и откроет врата. Ты получишь власть. Откажешься — умрёшь."

    menu:
        "Согласиться на групповой секс.":
            jump police_together_group_sex_agree
        "Отказаться и биться за Лиру.":
            # Скрываем спрайты перед боем
            hide sheriff
            hide lira
            hide gg
            jump police_together_battle


# Ветка вмешательства – игрок отталкивает шерифа, но затем тот предлагает ту же сделку.
label police_together_intervene:
    "Я бросаюсь вперёд, отталкивая шерифа от Лиры."

    gg "Руки прочь от неё!"

    sheriff "О, Дима, ты вовремя. Я как раз думал, что нам нужно поговорить."

    "Лира выбегает за мою спину. Шериф снимает очки и ухмыляется."

    sheriff "Ты ведь знаешь меня. Я — Кирилл. Твой друг, коллега, а теперь — твой судьба."

    gg "Что тебе нужно?"

    kirill "Я предлагаю тебе сделку. Мы вместе трахнем Лиру. Это объединит наши силы и откроет врата. Ты получишь власть. Откажешься — умрёшь."

    menu:
        "Согласиться на групповой секс.":
            jump police_together_group_sex_agree
        "Отказаться и биться за Лиру.":
            # Скрываем спрайты перед боем
            hide sheriff
            hide lira
            hide gg
            jump police_together_battle


# ===== НОВАЯ МЕТКА: ГРУППОВОЙ СЕКС (СОВМЕСТНЫЙ) =====
# Если игрок соглашается, происходит сцена группового секса, после которой
# Дима умирает от сердечного приступа – плохая концовка.
label police_together_group_sex_agree:

    "Я смотрю на Лиру, потом на Кирилла. Что-то внутри меня срывается. Я киваю."

    gg "Пусть будет так."

    lira "Дима! Ты не можешь!"

    kirill "Отличный выбор, друг. Ты всегда был разумным."

    "Они подходят к ней. Я беру её за руку, а Кирилл — за другую. Она дрожит, но не сопротивляется."

    scene bg lira_sheriff6 with fade
    play music music_orgy loop
    play sound fuck loop

    "Мы кладем её на стол. Кирилл входит в неё сзади, я — спереди. Она стонет, но в её глазах — пустота."

    kirill "Да, Димон. Именно так. Мы станем сильнее."

    lira "П-пожалуйста... перестаньте..."

    "Но я не слышу. Я словно в тумане. Всё происходит как в полусне."

    scene bg lira_sheriff7 with fade
    play sound cum

    "Час спустя мы кончаем на неё. Она лежит без движения, вся в сперме. Я чувствую, как сердце начинает бешено биться."

    gg "Голова... кружится..."

    kirill "Это побочный эффект. Ты получил слишком много силы. Ну ничего, мне и одному хватит."

    "Я падаю на колени. В глазах темнеет. Последнее, что я вижу — ухмыляющееся лицо Кирилла."

    scene black with fade
    play music music_bad_ending loop

    "Дима умер от сердечного приступа. Кирилл остался один с Лирой и ключом."

    jump end_chapter


# ---------- СОВМЕСТНЫЙ БОЙ С КИРИЛЛОМ (НОВАЯ МЕХАНИКА) ----------
# В этом бою Лира может помогать, если её привязанность достаточна.
# Также есть механика жертвы Лиры при поражении.
label police_together_battle:
    hide sheriff
    hide lira

    # ИНИЦИАЛИЗАЦИЯ ДЛЯ HUD (ФАЗА 1)
    $ max_hp_player = 50
    $ max_hp_troll = 80
    $ enemy_name = "Кирилл"

    $ phase_two = False
    $ hp_player = 50
    $ hp_troll = 80
    $ player_damage = 8 + (bravery // 3) + (intellect // 4)
    $ troll_damage = 12 - (bravery // 4)
    $ lira_joined_battle = False
    $ lira_sacrifice = False

    if has_key:
        $ player_damage += 3

    if girl_affinity >= 2:
        $ player_damage += 5                      # Бонус за поддержку Лиры
        "Лира готова помогать. Она встаёт рядом с тобой."

    $ battle_round = 0
    $ key_used = False

    play music music_battle loop
    jump police_together_battle_loop_phase1


# ---------- ФАЗА 1 (СОВМЕСТНЫЙ) ----------
# Аналогично одиночному, но с учётом присутствия Лиры и её возможной помощи.
label police_together_battle_loop_phase1:
    scene bg police with fade
    show gg battle at left_battle
    show kirill at center_pos
    show screen battle_hud
    $ battle_round += 1

    if hp_player <= 0:
        hide screen battle_hud
        jump police_together_battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump police_together_battle_phase1_win

    # Динамические фразы Кирилла (с Лирой)
    if hp_troll > 60:
        if renpy.random.randint(1, 3) == 1:
            $ k_phrase = renpy.random.choice(kirill_phrases_start_lira)
            kirill "[k_phrase]"
    elif hp_troll > 25:
        if renpy.random.randint(1, 2) == 1:
            $ k_phrase = renpy.random.choice(kirill_phrases_mid_lira)
            kirill "[k_phrase]"
    else:
        if renpy.random.randint(1, 2) == 1:
            $ k_phrase = renpy.random.choice(kirill_phrases_low_lira)
            kirill "[k_phrase]"

    # Лира помогает при опасности (если HP игрока <=20 и она ещё не помогала)
    if hp_player <= 20 and not lira_joined_battle and girl_affinity >= 2:
        $ lira_joined_battle = True
        show lira angry at center_pos
        with dissolve
        "Лира видит, что ты слабеешь, и бросается вперёд!"
        $ hp_troll -= 20
        $ dodge_chance += 20                     # Увеличиваем шанс уклонения (влияет на QTE)
        lira "Не трогай его!"
        hide lira angry
        with dissolve

    "Ты и Лира сражаетесь с Кириллом. Он быстр и опасен. Лира уклоняется, а ты наносишь удары."

    menu:
        "⚔ Атаковать":
            jump police_together_battle_attack_phase1
        "🔑 Использовать ключ" if has_key and not key_used:
            jump police_together_battle_key_phase1


# Атака в фазе 1 (совместно)
label police_together_battle_attack_phase1:
    show gg fight2 at left_battle
    $ damage = player_damage + renpy.random.randint(0, 3)
    $ hp_troll -= damage

    $ p_phrase = renpy.random.choice(player_phrases_attack_kirill)
    gg "[p_phrase]"
    "Ты наносишь [damage] урона. Кирилл отступает на шаг. (Кирилл: [hp_troll] HP)"
    show kirill at right_battle
    pause 0.5
    show kirill at right_battle
    show gg battle at left_battle

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_together_battle_phase1_win

    jump police_together_battle_kirill_turn_phase1


# Использование ключа (совместно)
label police_together_battle_key_phase1:
    # play sound key  # Убрано по требованию
    with flash
    $ key_used = True
    $ hp_troll -= player_damage * 3

    $ k_phrase = renpy.random.choice(player_phrases_key_kirill)
    gg "[k_phrase]"
    "Ключ вспыхивает, ослепляя Кирилла."
    show gg fight at left_battle
    show kirill at right_battle
    pause 0.5
    play music music_battle loop
    show gg battle at left_battle
    show kirill at right_battle

    "Ты наносишь [player_damage*3] урона! (Кирилл: [hp_troll] HP)"

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_together_battle_phase1_win

    jump police_together_battle_kirill_turn_phase1


# Ход Кирилла (совместный) – QTE
label police_together_battle_kirill_turn_phase1:
    $ qte_time = max(0.7, 1.5 - (battle_round - 1) * 0.08)

    call screen dodge_choice(time=qte_time, round=battle_round)
    $ result = _return

    if result == "success":
        $ p_phrase = renpy.random.choice(player_phrases_dodge_kirill)
        gg "[p_phrase]"
        "Уклоняешься от его контратаки!"
        show gg dodge at left_battle
        pause 0.8
        show gg battle at left_battle
    else:
        $ hp_player -= troll_damage
        $ p_phrase = renpy.random.choice(player_phrases_get_hit_kirill)
        gg "[p_phrase]"
        "Кирилл бьёт тебя. [troll_damage] урона. (Ты: [hp_player] HP)"
        show gg impact3 as gg at left_battle
        pause 0.8
        show gg battle at left_battle

    if hp_player <= 0:
        hide screen battle_hud
        jump police_together_battle_lose

    jump police_together_battle_loop_phase1


# ---------- ПОБЕДА В ФАЗЕ 1 → ФАЗА 2 (С АНИМАЦИЕЙ) ----------
# После победы в первой фазе Кирилл трансформируется, аналогично одиночному.
label police_together_battle_phase1_win:
    stop music
    play music music_battle loop

    "Кирилл падает на колени. Лира подходит к нему, держа кинжал."

    # Анимация падения Кирилла (1 фаза)
    show kirill fall2 at right_battle
    pause 0.5
    show kirill fall3 at right_battle
    pause 0.5

    kirill "Ты победил... но это только начало."

    "Он поднимается. Его глаза загораются зелёным. Тело покрывается тёмными венами. Он больше не похож на человека."

    # Трансформация во вторую фазу
    show kirill reborn1 at right_battle
    pause 0.5
    show kirill reborn2 at right_battle
    pause 0.5

    kirill "Теперь ты увидишь мою истинную форму. Это моя тень – и она сильнее тебя."

    "Ты чувствуешь, как воздух становится густым. Лира сжимает твою руку."

    hide kirill
    show kirill reborn2 at right_battle

    # ИНИЦИАЛИЗАЦИЯ ДЛЯ HUD (ФАЗА 2)
    $ max_hp_troll = 160
    $ enemy_name = "Кирилл"
    $ phase_two = True
    $ hp_troll = 160
    $ player_damage = 10 + (bravery // 2) + (intellect // 3)
    $ troll_damage = 18 - (bravery // 3)
    $ battle_round = 0
    $ key_used = False

    if girl_affinity >= 3:
        $ player_damage += 8
        "Лира кричит: 'Я не позволю тебе умереть!' – и бросается в атаку вместе с тобой."

    jump police_together_battle_loop_phase2


# ---------- ФАЗА 2 (СОВМЕСТНЫЙ) ----------
# Усиленная форма Кирилла, но Лира может помочь ещё раз.
label police_together_battle_loop_phase2:
    show gg battle at left_battle
    show kirill fight2 at right_battle
    show screen battle_hud
    $ battle_round += 1

    if hp_player <= 0:
        hide screen battle_hud
        jump police_together_battle_lose
    if hp_troll <= 0:
        hide screen battle_hud
        jump police_together_battle_phase2_win

    # Вторая помощь Лиры, если она ещё не присоединилась (но теперь она уже могла помочь)
    if hp_player <= 20 and not lira_joined_battle and girl_affinity >= 2:
        $ lira_joined_battle = True
        "Лира видит, что ты ослабеваешь. Она бросается вперёд, чтобы защитить тебя."
        show lira angry at center_pos
        lira "Не трогай его!"
        $ hp_troll -= 30
        "Она наносит сильный удар! (Кирилл: [hp_troll] HP)"
        hide lira angry

    "Ты сражаешься с усиленным Кириллом. Каждый удар – как гром. Лира рядом, её дыхание сбивается, но она не отступает."

    menu:
        "⚔ Атаковать":
            jump police_together_battle_attack_phase2
        "🔑 Использовать ключ" if has_key and not key_used:
            jump police_together_battle_key_phase2


# Атака в фазе 2 (совместно)
label police_together_battle_attack_phase2:
    show gg fight2 at left_battle
    $ damage = player_damage + renpy.random.randint(0, 4)
    $ hp_troll -= damage

    $ p_phrase = renpy.random.choice(player_phrases_attack_kirill)
    gg "[p_phrase]"
    "Ты наносишь [damage] урона. Кирилл рычит. (Кирилл: [hp_troll] HP)"
    show kirill fall4 at right_battle
    pause 0.5
    show kirill reborn2 at right_battle
    show gg battle at left_battle

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_together_battle_phase2_win

    jump police_together_battle_kirill_turn_phase2


# Использование ключа в фазе 2 (совместно)
label police_together_battle_key_phase2:
    # play sound key  # Убрано по требованию
    with flash
    $ key_used = True
    $ hp_troll -= player_damage * 3

    $ k_phrase = renpy.random.choice(player_phrases_key_kirill)
    gg "[k_phrase]"
    "Ключ вспыхивает ярче прежнего, но Кирилл не отшатывается. Он идёт прямо на свет."
    show gg fight at left_battle
    show kirill fall4 at right_battle
    pause 0.5
    play music music_battle loop
    show gg battle at left_battle
    show kirill reborn2 at right_battle

    "Ты наносишь [player_damage*3] урона! (Кирилл: [hp_troll] HP)"

    kirill "Ты не победишь меня ключом! Я – твоя суть!"

    if hp_troll <= 0:
        hide screen battle_hud
        jump police_together_battle_phase2_win

    jump police_together_battle_kirill_turn_phase2


# Ход Кирилла в фазе 2 (совместно) – QTE с меньшим временем
label police_together_battle_kirill_turn_phase2:
    $ qte_time = max(0.6, 1.2 - (battle_round - 1) * 0.06)

    show kirill superattack1 at right_battle
    pause 0.3

    call screen dodge_choice(time=qte_time, round=battle_round)
    $ result = _return

    if result == "success":
        $ p_phrase = renpy.random.choice(player_phrases_dodge_kirill)
        gg "[p_phrase]"
        "Уклоняешься от его яростной атаки!"
        show gg dodge at left_battle
        pause 0.8
        show gg battle at left_battle
    else:
        $ hp_player -= troll_damage
        $ p_phrase = renpy.random.choice(player_phrases_get_hit_kirill)
        gg "[p_phrase]"
        "Кирилл бьёт тебя с такой силой, что мир качается. [troll_damage] урона. (Ты: [hp_player] HP)"
        show gg impact3 as gg at left_battle
        pause 0.8
        show gg battle at left_battle

    show kirill reborn2 at right_battle

    if hp_player <= 0:
        hide screen battle_hud
        jump police_together_battle_lose

    jump police_together_battle_loop_phase2


# ---------- ФИНАЛЬНАЯ ПОБЕДА (СОВМЕСТНЫЙ) – С АНИМАЦИЕЙ ПАДЕНИЯ ----------
# После победы во второй фазе Кирилл повержен, и в зависимости от привязанности
# Лиры и флага жертвы, следует одна из двух концовок.
label police_together_battle_phase2_win:
    stop music
    play music music_good_ending loop
    hide screen battle_hud

    "Кирилл падает. Его тело содрогается, тёмные вены исчезают. Он смотрит на тебя с уважением."

    # Анимация падения (финальная)
    show kirill fall4 at right_battle
    pause 0.5
    show kirill fall5 at right_battle
    pause 0.5

    $ k_phrase = renpy.random.choice(kirill_phrases_defeat)
    kirill "[k_phrase]"

    gg "Я не хотел этого."

    kirill "Но ты сделал это. Теперь ты свободен. Иди."

    "Он исчезает."
    hide kirill

    "Лира подходит к тебе. Она обнимает тебя."

    lira "Мы сделали это."

    gg "Да. Мы."

    scene black with fade

    "У Димы резко чернеет в глазах."
    
    # Разветвление концовок в зависимости от параметров
    if girl_affinity >= 3 and not lira_sacrifice:
        jump lira_home_romance_scene      # Романтическая концовка с Лирой
    else:
        jump lira_home_lonely_scene       # Лира уходит, или игрок остаётся один


# ---------- ПОРАЖЕНИЕ (СОВМЕСТНЫЙ) – ИСПРАВЛЕННЫЙ ----------
# При поражении в совместном бою возможна жертва Лиры, если её привязанность >=2.
label police_together_battle_lose:
    stop music
    play music music_bad_ending loop
    hide screen battle_hud

    if lira_sacrifice:
        scene bg police with fade
        show gg fall3 at left_pos
        show kirill at center_pos
        "Ты падаешь без сил. Шериф нависает над тобой."
        sheriff "Ты не смог спасти её, и не смог спасти себя."
        scene black with fade
        "Ты проиграл. Тьма забирает тебя навсегда."
        return

    elif girl_affinity >= 2:
        scene bg police with fade
        show gg fall3 at left_pos
        show kirill at center_pos
        show lira scream at right_pos
        $ lira_sacrifice = True
        $ lira_joined_battle = True
        "Лира видит, что ты падаешь, и бросается между тобой и шерифом."
        lira "Беги! Я прикрою!"
        "Шериф наносит удар, и Лира падает замертво."
        hide lira scream
        scene bg lira_dead with fade
        pause 1.0
        "Ты смотришь на её бездыханное тело. Она пожертвовала собой ради тебя."
        "Ты встаёшь с новой, яростной силой!"
        stop music
        play music music_battle loop
        scene bg police with fade
        $ hp_player = 30
        $ hp_troll = 35
        "Ты должен закончить это ради неё!"
        jump police_together_battle_loop_phase2

    else:
        scene bg police with fade
        show gg fall3 at left_pos
        show kirill at center_pos
        show lira stand at right_pos
        sheriff "Ты проиграл. Ты слишком слаб, чтобы защитить её."
        "Ты падаешь без сил. Кирилл подходит к Лире, но она отворачивается от него и смотрит на тебя с презрением."
        lira "Ты не смог. Я думала, ты другой."
        "Лира отдалась Кириллу. Он трахает ее на своем рабочем столе."
        scene black with fade
        "Ты потерял всё. Лира отвернулась от тебя, Кирилл победил. Тьма забирает тебя."
        jump bad_end