import psycopg2
from datetime import date

DATABASE = "studs"
HOST = "pg"
PORT = "5432"

connection = psycopg2.connect(
    dbname=DATABASE,
    host=HOST,
    port=PORT
)
cursor = connection.cursor()

# Function to insert data into locality table
def insert_locality(name, foundation_date):
    query = "INSERT INTO locality (name, foundation_date) VALUES (%s, %s);"
    data = (name, foundation_date)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into church table
def insert_church(name, foundation_date, locality_id):
    query = "INSERT INTO church (name, foundation_date, locality_id) VALUES (%s, %s, %s);"
    data = (name, foundation_date, locality_id)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into prison table
def insert_prison(name, locality_id):
    query = "INSERT INTO prison (name, locality_id) VALUES (%s, %s);"
    data = (name, locality_id)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into bible table
def insert_bible(version, publication_date, name):
    query = "INSERT INTO bible (version, publication_date, name) VALUES (%s, %s, %s);"
    data = (version, publication_date, name)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into commandment table
def insert_commandment(description, rank):
    query = "INSERT INTO commandment (description, rank) VALUES (%s, %s);"
    data = (description, rank)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into bible_commandment table
def insert_bible_commandment(bible_id, commandment_id):
    query = "INSERT INTO bible_commandment (bible_id, commandment_id) VALUES (%s, %s);"
    data = (bible_id, commandment_id)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into person table
def insert_person(name, surname, birth_date, person_gender, locality):
    query = "INSERT INTO person (name, surname, birth_date, person_gender, locality_id) VALUES (%s, %s, %s, %s, %s);"
    data = (name, surname, birth_date, person_gender, locality)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into official table
def insert_official(person_id, official_name, employment_date, fired_date=None):
    query = "INSERT INTO official (person_id, official_name, employment_date, fired_date) VALUES (%s, %s, %s, %s);"
    data = (person_id, official_name, employment_date, fired_date)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into punishment table
def insert_punishment(name, description=None):
    query = """
    INSERT INTO punishment (name, description)
    VALUES (%s, %s);
    """
    data = (name, description)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into torture_type table
def insert_torture_type(name, description=None):
    query = """
    INSERT INTO torture_type (name, description)
    VALUES (%s, %s);
    """
    data = (name, description)
    cursor.execute(query, data)
    connection.commit()


# Example data for localities
localities = [
    ('Белый Сад', date(1150, 1, 1)),
    ('Залипье', date(960, 2, 10)),
    ('Штуйгуры', date(1273, 3, 20)),
    ('Харвикен', date(870, 3, 20)),
    ('Тодерас', date(777, 3, 20)),
]

# Inserting data into locality table
for locality in localities:
    insert_locality(*locality)

# Example data for churches
churches = [
    ('Базилика Святого Семейства', date(1150, 1, 1), 1),
    ('Санта-Мария-дель-Мар', date(960, 1, 10), 2),
    ('Базилика Ковадонга', date(1273, 8, 15), 3),
    ('Эрмитаж Эль-Росио', date(870, 5, 25), 4),
    ('Гваделупа', date(777, 5, 25), 5),
]

# Inserting data into church table
for church in churches:
    insert_church(*church)

# Example data for prisons
prisons = [
    ('Тюрьма при Базилики Святого Семейства', 1),
    ('Тюрьма при Санта-Мария-дель-Мар', 2),
    ('Тюрьма при Гваделупе', 5),
]

# Inserting data into prison table
for prison in prisons:
    insert_prison(*prison)

# Example data for bible versions
bibles = [
    (1, date(89, 1, 1), 'Bible 1'),
    (2, date(356, 2, 10), 'Bible 2'),
    (3, date(498, 3, 20), 'Bible 3'),
]

# Inserting data into bible table
for bible in bibles:
    insert_bible(*bible)

# Example data for commandments
commandments = [
    ('Да не будет у тебя других богов пред лицем Моим.', 5),
    ('Чтение запрещенных книг.', 5),
    ('Не делай идолов.', 4),
    ('Не произноси имени Господа, Бога твоего, всуе.', 3),
    ('Помни день субботний, чтобы святить его.', 2),
    ('Почитай отца твоего и мать твою.', 2), 
    ('Не убей.', 5), 
    ('Не прелюбодействуй.', 3),
    ('Не укради.', 4), # 8
    ('Не лжесвидетельствуй против ближнего твоего.', 1), 
    ('Не возжелай, не завидуй', 4),
    ('Не сквернословь.', 2),
    ('Не желай плохого обидчику своему,не совершай мести.', 2),
    ('Ешь, чтобы быть сытым. Не объедайся.', 3),
    ('Почитай святые места.', 3),
    ('Будь честен.', 2),
]

# Inserting data into commandment table
for commandment in commandments:
    insert_commandment(*commandment)

