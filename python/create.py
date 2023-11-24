import psycopg2

DATABASE = "studs"
HOST = "pg"
PORT = "5432"

connection = psycopg2.connect(
    dbname=DATABASE,
    host=HOST,
    port=PORT
)
cursor = connection.cursor()

# SQL statements to create tables
create_locality_table = """
CREATE TABLE IF NOT EXISTS locality (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    foundation_date date
);
"""

create_church_table = """
CREATE TABLE IF NOT EXISTS church (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    foundation_date date,
    locality_id integer NOT NULL REFERENCES locality(id) ON DELETE CASCADE
);
"""

create_prison_table = """
CREATE TABLE IF NOT EXISTS prison (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    locality_id integer NOT NULL REFERENCES locality(id) ON DELETE CASCADE
);
"""

create_bible_table = """
CREATE TABLE IF NOT EXISTS bible (
    version integer PRIMARY KEY,
    publication_date date,
    name varchar(255) NOT NULL
);
"""

# SQL statements to create tables and type
create_commandment_table = """
CREATE TABLE IF NOT EXISTS commandment (
    id serial PRIMARY KEY,
    description text NOT NULL UNIQUE,
    rank integer NOT NULL CHECK (rank > 0 and rank < 6)
);
"""

create_bible_commandment_table = """
CREATE TABLE IF NOT EXISTS bible_commandment (
    bible_id integer REFERENCES bible(version) ON DELETE CASCADE,
    commandment_id integer REFERENCES commandment(id) ON DELETE RESTRICT,
    PRIMARY KEY(bible_id, commandment_id)
);
"""

create_gender_type = """
CREATE TYPE gender as enum ('М', 'Ж');
"""

create_person_table = """
CREATE TABLE IF NOT EXISTS person (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    birth_date date NOT NULL,
    person_gender gender NOT NULL,
    locality_id integer REFERENCES locality(id) ON DELETE RESTRICT
);
"""

create_type_query = """
CREATE TYPE official_name as enum ('Епископ', 'Светская власть', 'Инквизитор', 'Фискал');
"""

create_official_table_query = """
CREATE TABLE IF NOT EXISTS official (
 id serial PRIMARY KEY,
 person_id integer NOT NULL REFERENCES person(id) ON DELETE CASCADE,
 official_name official_name NOT NULL,
 employment_date date NOT NULL,
 fired_date date
 CHECK (fired_date IS NULL OR employment_date < fired_date)
);
"""

create_inquisition_process_table_query = """
CREATE TABLE IF NOT EXISTS inquisition_process (
 id serial PRIMARY KEY,
 start_data date NOT NULL,
 finish_data date,
 official_id integer NOT NULL REFERENCES official(id) ON DELETE RESTRICT,
 church_id integer NOT NULL REFERENCES church(id) ON DELETE RESTRICT,
 bible_id integer NOT NULL REFERENCES bible(version) ON DELETE RESTRICT,
 CHECK (finish_data IS NULL OR start_data <= finish_data)
);
"""

create_accusation_table_query = """
CREATE TABLE IF NOT EXISTS accusation_process(
	id serial PRIMARY KEY,
	start_time timestamp NOT NULL,
	finish_time timestamp,
	inquisition_process_id integer NOT NULL REFERENCES inquisition_process(id) ON DELETE CASCADE
);
"""

create_accusation_status_type_query = """
CREATE TYPE accusation_status as enum ('Ложный', 'Правдивый');
"""

create_accusation_record_table_query = """
CREATE TABLE IF NOT EXISTS accusation_record(
	id serial PRIMARY KEY,
	informer integer REFERENCES person(id) ON DELETE RESTRICT,
	bishop integer NOT NULL REFERENCES official(id) ON DELETE RESTRICT,
	accused integer NOT NULL REFERENCES person(id) ON DELETE RESTRICT,
	violation_place varchar(255),
	violation_time timestamp NOT NULL,
	description text,
	id_accusation integer NOT NULL REFERENCES accusation_process(id) ON DELETE CASCADE,
    record_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	status accusation_status DEFAULT NULL
);
"""

