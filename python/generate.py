# import psycopg2
import random
from datetime import timedelta, datetime, date
from person_data import russian_male_names, russian_female_names, russian_male_surnames, russian_female_surnames
from commandment_data import commandments
import csv

from datetime import datetime, timedelta
import random
from dateutil.relativedelta import relativedelta

random.seed(10)

def random_date_without_formating(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def random_date(start, end):
    return random_date_without_formating(start, end).strftime('%Y-%m-%d')

def add_date_without_formating(start_date, plus):
    return start_date + relativedelta(months=plus)

def minus_date_without_formating(start_date, plus):
    return start_date - relativedelta(months=plus)

def add_days_without_formating(start_date, plus):
    return start_date + relativedelta(days=plus)
def add_days(start_date, plus):
    return add_days_without_formating(start_date, plus).strftime('%Y-%m-%d')

def add_date(start_date, plus):
    return add_date_without_formating(start_date, plus).strftime('%Y-%m-%d')

def save_to_file(filename, header, elements):
    with open(filename, mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        for row in elements:
            writer.writerow(row)

DATABASE = "studs"
USERNAME = "YourUsername"
PASSWORD = "YourPassword"
HOST = "pg"
PORT = "5432"

# uncomment
# connection = psycopg2.connect(
    # dbname=DATABASE,
    # host=HOST,
    # port=PORT
# )
# cursor = connection.cursor()
connection = ""
cursor = ""

def insert_locality(name, foundation_date):
    query = "INSERT INTO locality (name, foundation_date) VALUES (%s, %s);"
    data = (name, foundation_date)
    cursor.execute(query, data)
    connection.commit()

def insert_church(name, foundation_date, locality_id):
    query = "INSERT INTO church (name, foundation_date, locality_id) VALUES (%s, %s, %s);"
    data = (name, foundation_date, locality_id)
    cursor.execute(query, data)
    connection.commit()

def insert_prison(name, locality_id):
    query = "INSERT INTO prison (name, locality_id) VALUES (%s, %s);"
    data = (name, locality_id)
    cursor.execute(query, data)
    connection.commit()

def insert_bible(version, publication_date, name):
    query = "INSERT INTO bible (version, publication_date, name) VALUES (%s, %s, %s);"
    data = (version, publication_date, name)
    cursor.execute(query, data)
    connection.commit()

def insert_commandment(description, rank):
    query = "INSERT INTO commandment (description, rank) VALUES (%s, %s);"
    data = (description, rank)
    cursor.execute(query, data)
    connection.commit()

def insert_bible_commandment(bible_id, commandment_id):
    query = "INSERT INTO bible_commandment (bible_id, commandment_id) VALUES (%s, %s);"
    data = (bible_id, commandment_id)
    cursor.execute(query, data)
    connection.commit()

def insert_person(name, surname, birth_date, person_gender, locality_id):
    query = "INSERT INTO person (name, surname, birth_date, person_gender, locality_id) VALUES (%s, %s, %s, %s, %s);"
    data = (name, surname, birth_date, person_gender, locality_id)
    cursor.execute(query, data)
    connection.commit()

def insert_official(person_id, official_name, employment_date, fired_date=None):
    query = "INSERT INTO official (person_id, official_name, employment_date, fired_date) VALUES (%s, %s, %s, %s);"
    data = (person_id, official_name, employment_date, fired_date)
    cursor.execute(query, data)
    connection.commit()

def insert_inquisition_process(start_date, finish_date, official_id, church_id, bible_id):
    query = """
    INSERT INTO inquisition_process (start_data, finish_data, official_id, church_id, bible_id)
    VALUES (%s, %s, %s, %s, %s);
    """
    data = (start_date, finish_date, official_id, church_id, bible_id)
    cursor.execute(query, data)
    connection.commit()

def insert_accusation_process(start_time, finish_time, inquisition_process_id):
    query = """
    INSERT INTO accusation_process (start_time, finish_time, inquisition_process_id)
    VALUES (%s, %s, %s);
    """
    data = (start_time, finish_time, inquisition_process_id)
    cursor.execute(query, data)
    connection.commit()

def insert_accusation_record(informer, bishop, accused, violation_place, violation_time, description, id_accusation, record_time):
    query = """
    INSERT INTO accusation_record (informer, bishop, accused, violation_place, violation_time, description, id_accusation, record_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    data = (informer, bishop, accused, violation_place, violation_time, description, id_accusation, record_time)
    cursor.execute(query, data)
    connection.commit()

def insert_investigative_case(creation_date, closed_date=None):
    query = """
    INSERT INTO investigative_case (creation_date, closed_date)
    VALUES (%s, %s);
    """
    data = (creation_date, closed_date)
    cursor.execute(query, data)
    connection.commit()

def insert_accusation_investigative_case(case_id, record_id):
    query = """
    INSERT INTO accusation_investigative_case (case_id, record_id)
    VALUES (%s, %s);
    """
    data = (case_id, record_id)
    cursor.execute(query, data)
    connection.commit()

def insert_punishment(name, description=None):
    query = """
    INSERT INTO punishment (name, description)
    VALUES (%s, %s);
    """
    data = (name, description)
    cursor.execute(query, data)
    connection.commit()

def insert_case_log(case_id, case_status, principal, start_time, result, prison_id, finish_time, punishment_id, description=None):
    query = """
    INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, punishment_id, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    data = (case_id, case_status, principal, start_time, result, prison_id, finish_time, punishment_id, description)
    cursor.execute(query, data)
    connection.commit()

def insert_violation(commandment_id, record_id):
    query = """
    INSERT INTO violation (commandment_id, record_id)
    VALUES (%s, %s);
    """
    data = (commandment_id, record_id)
    cursor.execute(query, data)
    connection.commit()

def insert_torture_type(name, description=None):
    query = """
    INSERT INTO torture_type (name, description)
    VALUES (%s, %s);
    """
    data = (name, description)
    cursor.execute(query, data)
    connection.commit()

def insert_torture_log(case_log_id, type_id, executor, victim):
    query = """
    INSERT INTO torture_log (case_log_id, type_id, executor, victim)
    VALUES (%s, %s, %s, %s);
    """
    data = (case_log_id, type_id, executor, victim)
    cursor.execute(query, data)
    connection.commit()


localities = [
    ('Barcelona', date(800, 4, 7)),
    ('Girona', date(719, 6, 1)),
    ('Lleida', date(905, 8, 20)),
    ('Tarragona', date(815, 9, 12)),
    ('Pamplona', date(623, 2, 18)),
    ('Vitoria-Gasteiz', date(1181, 7, 14)),
    ('Logroño', date(920, 12, 23)),
    ('Oviedo', date(578, 2, 21)),
    ('Santander', date(1042, 11, 11)),
    ('Valladolid', date(1072, 11, 9)),
    ('Gijón', date(733, 10, 5)),
    ('Palencia', date(919, 5, 2)),
    ('Salamanca', date(1118, 3, 1)),
    ('Soria', date(1108, 7, 21)),
    ('Burgos', date(884, 7, 20)),
    ('León', date(910, 6, 29)),
    ('Pontevedra', date(895, 9, 15)),
    ('Lugo', date(697, 2, 18)),
    ('Ourense', date(775, 8, 1)),
    ('A Coruña', date(599, 5, 13)),
    ('Badajoz', date(861, 4, 10)),
    ('Córdoba', date(789, 1, 20)),
    ('Granada', date(1013, 2, 5)),
    ('Sevilla', date(712, 4, 25)),
    ('Murcia', date(828, 7, 3)),
    ('Albacete', date(871, 12, 9)),
    ('Alicante', date(739, 11, 14)),
    ('Valencia', date(1060, 6, 17)),
    ('Zaragoza', date(756, 8, 29)),
    ('Toledo', date(542, 9, 22)),
]

#TODO
# for locality in localities:
    # insert_locality(*locality)
localities_to_save = [(id, *(localities[id-1])) for id in range(1, len(localities) + 1)]

save_to_file('backup/locality.csv', ['id', 'name', 'foundation_date'], localities_to_save)

churches = [
    ('Iglesia de Santa María', date(912, 8, 14), 1),
    ('Basílica de San Pedro', date(975, 3, 2), 2),
    ('Catedral de San Cristóbal', date(1005, 12, 7), 3),
    ('Iglesia de San Mateo', date(1101, 4, 21), 4),
    ('Catedral de la Asunción', date(1140, 6, 30), 5),
    ('Iglesia de San Francisco', date(900, 11, 15), 6),
    ('Basílica de La Merced', date(1052, 5, 18), 7),
    ('Iglesia de Santa Eulalia', date(1156, 7, 23), 8),
    ('Catedral de San Juan', date(952, 8, 19), 9),
    ('Iglesia de los Santos Justo y Pastor', date(1073, 2, 28), 10),
    ('Iglesia de Santa Cecilia', date(902, 7, 10), 11),
    ('Catedral de la Encarnación', date(915, 8, 29), 12),
    ('Iglesia de San Ginés', date(960, 3, 11), 13),
    ('Catedral de San Salvador', date(1103, 9, 20), 14),
    ('Iglesia de Santa Catalina', date(1000, 5, 30), 15),
    ('Catedral de La Santa Cruz', date(1095, 10, 14), 16),
    ('Iglesia de San Martín', date(1080, 9, 17), 17),
    ('Catedral de San Vicente', date(920, 1, 5), 18),
    ('Iglesia del Salvador', date(1091, 5, 19), 19),
    ('Catedral de San Antolín', date(1020, 12, 7), 20),
    ('Iglesia de San Isidoro', date(1006, 4, 12), 21),
    ('Catedral de San Lorenzo', date(1189, 6, 28), 22),
    ('Iglesia de San Pedro', date(1108, 10, 30), 23),
    ('Catedral de Santa María', date(1001, 2, 22), 24),
    ('Iglesia de San Miguel', date(1111, 8, 18), 25),
    ('Catedral de San Andrés', date(1065, 11, 11), 26),
    ('Iglesia de Santa Clara', date(1105, 7, 9), 27),
    ('Catedral de Santa Ana', date(961, 8, 24), 28),
    ('Iglesia del Espíritu Santo', date(1098, 12, 21), 29),
    ('Catedral de Santiago', date(1000, 5, 25), 30),
    ('Iglesia de San Andrés', date(1122, 2, 1), 1),
    ('Catedral de Santa Isabel', date(821, 3, 21), 2),
    ('Iglesia de San Nicolás', date(1109, 11, 22), 3),
    ('Basílica de Santa María del Mar', date(950, 6, 14), 4),
    ('Iglesia de San Pablo', date(1104, 2, 25), 5),
    ('Catedral de San Miguel', date(1195, 7, 7), 6),
    ('Iglesia de San Juan Bautista', date(920, 3, 31), 7),
    ('Catedral de San Esteban', date(960, 9, 17), 8),
    ('Iglesia de Santa Teresa', date(930, 11, 1), 9),
    ('Catedral de Nuestra Señora de la Asunción', date(1088, 1, 22), 10),
    ('Iglesia de San Bartolomé', date(1130, 10, 17), 11),
    ('Catedral de la Inmaculada Concepción', date(965, 6, 2), 12),
    ('Iglesia del Sagrado Corazón', date(1024, 12, 15), 13),
    ('Catedral de San Ildefonso', date(1110, 3, 8), 14),
    ('Iglesia de San Pedro Apóstol', date(1035, 4, 18), 15),
    ('Catedral de San Ignacio de Loyola', date(907, 11, 25), 16),
    ('Iglesia de San Agustín', date(1180, 8, 28), 17),
    ('Catedral del Buen Pastor', date(1125, 7, 10), 18),
    ('Iglesia de Santa Mónica', date(1131, 1, 6), 19),
    ('Catedral de San Francisco de Asís', date(961, 10, 4), 20),
    ('Iglesia de San Estanislao', date(1128, 9, 13), 21),
    ('Catedral de la Santísima Trinidad', date(1049, 8, 6), 22),
    ('Iglesia del Santo Ángel', date(1152, 5, 20), 23),
    ('Catedral de Santa Eulalia', date(1047, 12, 12), 24),
    ('Iglesia de San Antonio de Padua', date(1028, 9, 8), 25),
    ('Catedral de San Julián', date(983, 4, 9), 26),
    ('Iglesia de San Benito', date(1118, 5, 17), 27),
    ('Catedral del Nacimiento de Nuestra Señora', date(960, 10, 1), 28),
    ('Iglesia del Silencio', date(1190, 9, 29), 29),
    ('Catedral de San José', date(1140, 10, 20), 30),
]

#TODO
# for church in churches:
    # insert_church(*church)
churches_to_save = [(id, *(churches[id - 1])) for id in range(1, len(churches) + 1)]
save_to_file('backup/church.csv', ['id', 'name', 'foundation_date', 'locality_id'], churches_to_save)

prisons = [
    ('Centro Penitenciario Albolote', 1),
    ('Centro Penitenciario Algeciras', 2),
    ('Centro Penitenciario Alicante', 3),
    ('Centro Penitenciario Almendro', 4),
    ('Centro Penitenciario Almería', 5),
    ('Centro Penitenciario Araba', 6),
    ('Centro Penitenciario Badajoz', 7),
    ('Centro Penitenciario Barcelona', 8),
    ('Centro Penitenciario Burgos', 9),
    ('Centro Penitenciario Cáceres', 10),
    ('Centro Penitenciario Cádiz', 11),
    ('Centro Penitenciario Cartagena', 12),
    ('Centro Penitenciario Castellón', 13),
    ('Centro Penitenciario Ceuta', 14),
    ('Centro Penitenciario Ciudad Real', 15),
    ('Centro Penitenciario Córdoba', 16),
    ('Centro Penitenciario Cuenca', 17),
    ('Centro Penitenciario Granada', 18),
    ('Centro Penitenciario Guadalajara', 19),
    ('Centro Penitenciario Huelva', 20),
    ('Centro Penitenciario Huesca', 21),
    ('Centro Penitenciario Jaén', 22),
    ('Centro Penitenciario La Coruña', 23),
    ('Centro Penitenciario Las Palmas', 24),
    ('Centro Penitenciario La Rioja', 25),
    ('Centro Penitenciario León', 26),
    ('Centro Penitenciario Lleida', 27),
    ('Centro Penitenciario Lugo', 28),
    ('Centro Penitenciario Málaga', 29),
    ('Centro Penitenciario Melilla', 30),
    ('Centro Penitenciario Mataró', 1),
    ('Centro Penitenciario Mérida', 2),
    ('Centro Penitenciario Murcia', 3),
    ('Centro Penitenciario Navarra', 4),
    ('Centro Penitenciario Ocaña', 5),
    ('Centro Penitenciario Ourense', 6),
    ('Centro Penitenciario Palencia', 7),
    ('Centro Penitenciario Palma de Mallorca', 8),
    ('Centro Penitenciario Pamplona', 9),
    ('Centro Penitenciario Pontevedra', 10),
    ('Centro Penitenciario Salamanca', 11),
    ('Centro Penitenciario Santa Cruz de Tenerife', 12),
    ('Centro Penitenciario Santander', 13),
    ('Centro Penitenciario Segovia', 14),
    ('Centro Penitenciario Sevilla', 15),
    ('Centro Penitenciario Soria', 16),
    ('Centro Penitenciario Tarragona', 17),
    ('Centro Penitenciario Teruel', 18),
    ('Centro Penitenciario Toledo', 19),
    ('Centro Penitenciario Valencia', 20),
    ('Centro Penitenciario Valladolid', 21),
    ('Centro Penitenciario Vigo', 22),
    ('Centro Penitenciario Villabona', 23),
    ('Centro Penitenciario Vitoria', 24),
    ('Centro Penitenciario Zamora', 25),
    ('Centro Penitenciario Zaragoza', 26),
    ('Centro Penitenciario Albacete', 27),
    ('Centro Penitenciario Ávila', 28),
    ('Centro Penitenciario Bilbao', 29),
    ('Centro Penitenciario Cáceres II', 30)
]

#TODO
# for prison in prisons:
#     insert_prison(*prison)
prisons_to_save = [(id, *(prisons[id - 1])) for id in range(1, len(prisons) + 1)]
save_to_file('backup/prison.csv', ['id', 'name', 'locality_id'], prisons_to_save)

bibles = [
    (1, date(89, 1, 1), 'Bible 1'),
    (2, date(356, 2, 10), 'Bible 2'),
    (3, date(498, 3, 20), 'Bible 3'),
]

#TODO
# for bible in bibles:
#     insert_bible(*bible)
save_to_file('backup/bible.csv', ['version', 'publication_date', 'name'], bibles)

#TODO
# for commandment in commandments:
#     insert_commandment(commandment)
commandments_to_save = [(i, commandments[i - 1], 5 - (i // 150), None) for i in range(1, len(commandments) + 1)]
save_to_file('backup/commandment.csv', ['id', 'description', 'rank', 'description_vector'], commandments_to_save)

# #TODO
first_bible_commandments = [(1, comm_id) for comm_id in range(1, len(commandments) + 1, 5)]
# for bible_commandment in first_bible_commandments:
#     insert_bible_commandment(*bible_commandment)

second_bible_commandments = [(2, comm_id) for comm_id in range(1, len(commandments) + 1, 3)]
# for bible_commandment in second_bible_commandments:
#     insert_bible_commandment(*bible_commandment)
    
third_bible_commandments = [(3, comm_id) for comm_id in range(1, len(commandments) + 1)]
# for bible_commandment in third_bible_commandments:
#     insert_bible_commandment(*bible_commandment)
bible_commandments = first_bible_commandments + second_bible_commandments + third_bible_commandments
save_to_file('backup/bible_commandment.csv', ['bible_id, commandment_id'], bible_commandments)

birth_start = datetime(1400, 1, 1)
birth_end = datetime(1420, 12, 31)

persons = []
persons_to_save = []
locality_by_person_id = {}
persons_by_locality = {}

curr_locality_id = 1
#TODO
for i in range(1, 25151):

    m_name = random.choice(russian_male_names)[0]
    m_surname = random.choice(russian_male_surnames)[0]
    m_birth_date = random_date(birth_start, birth_end)
    
    if i < 151:
        m_locality_id = curr_locality_id
    else:
        m_locality_id = random.randrange(1, 31)

    persons.append([2 * i - 1, m_name, m_surname, m_birth_date, 'М', m_locality_id])
    persons_to_save.append([m_name, m_surname, m_birth_date, 'М', m_locality_id])
    locality_by_person_id[2 * i - 1] = m_locality_id
    # insert_person(m_name, m_surname, m_birth_date, 'M', m_locality_id)

    if m_locality_id not in persons_by_locality:
        persons_by_locality[m_locality_id] = [i]
    else:
        persons_by_locality[m_locality_id].append(i)
    
    f_name = random.choice(russian_female_names)[0]
    f_surname = random.choice(russian_female_surnames)[0]
    f_birth_date = random_date(birth_start, birth_end)
    
    if i < 151:
        f_locality_id = curr_locality_id
    else:
        f_locality_id = random.randrange(1, 31)

    persons.append([2 * i, f_name, f_surname, f_birth_date, 'Ж', f_locality_id])
    persons_to_save.append([f_name, f_surname, f_birth_date, 'Ж', f_locality_id])
    locality_by_person_id[2 * i] = f_locality_id
    # insert_person(f_name, f_surname, f_birth_date, 'F', f_locality_id)
    
    if f_locality_id not in persons_by_locality:
        persons_by_locality[f_locality_id] = [i]
    else:
        persons_by_locality[f_locality_id].append(i)

    if i % 30 == 0:
        curr_locality_id += 1
 
save_to_file('backup/person.csv', ['id', 'name', 'surname', 'birth_date', 'gender', 'locality_id'], persons)

official_types = [
    'Инквизитор',
    'Епископ',
    'Светская власть',
    'Фискал'
]

used_id = set()

hired_start = datetime(1445, 1, 1)
hired_end = datetime(1486, 12, 31)

fired_start = datetime(1490, 1, 1)
fired_end = datetime(1510, 12, 31)

officials = []
officials_to_save = []
official_ids = set()

# bishop = {}
inqusitors = []
# fiskal = {}
# sovety = {}

bishops_by_locality = {}

#TODO
counter = 1
for i in range(1, 5):
    j = 0
    for type_o in official_types:
        for q in range(1, 5):
            person_id = (i - 1) * 30 + j * 4 + q
            type_officials = type_o
            hired_date = random_date(hired_start, hired_end)
            fired_date = None

            officials.append([counter, person_id, type_officials, hired_date, fired_date])
            officials_to_save.append([person_id, type_officials, hired_date, fired_date])
            official_ids.add(person_id)
            
            if type_officials == 'Епископ':
                # bishop[person_id] = [person_id, type_officials, hired_date, fired_date]
                locality = locality_by_person_id[person_id]
                
                if locality not in bishops_by_locality:
                    bishops_by_locality[locality] = [counter]
                else:
                    bishops_by_locality[locality].append(counter)

            elif type_officials == 'Инквизитор':
                inqusitors.append([counter, person_id, type_officials, hired_date, fired_date])
            # elif type_officials == 'Фискал':
                # pass
                # fiskal[person_id] = [person_id, type_officials, hired_date, fired_date]
            # else:
                # pass
                # sovety[person_id] = [person_id, type_officials, hired_date, fired_date]

            # insert_official(person_id, type_officials, hired_date, fired_date)
            counter += 1
        j += 1


for i in range(64, 20065):
    person_id = random.randrange(1, 50001)
    type_officials = random.choice(official_types)
    hired_date = random_date(hired_start, hired_end)
    fired_date = random_date(fired_start, fired_end)

    if i % 2 == 1 and person_id not in official_ids:
        fired_date = None
    
    officials.append([counter, person_id, type_officials, hired_date, fired_date])
    officials_to_save.append([person_id, type_officials, hired_date, fired_date])
    official_ids.add(person_id)
    
    if type_officials == 'Епископ':
        # bishop[person_id] = [person_id, type_officials, hired_date, fired_date]
        locality = locality_by_person_id[person_id]
        
        if locality not in bishops_by_locality:
            bishops_by_locality[locality] = [counter]
        else:
            bishops_by_locality[locality].append(counter)

    elif type_officials == 'Инквизитор':
        inqusitors.append([counter, person_id, type_officials, hired_date, fired_date])
    # elif type_officials == 'Фискал':
        # pass
        # fiskal[person_id] = [person_id, type_officials, hired_date, fired_date]
    # else:
        # pass
        # sovety[person_id] = [person_id, type_officials, hired_date, fired_date]

    # insert_official(person_id, type_officials, hired_date, fired_date)
    counter += 1
save_to_file('backup/official.csv', ['id', 'person_id', 'official_name', 'employment_date', 'fired_date'], officials)

inquis_start = datetime(1480, 1, 1)
inquis_end = datetime(1490, 12, 31)

processes = []
processes_to_save = []
process_by_locality = {}
locality_by_process = {}

#TODO
for i in range(1, 5):
    start_date = random_date_without_formating(inquis_start, inquis_end)
    finish_date = add_date(start_date, random.randint(4, 9))
    start_date = start_date.strftime('%Y-%m-%d')
    
    inquis = inqusitors[(i - 1) * 20][0]
    locality_for_process = i
    church_id = locality_for_process
    bible = random.randrange(1, 4)

    processes.append([i, start_date, finish_date, inquis, church_id, bible])
    processes_to_save.append([start_date, finish_date, inquis, church_id, bible])
    if locality_for_process not in process_by_locality:
        process_by_locality[locality_for_process] = [(i, start_date, finish_date, inquis, church_id, bible)]
    else:
        process_by_locality[locality_for_process].append((i, start_date, finish_date, inquis, church_id, bible))
    locality_by_process[i] = locality_for_process
    # insert_inquisition_process(start_date, finish_date, inquis, church_id, bible)

save_to_file('backup/inquisition_process.csv', ['id', 'start_date', 'finish_date', 'official_id', 'church_id', 'bible_id'], processes)

date_by_accusation = {}
accusation_process = []
accusation_by_process = {}
accusations_to_save = []

#TODO
for proc in processes:
    start_date_proc = datetime.strptime(proc[1], "%Y-%m-%d")
    finish_date_proc = add_date_without_formating(start_date_proc, random.randint(4, 9))
    start_date_acc = start_date_proc
    finish_date_acc = add_days(start_date_acc, random.randrange(1, 120))
    start_date_acc = start_date_acc.strftime('%Y-%m-%d')

    accusation_by_process[proc[0]] = [len(accusation_process)+1, start_date_acc, finish_date_acc, proc[0]]
    accusation_process.append([len(accusation_process)+1, start_date_acc, finish_date_acc, proc[0]])
    accusations_to_save.append([start_date_acc, finish_date_acc, proc[0]])
    # insert_accusation_process(start_date_acc, finish_date_acc, proc[0])
save_to_file('backup/accusation_process.csv', ['id', 'start_time', 'finish_time', 'inquisition_process_id'], accusation_process)

violations = [
    ('Дом художника в Саламанке', 'Совершение колдовских обрядов и заклинаний, противоречащих Библии.'),
    ('Церковь Санта-Мария в Севилье', 'Ересь и распространение ложных учений о Святой Троице.'),
    ('Тайный синагога в Толедо', 'Отступничество от католической веры и тайное исповедание иудаизма.'),
    ('Лавка купца в Гранаде', 'Ворожба на ущерб здоровью и благополучию соседей, что противоречит заповедям Библии.'),
    ('Дворец герцога в Валенсии', 'Чтение и распространение запрещенных книг и активное участие в еретических собраниях.'),
    ('Капелла Сантьяго в Барселоне', 'Отрицание Божественности Христа и оскорбление священных символов.'),
    ('Рынок Алхамбра в Сарагосе', 'Тайное сотрудничество с мусульманами и продажа христианской военной информации.'),
    ('Поместье знатного сеньора в Кордове', 'Нарушение правил поста и богослужения во время Великого поста.'),
    ('Таверна у подножия крепости Бильбао', 'Содействие беглецам, обвиняемым в ереси, и сокрытие еретических печатных изданий.'),
    ('Театр Сан-Феликс в Таррагоне', 'Смех над святым образом Мадонны и высмеивание религиозных истин.'),
    ('Церковь святого Доминика в Сеговии', 'Тайное насаждение идеями альбигойцев и пропаганда против церкви.'),
    ('Домашняя библиотека ученого в Авиле', 'Изучение геретических трактатов и величание запрещенных авторов.'),
    ('Площадь Фернандо III в Бургосе', 'Призыв к открытому неповиновению духовенству и к созданию альтернативной церкви.'),
    ('Монастырь Сан-Хуан в Руэда', 'Изнасилование монахини и осквернение священного места.'),
    ('Учебный класс в Университете Алькала', 'Открытое критикование учения о преображении и сарказм насчет чуда.'),
    ('Цветочная лавка в Лериде', 'Проклятие на церковь, священниц и осквернение места поклонения.'),
    ('Рыбацкий квартал в Кадисе', 'Сокрытие убийства местного священника и обнародование клеветы о его погибели.'),
    ('Тайные встречи Логроño', 'Ритуальные самоистязания и открытая критика церковной иерархии.'),
    ('Исповедальня в катедрале Леона', 'Секретное раскрытие исповедей членам антицерковной группировки.'),
    ('Краеведческий музей в Кастельоне', 'Уничтожение христианских икон и святых образов.'),
    ('Мастерская каменщика в Памплоне', 'Создание и установка статуй идолов, противоречащих заповедям Библии и исповеданием христианства.'),
    ('Тайный подвал в Альмерии', 'Проведение сатанинских ритуалов и жертвоприношение черной мессе.'),
    ('Детская школа в Героне', 'Проведение пропаганды еретических учений среди молодежи и воспитанников.'),
    ('Кондитерская на главной улице Сантандер', 'Отравление священницы и её ассистента.'),
    ('Замок Алькасар в Черкесске', 'Тайное укрытие еретиков и организация подпольных митингов.'),
    ('Подворье местного землевладельца в Салерно', 'Кража реликвий и осквернение святынь.'),
    ('Термы в Мериде', 'Распространение распущенности и осквернение тела, созданного по образу и подобию Божьему.'),
    ('Башня наблюдения в Гибралтаре', 'Открытое выражение сомнения в святости церковных деятелей и проклятие на их действия.'),
    ('Семейное загородное имение в Армерии', 'Колдовство и проведение обрядов чародейства с использованием священных предметов.'),
    ('Оружейный магазин в Заморе', 'Прокачивание, продажа и обучение использованию оружия для антицерковных интересов.'),
    ('Издательский дом в Витории', 'Написание, печать и распространение книг, содержащих еретические идеи.'),
    ('Аптека Раймундо в Тарифе', 'Производство и продажа ядов для убийства верующих и насаждение страха в общине.'),
    ('Церковь святого Агостино в Эль Веро', 'Содействие скрытию атеистических мыслителей и проведение секретных дебатов.'),
    ('Центральная площадь Ла-Коруньи', 'Проповеди об уничтожении католической церкви и призывы к ее распаду.'),
    ('Частный дом в Ронда', 'Организация обучения чёрной магии и колдовства для последующего использования в антицерковных целях.'),
    ('Изготовление икон в Кармона', 'Изменение христианских святых и создание еретических символов вместо допустимых образов.'),
    ('Прачечная на одной из улиц Малаги', 'Проведение обрядов очищения от духов католической веры и пропаганда неподдержки духовенства.'),
    ('Гостевой дом в Логроньо', 'Устраивание тайных встреч с беглыми еретиками и предоставление укрытия.'),
    ('Книжный магазин в Андхуэла', 'Сбыт и продвижение антицерковной литературы и еретических сочинений.'),
    ('Колодец на окраине Мурсии', 'Подстрекательство к колдовству, проведение тайных ритуалов в полночь.'),
    ('Мост обогревателей в Паленсии', 'Саботаж и разрушение церковных построек, осквернение священного места.'),
    ('Частный банк в Касерес', 'Финансирование антицерковных деятелей и их разрушительных действий по всей стране.'),
    ('Ткацкая мастерская в Оссуна', 'Секретное создание и распространение оккультных символов на одежде и других предметах.'),
    ('Поместье Наварро в Алькора', 'Тайная организация еретических восстаний против церковной власти и насаждение авторитета.'),
    ('Лесопилка на окраине Гвадалахары', 'Производство факелов и поджог часовни святой Марии.'),
    ('Частный лавочник в Хаэне', 'Сокрытие свитков с геретическими текстами и привоз запрещенной литературы из-за границы.'),
    ('Столярная мастерская в Линаресе', 'Тайное изготовление устройств для пыток настигаемых инквизицией и связывание с еретиками.'),
    ('Конюшня на окраине Марбельи', 'Шпионаж и передача информации об инквизиционных актах иначе верующим.'),
    ('Пекарня на центральной улице Талаверы', 'Размещение антицерковных лозунгов на хлебных изделиях и замена христианских образов.'),
    ('Сады аль-Хами в Эльче', 'Организация кландестинных митингов еретиков и обсуждение планов будущих акций.'),
    ('Частная резиденция в Мотрил', 'Использование замаскированных комнат для проведения секретных ритуалов и скрытия запрещенных рукописей.'),
    ('Каминная комната в Замора', 'Производство и сбыт поддельных церковных документов и искусственного восстановления еретиков среди общества.'),
    ('Школа святого Игнатия в Вильяреале', 'Введение еретического и антицерковного контента в учебную программу и отравление ума студентов.'),
    ('Лавка ремесленника в Фигерасе', 'Тайное производство амулетов и талисманов, содержащих оккультные символы и несущих еретические послания.'),
    ('Башня знатного сеньора в Лерме', 'Тайное хранение и изучение геретических рукописей, отвергающих учение католической церкви.'),
    ('Винодельня в Вальядолиде', 'Подмешивание геретической лирики в песни, исполняемые на празднествах и трапезах.'),
    ('Библиотека монастыря в Торревьехе', 'Подделка религиозных книг и замена священных текстов на еретические идеи и проповеди.'),
    ('Портовая таверна в Алицанте', 'Распространение слухов о коррупции церковной иерархии и подрыв общественного доверия к духовным лидерам.'),
    ('Дом местного лекаря в Химене', 'Применение оккультных методов в исцелении и проведение лечения с противоречащим Библии практиками.'),
    ('Сад ягодника в Рекена', 'Тайное выращивание и использование отравленных растений в коварных планах против церкви и её служителей.'),
    ('Художественная галерея в Манресе', 'Распространение изображений с антицерковными и еретическими сюжетами, выявляющими дестабилизацию церковных истин.'),
    ('Улочка рядом с церковью в Эстепоне', 'Проведение антицерковных светских митингов и планирование действий по освобождению от духовенства.'),
    ('Обувной магазин в Теруэль', 'Гражданская неподчиненность и отказ от уплаты податей церкви, призывая народ к восстанию против католического монарха.'),
    ('Студия ювелира в Ла Гвардии', 'Подделка церковных реликвий и использование их в еретических служениях и обрядах.'),
    ('Университет святых Филиппа и Якова в Салины', 'Активное насаждение просветительских и антицерковных идей среди преподавателей и студентов.'),
    ('Мост в виде акведука в Ла Херад', 'Осквернение места проведения крещения и планирование обрушения моста во время католического паломничества.'),
    ('Местная аптека в Оренсе', 'Продажа средств антицерковного действия, включая поддельные медикаменты и зелья для использования против православной церкви.'),
    ('Конфетная фабрика в Эгедола', 'Продажа сладостей с антицерковной аналогией, разрыхление авторитета местного духовенства.'),
    ('Фонтан на главной площади Калафельа', 'Открытое объявление о своей верности враждебным мнениям и идеям, относящимся к церкви.'),
    ('Оратория святого Мартина в Херика', 'Создание и прослушивание еретических проповедей, противоречащих учению католической церкви.'),
    ('Исторический архив в Алькой', 'Подделка и изменение документов, свидетельствующих о деятельности инквизиции на территории государства.'),
    ('Зал заседаний местного совета в Лойола', 'Тайное планирование мятежей и кампаний против господства католической церкви.'),
    ('Приватный сад в Кармоне', 'Тайная практика поклонения древним языческим богам и проведение жертвоприношений.'),
    ('Кабинет философии в академии Навальмораль', 'Тайное насаждение деистических и антицерковных идей в учебном процессе и активное влияние на слабых умы студентов.'),
    ('Цветочный магазин на площади Кармезин в Эль-Пуэбло', 'Сбыт и раскрытие геретических посланий, оставленных на открытках с букетами цветов.'),
    ('Угловая башня дворца в Онтиньенте', 'Секретные встречи с еретиками и несанкционированные сделки с антицерковными деятелями.'),
    ('Старая мельница на окраине Балрасе', 'Использование места для проведения обрядов тайного общества, посвященного осквернению христианских истин.'),
    ('Торговый корабль у берега Арсуаль', 'Сокрытие и перевозка людей, обвиняемых в ереси и их помощников, передавая им укрытие и материальную поддержку.'),
    ('Живописная беседка в саду имения Трухильо', 'Проведение еретических семинаров и обсуждение методов подрыва власти церкви.'),
    ('Мастерская музыканта в Солсоне', 'Создание еретических песнопений и гимнов, пропагандирующих антицерковные идеи.'),
    ('Набережная канала в Исла Кристина', 'Граффити с антицерковными лозунгами и символами подрыва авторитета католической веры.'),
    ('Переплетческая мануфактура в Маде...', 'Скрытое соучастие в печати и распространении запрещенных антицерковных публикаций и трактатов.'),
    ('Кладбище святого Лазаря в Агиларе', 'Осквернение могил духовных деятелей и организация еретических собраний ночью на святой земле.'),
    ('Башня искателя в Брионе', 'Наблюдение за движением священников и процессиями и передача информации о них враждебным силам.'),
    ('Завод по производству свечей в Уэске', 'Изготовление свечей с антицерковными символами и продажа их верующим в целях осквернения богослужений.'),
    ('Театральная школа в Коломере', 'Создание и постановка спектаклей, высмеивающих священнослужителей и разрушающих авторитет церкви.'),
    ('Школа искусств при церкви Сан-Педро в Ансоуль', 'Перевод и тайна распространения еретических текстов вместо классической христианской литературы.'),
    ('Круглый стол в местных винных погребах Жадаме', 'Клуб секретных дискуссий и кладовая псевдорелигиозной идеологии, направленной на уничтожение католической веры.'),
    ('Паломничество к святому источнику эль-Ибрагим', 'Проведение тайных еретических служб, основанных на отрицании основных принципов Библии и католического вероучения.'),
    ('Студия писателя в Антеэкере', 'Тайная подготовка и публикация текстов, продолжательность распространения еретических принципов и антицерковных представлений среди чтения публики.'),
    ('Башня с видом на реку Бетис в Монторо', 'Организация тайных встреч для обсуждения планов по устранению влиятельного духовенства и созданию антицерковной коммунальной системы.'),
    ('Подпольное заключение в лабиринте Базтан', 'Страшная тюрьма для заключенных еретиков, выжженных католической церковью жертвами на кострах.'),
    ('Изоляция монахов в монастыре Картена', 'Введение еретических представлений в общину монастыря и открытая критика Преподобным Отцам Ордения.'),
    ('Португальский перевал в Кастельару', 'Разговаривая и находясь в непосредственной оппозиционной связи с еретиками во время передачи государственного и церковного истеблишмента.'),
    ('Ресторан с видом на морскую бухту Лас-Росас', 'Создание и предложение блюд, символически ассоциирующихся с отвержением церковных заповедей и католической доктрины.'),
    ('Бутик конфет в Хересе', 'Приучение детей к геретическим идеям через серию направленного на них средства обращения и упаковки.'),
    ('Школа иностранных языков в Хехоне', 'Классы просветительского движения и набор идей о ратализме, деизме и прямой конфронтации с установленными религиозными взглядами.'),
    ('В церкви Сан-Антонио', 'Проповедь еретических идей, отрицающих Библию.'),
    ('На центральной площади', 'Произнесение богохульных высказываний о святых и церкви.'),
    ('У себя дома', 'Конспирация для распространения антицерковной литературы.'),
    ('В монастыре', 'Получение и передача тайных знаков геретических организаций.'),
    ('В доме старейшин', 'Ссыкултратион и побои священника.'),
    ('На сельском кладбище', 'Ночные тайные саббаты и чёрные мессы.'),
    ('В библиотеке', 'Подделка и изменение священных текстов.'),
    ('В общественном саду', 'Открытое презиление Христианской веры.'),
    ('На рынке', 'Продажа амулетов и грезициских символов.'),
    ('В школе', 'Обучение детей еретическим учениям и отвержение духовенству.'),
    ('В гостинице', 'Злоупотребление имуществом и тайная организация антицерковных мероприятий.'),
    ('На ферме', 'Осквернение священных книг и земли.'),
    ('В таверне', 'Заведомо ложное обвинение священника в воровстве.'),
    ('В парке', 'Участие и подготовка видео рояля в богохулительных целях.'),
    ('В деревенской площади', 'Насильственной окрути Shnape и патия нек умудрания их.'),
    ('В мастерской', 'Изготовление икон и крестов с неприемлемыми символами.'),
    ('В соборе', 'Порочнение и опорчение священных образов.'),
    ('На реке', 'Клеветнические разговоры о замещении духовных ценностей.'),
    ('В лесу', 'Посещение ведьмы и использование её заклинаний в злонамеренных целях.'),
    ('В столовой общины', 'Блазн потебирования проблемы и обсуждение священной тайны')
]
accusation_record = []
accusation_record_to_save = []
counter = 1
#TODO
for key, value in accusation_by_process.items():
    acc_pr_id = value[0]
    locality = locality_by_process[key]
    for i in range(100 * 100 + 10):
        violation = random.choice(violations)
        violation_place = violation[0]
        if i < 10:
            description = violation[1]
        else:
            description = random.choice(violations)[1]
        
        accuset_id = 0
        while True:
            accuset_id = random.choice(persons)[0]
            if accuset_id not in official_ids:
                break
        
        informer_id = 0
        while True:
            informer_id = random.choice(persons)[0]
            if accuset_id not in official_ids:
                break
        
        if i < 50:
            informer_id = accuset_id

        bishop = random.choice(bishops_by_locality[locality])
        st_date = datetime.strptime(value[1], "%Y-%m-%d")
        fn_date = datetime.strptime(value[2], "%Y-%m-%d")
        violation_time = random_date(minus_date_without_formating(st_date, 12), st_date)
        record_time = random_date(st_date, fn_date)

        accusation_record.append([counter, informer_id, bishop, accuset_id, violation_place, violation_time, description, acc_pr_id, record_time, None])
        accusation_record_to_save.append([informer_id, bishop, accuset_id, violation_place, violation_time, description, acc_pr_id, record_time, None])
        counter += 1
        # insert_accusation_record(informer, bishop, accused, violation_place, violation_time, description, id_accusation, record_time)

save_to_file('backup/accusation_record.csv', ['id', 'informer', 'bishop', 'accused', 'violation_place', 'violation_time', 'description', 'id_accusation', 'record_time', 'status'], accusation_record)

punishments = [
    ('Казнь', 'Ну убили и все'),
    ('Епетимья', 'На поболтать'),
    ('Аутодафе', 'Командный синк'),
]
punishments_to_save = [(id, *(punishments[id - 1])) for id in range(1, len(punishments) + 1)]
save_to_file('backup/punishment.csv', ['id', 'name', 'description'], punishments_to_save)
#TODO
# for punishment in punishments:
#     insert_punishment(*punishment)

violations_to_save = []
#TODO
for record_id in range(1, len(accusation_record)):
    if record_id % 100 == 0:
        continue
    commandment_id = random.randint(1, len(commandments))
    violations_to_save.append([commandment_id, record_id])
    # insert_violation(commandment_id, record_id)

save_to_file('backup/violation.csv', ['commandment_id', 'record_id'], violations_to_save)

torture_types = [
    ('Падение связанного узника с высоты', 'Классные ощущения полета, только падать большо'),
    ('Пытка водой', 'Самое то в жаркий день и в засуху'),
    ('Пытка огнем', 'Лучше держать 40 минут на среднем огне. Так мясо прожариться, но при это сохранит весь сок. Получить очень нежным и сочным'),
]
torture_types_to_save = [(id, *(torture_types[id - 1])) for id in range(1, len(torture_types) + 1)]
save_to_file('backup/torture_type.csv', ['id', 'name', 'description'], torture_types_to_save)
#TODO
# for torture_type in torture_types:
    # insert_torture_type(*torture_type)


# Close the connection after completion
# cursor.close()
# connection.close()
