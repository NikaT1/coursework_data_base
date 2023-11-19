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
def insert_commandment(description):
    query = "INSERT INTO commandment (description) VALUES (%s);"
    data = (description,)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into bible_commandment table
def insert_bible_commandment(bible_id, commandment_id):
    query = "INSERT INTO bible_commandment (bible_id, commandment_id) VALUES (%s, %s);"
    data = (bible_id, commandment_id)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into person table
def insert_person(name, birth_date, person_gender):
    query = "INSERT INTO person (name, birth_date, person_gender) VALUES (%s, %s, %s);"
    data = (name, birth_date, person_gender)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into official table
def insert_official(person_id, official_name, employment_date, fired_date=None):
    query = "INSERT INTO official (person_id, official_name, employment_date, fired_date) VALUES (%s, %s, %s, %s);"
    data = (person_id, official_name, employment_date, fired_date)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into inquisition_process table
def insert_inquisition_process(start_date, finish_date, official_id, church_id, bible_id):
    query = """
    INSERT INTO inquisition_process (start_data, finish_data, official_id, church_id, bible_id)
    VALUES (%s, %s, %s, %s, %s);
    """
    data = (start_date, finish_date, official_id, church_id, bible_id)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into accusation table
def insert_accusation(informer, bishop, inquisition_process_id):
    query = """
    INSERT INTO accusation (informer, bishop, inquisition_process_id)
    VALUES (%s, %s, %s);
    """
    data = (informer, bishop, inquisition_process_id)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into accusation_record table
def insert_accusation_record(violation_place, accused, date_time, description, id_accusation):
    query = """
    INSERT INTO accusation_record (violation_place, accused, date_time, description, id_accusation)
    VALUES (%s, %s, %s, %s, %s);
    """
    data = (violation_place, accused, date_time, description, id_accusation)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into investigative_case table
def insert_investigative_case(creation_date, closed_date=None):
    query = """
    INSERT INTO investigative_case (creation_date, closed_date)
    VALUES (%s, %s);
    """
    data = (creation_date, closed_date)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into accusation_investigative_case table
def insert_accusation_investigative_case(case_id, record_id):
    query = """
    INSERT INTO accusation_investigative_case (case_id, record_id)
    VALUES (%s, %s);
    """
    data = (case_id, record_id)
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