create_investigative_case_table_query = """
CREATE TABLE IF NOT EXISTS investigative_case (
 id serial PRIMARY KEY,
 creation_date date NOT NULL,
 closed_date date,
 CHECK (closed_date IS NULL OR creation_date <= closed_date)
);
"""

create_accusation_investigative_case_table_query = """
CREATE TABLE IF NOT EXISTS accusation_investigative_case (
 case_id integer REFERENCES investigative_case(id) ON DELETE CASCADE,
 record_id integer UNIQUE REFERENCES accusation_record(id) ON DELETE RESTRICT,
 PRIMARY KEY(case_id, record_id)
);
"""

create_punishment_table_query = """
CREATE TABLE IF NOT EXISTS punishment (
 id serial PRIMARY KEY,
 name varchar(255) NOT NULL,
 description text
);
"""

create_case_log_result_type_query = """
CREATE TYPE case_log_result as enum ('Признание вины', 'Отрицание вины');
"""

create_case_log_status_type_query = """
CREATE TYPE case_log_status as enum ('Пыточный процесс', 'Исправительная беседа', 'Наказание');
"""

create_case_log_table_query = """
CREATE TABLE IF NOT EXISTS case_log (
 id serial PRIMARY KEY,
 case_id integer NOT NULL REFERENCES investigative_case(id) ON DELETE RESTRICT,
 case_status case_log_status NOT NULL,
 principal integer NOT NULL REFERENCES official(id) ON DELETE RESTRICT,
 start_time timestamp NOT NULL,
 result case_log_result,
 prison_id integer REFERENCES prison(id) ON DELETE RESTRICT,
 finish_time timestamp,
 punishment_id integer REFERENCES punishment(id) ON DELETE RESTRICT,
 description text,
 UNIQUE(case_id, case_status),
 CHECK (finish_time IS NULL OR start_time < finish_time)
);
"""

create_violation_table_query = """
CREATE TABLE IF NOT EXISTS violation (
 commandment_id integer REFERENCES commandment(id) ON DELETE RESTRICT,
 record_id integer REFERENCES accusation_record(id) ON DELETE CASCADE,
 PRIMARY KEY(commandment_id, record_id)
);
"""

create_torture_type_table_query = """
CREATE TABLE IF NOT EXISTS torture_type (
 id serial PRIMARY KEY,
 name varchar(255) NOT NULL,
 description text
);
"""

create_torture_log_table_query = """
CREATE TABLE IF NOT EXISTS torture_log (
 case_log_id integer NOT NULL REFERENCES case_log(id) ON DELETE CASCADE,
 type_id integer NOT NULL REFERENCES torture_type(id) ON DELETE RESTRICT,
 executor integer NOT NULL REFERENCES official(id) ON DELETE RESTRICT,
 victim integer NOT NULL REFERENCES person(id) ON DELETE RESTRICT,
 PRIMARY KEY(case_log_id, type_id)
);
"""


# Creating tables
cursor.execute(create_locality_table)
cursor.execute(create_church_table)
cursor.execute(create_prison_table)
cursor.execute(create_bible_table)

# Creating tables and types
cursor.execute(create_commandment_table)
cursor.execute(create_bible_commandment_table)
cursor.execute(create_gender_type)
cursor.execute(create_person_table)

queries = [
    create_type_query,
    create_official_table_query,
    create_inquisition_process_table_query,
    create_accusation_status_type_query,
    create_accusation_table_query,
    create_accusation_record_table_query
]

queries.extend([
    create_investigative_case_table_query,
    create_accusation_investigative_case_table_query,
    create_punishment_table_query
])

queries.extend([
    create_case_log_result_type_query,
    create_case_log_status_type_query,
    create_case_log_table_query,
    create_violation_table_query,
    create_torture_type_table_query,
    create_torture_log_table_query
])

for query in queries:
    cursor.execute(query)

# Commit and close connection
connection.commit()
cursor.close()
connection.close()