# Example data for bible_commandments
# FIXME: кажется есть проблемка с тем, что мы не проверям есть ли такой свод в Бибилии, по которой проходит процесс
bible_commandments = [
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (1, 11),
    (1, 13),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (2, 8),
    (2, 9),
    (3, 1),
    (3, 2),
    (3, 3),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (3, 8),
    (3, 9),
    (3, 10),
    (3, 11),
    (3, 12),
    (3, 13),
    (3, 14),
    (3, 15),
]

# Inserting data into bible_commandment table
for bible_commandment in bible_commandments:
    insert_bible_commandment(*bible_commandment)

# Example data for persons
persons = [
    ('Александр', 'Иванов', date(1412, 11, 27), 'М', 1),
    ('Михаил', 'Кузнецов', date(1406, 11, 8), 'М', 2),
    ('Дмитрий', 'Соколов', date(1414, 5, 17), 'М', 3),
    ('Игорь', 'Козлов', date(1412, 2, 23), 'М', 4),
    ('Николай', 'Носов', date(1420, 5, 7), 'М', 5),
    ('Константин', 'Морозов', date(1420, 5, 7), 'М', 1),
    ('Василий', 'Зайцев', date(1405, 11, 27), 'М', 2),
    ('Сергей', 'Волков', date(1412, 10, 12), 'М', 3),
    ('Светлана', 'Попова', date(1403, 10, 21), 'Ж', 4),
    ('Анна', 'Лебедева', date(1418, 3, 20), 'Ж', 5),
    ('Мария', 'Виноградова', date(1415, 9, 20), 'Ж', 1),
    ('Елена', 'Смирнова', date(1417, 3, 5), 'Ж', 2),
    ('Ольга', 'Петрова', date(1413, 8, 12), 'Ж', 3),
    ('Татьяна', 'Белоусова', date(1410, 6, 27), 'Ж', 4),
    ('Надежда', 'Степанова', date(1401, 1, 6), 'Ж', 5),
    ('Георгий', 'Борисов', date(1409, 4, 19), 'М', 1), # 16
    ('Маргарита', 'Григорьева', date(1402, 1, 6), 'Ж', 2),
    ('Владимир', 'Тихонов', date(1412, 11, 3), 'М', 3),
    ('Виктория', 'Савельева', date(1419, 2, 2), 'Ж', 4),
    ('Антон', 'Романов', date(1406, 8, 4), 'М', 5),
    ('Ирина', 'Захарова', date(1404, 12, 26), 'Ж', 1),
    ('Ярослав', 'Голубев', date(1400, 2, 20), 'М', 2),
    ('Юлия', 'Михайлова', date(1417, 11, 6), 'Ж', 3),
    ('Илья', 'Федосеев', date(1407, 11, 18), 'М', 4),
    ('Ксения', 'Тарасова', date(1416, 1, 24), 'Ж', 5),
    ('Григорий', 'Андреев', date(1417, 3, 21), 'М', 1),
    ('Дарья', 'Белякова', date(1420, 7, 15), 'Ж', 2),
    ('Роман', 'Осипов', date(1415, 7, 24), 'М', 3),
    ('София', 'Сергеева', date(1401, 10, 27), 'Ж', 4),
    ('Андрей', 'Родионов', date(1408, 12, 12), 'М', 5),

]


# Inserting data into person table
for person in persons:
    insert_person(*person)

# Example data for officials (assuming some person IDs from the previous insertions)
officials = [
    (1, 'Епископ', date(1455, 1, 1)),
    (30, 'Епископ', date(1445, 1, 1)),
    (28, 'Епископ', date(1447, 1, 1)),
    (26, 'Епископ', date(1467, 1, 1)),
    (2, 'Светсткая власть', date(1434, 2, 2)),
    (6, 'Светсткая власть', date(1434, 2, 2)),
    (3, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (4, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (5, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (8, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (7, 'Фискал', date(1486, 4, 4), date(1495, 4, 4)),
]

# Inserting data into official table
for official in officials:
    insert_official(*official)

punishments = [
    ('Казнь', 'Description1'),
    ('Епетимья', 'Description2'),
    ('Аутодафе', 'Description3'),
]

# Inserting data into punishment table
for punishment in punishments:
    insert_punishment(*punishment)

# Example data for torture_types
torture_types = [
    ('Падение связанного узника с высоты', 'Классные ощущения полета, только падать большо'),
    ('Пытка водой', 'Самое то в жаркий день и в засуху'),
    ('Пытка огнем', 'Лучше держать 40 минут на среднем огне. Так мясо прожариться, но при это сохранит весь сок. Получить очень нежным и сочным'),
]

# Inserting data into torture_type table
for torture_type in torture_types:
    insert_torture_type(*torture_type)

# Close the connection after completion
cursor.close()
connection.close()