# Function to insert data into case_log table
def insert_case_log(case_id, case_status, principal, start_time, result, prison_id, finish_time, punishment_id, description=None):
    query = """
    INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, punishment_id, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    data = (case_id, case_status, principal, start_time, result, prison_id, finish_time, punishment_id, description)
    cursor.execute(query, data)
    connection.commit()

# Function to insert data into violation table
def insert_violation(commandment_id, case_id):
    query = """
    INSERT INTO violation (commandment_id, case_id)
    VALUES (%s, %s);
    """
    data = (commandment_id, case_id)
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

# Function to insert data into torture_log table
def insert_torture_log(case_log_id, type_id, executor, victim):
    query = """
    INSERT INTO torture_log (case_log_id, type_id, executor, victim)
    VALUES (%s, %s, %s, %s);
    """
    data = (case_log_id, type_id, executor, victim)
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
    ('Да не будет у тебя других богов пред лицем Моим.'),
    ('Не делай идолов.'),
    ('Не произноси имени Господа, Бога твоего, всуе.'),
    ('Помни день субботний, чтобы святить его.'),
    ('Почитай отца твоего и мать твою.'), 
    ('Не убей.'), 
    ('Не прелюбодействуй.'),
    ('Не укради.'), # 8
    ('Не лжесвидетельствуй против ближнего твоего.'), 
    ('Не возжелай.'),
    ('Не сквернословь.'),
    ('Не желай плохого обидчику своему.'),
    ('Ешь, чтобы быть сытым. Не объедайся.'),
    ('Почитай святые места.'),
    ('Будь честен.'),
]

# Inserting data into commandment table
for commandment in commandments:
    insert_commandment(commandment)

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
    ('Александр Иванов', date(1412, 11, 27), 'М'),
    ('Михаил Кузнецов', date(1406, 11, 8), 'М'),
    ('Дмитрий Соколов', date(1414, 5, 17), 'М'),
    ('Игорь Козлов', date(1412, 2, 23), 'М'),
    ('Николай Носов', date(1420, 5, 7), 'М'),
    ('Константин Морозов', date(1420, 5, 7), 'М'),
    ('Василий Зайцев', date(1405, 11, 27), 'М'),
    ('Сергей Волков', date(1412, 10, 12), 'М'),
    ('Светлана Попова', date(1403, 10, 21), 'Ж'),
    ('Анна Лебедева', date(1418, 3, 20), 'Ж'),
    ('Мария Виноградова', date(1415, 9, 20), 'Ж'),
    ('Елена Смирнова', date(1417, 3, 5), 'Ж'),
    ('Ольга Петрова', date(1413, 8, 12), 'Ж'),
    ('Татьяна Белоусова', date(1410, 6, 27), 'Ж'),
    ('Надежда Степанова', date(1401, 1, 6), 'Ж'),
    ('Георгий Борисов', date(1409, 4, 19), 'М'), # 16
    ('Маргарита Григорьева', date(1402, 1, 6), 'Ж'),
    ('Владимир Тихонов', date(1412, 11, 3), 'М'),
    ('Виктория Савельева', date(1419, 2, 2), 'Ж'),
    ('Антон Романов', date(1406, 8, 4), 'М'),
    ('Ирина Захарова', date(1404, 12, 26), 'Ж'),
    ('Ярослав Голубев', date(1400, 2, 20), 'М'),
    ('Юлия Михайлова', date(1417, 11, 6), 'Ж'),
    ('Илья Федосеев', date(1407, 11, 18), 'М'),
    ('Ксения Тарасова', date(1416, 1, 24), 'Ж'),
    ('Григорий Андреев', date(1417, 3, 21), 'М'),
    ('Дарья Белякова', date(1420, 7, 15), 'Ж'),
    ('Роман Осипов', date(1415, 7, 24), 'М'),
    ('София Сергеева', date(1401, 10, 27), 'Ж'),
    ('Андрей Родионов', date(1408, 12, 12), 'М'),

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
    (3, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (4, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (5, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (6, 'Инквизитор', date(1487, 3, 3), date(1499, 3, 3)),
    (7, 'Фискал', date(1486, 4, 4), date(1495, 4, 4)),
]

# Inserting data into official table
for official in officials:
    insert_official(*official)

# Example data for inquisition_processes (assuming some official IDs, church IDs, and bible IDs from previous insertions)
inquisition_processes = [
    (date(1489, 1, 1), date(1489, 5, 1), 3, 1, 3),
    (date(1480, 2, 1), date(1480, 6, 1), 4, 2, 1),
    (date(1481, 5, 1), date(1481, 11, 1), 5, 3, 2),
    (date(1483, 4, 21), date(1483, 8, 1), 6, 4, 3),
]

# Inserting data into inquisition_process table
for inquisition_process in inquisition_processes:
    insert_inquisition_process(*inquisition_process)

# Example data for accusations (assuming some person IDs, official IDs, and inquisition_process IDs from previous insertions)
accusations = [
    (8, 1, 1),
    (16, 2, 2),
    (12, 3, 3),
    (13, 4, 4),
    (18, 1, 1),
    (19, 2, 2),
    (20, 3, 3),
    (21, 4, 4),
]

# Inserting data into accusation table
for accusation in accusations:
    insert_accusation(*accusation)

# Example data for accusation_records (assuming some person IDs and accusation IDs from previous insertions)
# дата преступления
accusation_records = [
    ('Дома на столе', 22, date(1488, 8, 12), 'Найдена книга с запрещенными текстами', 1),
    ('Около церкви', 23, date(1479, 10, 2), 'Выругался на прохожего', 2),
    ('На сенокосе', 24, date(1480, 6, 22), 'Ради мести сломал орудие труда и подставил другого', 3),
    ('Ночью в комнате', 25, date(1483, 4, 18), 'Просил Бога наказать знакомого, потому что тому повезло', 4),
    ('У меня дома', 27, date(1488, 10, 18), 'Съел всю еду', 1),
    ('Слева от главной площади, есть дом с коричневой крышей', 13, date(1479, 12, 26), 'Украл из дома драгоценности', 3),
    ('В церковь', 11, date(1481, 3, 8), 'Появился в церкви в нетрезвом виде', 2),
    ('С утра на дороге в город', 14, date(1483, 3, 4), 'Подкупил местного офицера', 4),
]

# Inserting data into accusation_record table
for accusation_record in accusation_records:
    insert_accusation_record(*accusation_record)

# Example data for investigative_cases
# дата заведения дела
investigative_cases = [
    (date(1489, 2, 12), date(1490, 3, 12)),
    (date(1480, 3, 2), date(1480, 3, 22)),
    (date(1481, 5, 22), date(1481, 8, 22)),
    (date(1483, 4, 25), date(1483, 5, 18)),
    (date(1489, 1, 28), date(1489, 2, 22)),
    (date(1481, 5, 27), date(1481, 7, 2)),
    (date(1483, 4, 22), date(1483, 5, 22)),
]

# Inserting data into investigative_case table
for investigative_case in investigative_cases:
    insert_investigative_case(*investigative_case)

# Example data for accusation_investigative_cases (assuming some investigative_case IDs and accusation_record IDs from previous insertions)
accusation_investigative_cases = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (2, 8),
]

# Inserting data into accusation_investigative_case table
for accusation_investigative_case in accusation_investigative_cases:
    insert_accusation_investigative_case(*accusation_investigative_case)


# Example data for punishments
punishments = [
    ('Punishment1', 'Description1'),
    ('Punishment2', 'Description2'),
    ('Punishment3', 'Description3'),
    ('Punishment4', 'Description4'),
]

# Inserting data into punishment table
for punishment in punishments:
    insert_punishment(*punishment)

# Example data for case_logs (assuming some investigative_case IDs, official IDs, prison IDs, and punishment IDs from previous insertions)
# FIXME: проверить, что инквизитор 3 4 5 совпадает с инквизитором при инквизиции
# FIXME: проверить, что id обвиненных совпадают
case_logs = [
    (1, 'Пыточный процесс', 3, date(1489, 2, 22), 'Признание вины', 2, date(1489, 2, 23), 1, 'Признал вину после первой пытки, лох какой-то'),
    (2, 'Исправительная беседа', 2, date(1479, 10, 12), 'Отрицание вины', 2,  date(1479, 10, 13), 2, 'Сказал бы да, пошел бы домой, а так на висилицу ушел'),
    (3, 'Наказание', 3, date(1480, 7, 14), 'Отрицание вины', 3, None, 3, 'Наказание: сделать 5 лаб по ЛЛП за месяц'),
    (4, 'Пыточный процесс', 4, date(1483, 5, 15), 'Признание вины', 2, date(1483, 5, 17), 3, 'Жалко пацана'),
    (5, 'Исправительная беседа', 1, date(1488, 10, 28), 'Признание вины', 1, date(1488, 11, 8), 1, 'Ну съел всю еду, ну был голодный. С кем не случается'),
    (6, 'Наказание', 2, date(1480, 1, 26), 'Отрицание вины', 2, None, 2, 'Палач устал, все домой'),
    (7, 'Пыточный процесс', 5, date(1481, 6, 1), 'Отрицание вины', 1, date(1481, 6, 4), 3, 'Крепкий орешек, не раскололся'),
    (1, 'Исправительная беседа', 3, date(1483, 3, 24), 'Отрицание вины', 3, date(1483, 3, 26), 3, 'Как же хочется спать'),
]

# Inserting data into case_log table
for case_log in case_logs:
    insert_case_log(*case_log)

# Example data for violations (assuming some commandment IDs and investigative_case IDs from previous insertions)
violations = [
    (1, 1),
    (2, 3),
    (3, 2),
    (4, 6),
    (5, 7),
    (6, 5),
    (7, 4),
    (8, 1),
]

# Inserting data into violation table
for violation in violations:
    insert_violation(*violation)

# Example data for torture_types
torture_types = [
    ('Падение связанного узника с высоты', 'Классные ощущения полета, только падать большо'),
    ('Пытка водой', 'Самое то в жаркий день и в засуху'),
    ('Пытка огнем', 'Лучше держать 40 минут на среднем огне. Так мясо прожариться, но при это сохранит весь сок. Получить очень нежным и сочным'),
]

# Inserting data into torture_type table
for torture_type in torture_types:
    insert_torture_type(*torture_type)

# Example data for torture_logs (assuming some case_log IDs, torture_type IDs, official IDs, and person IDs from previous insertions)
torture_logs = [
    (1, 1, 7, 22),
    (4, 2, 7, 25),
    (7, 3, 7, 11),
]

# Inserting data into torture_log table
for torture_log in torture_logs:
    insert_torture_log(*torture_log)



# Close the connection after completion
cursor.close()
connection.close()
