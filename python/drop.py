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

drop_queries = [
    "DROP FUNCTION IF EXISTS start_inquisition_process;",
    "DROP FUNCTION IF EXISTS finish_inquisition_process;",
    "DROP FUNCTION IF EXISTS start_accusation_process;",
    "DROP FUNCTION IF EXISTS finish_accusation_process;",
    "DROP FUNCTION IF EXISTS add_accusation_record;",
    "DROP FUNCTION IF EXISTS get_not_resolved_accusation_record;",
    "DROP FUNCTION IF EXISTS find_in_bible;",
    "DROP FUNCTION IF EXISTS read_bible;",
    "DROP FUNCTION IF EXISTS connect_commandment_with_record;",
    "DROP PROCEDURE IF EXISTS add_record_to_case;",
    "DROP FUNCTION IF EXISTS generate_cases;",
    "DROP PROCEDURE IF EXISTS handle_simple_cases;",
    "DROP PROCEDURE IF EXISTS handle_cases_with_grave_sin;",
    "DROP FUNCTION IF EXISTS get_not_resolved_cases;",
    "DROP FUNCTION IF EXISTS get_best_principal;",
    "DROP FUNCTION IF EXISTS get_best_prison;",
    "DROP FUNCTION IF EXISTS start_discussion;",
    "DROP FUNCTION IF EXISTS start_torture;",
    "DROP FUNCTION IF EXISTS make_torture_step;",
    "DROP FUNCTION IF EXISTS finish_case_log_process;",
    "DROP FUNCTION IF EXISTS assign_punishment;",
    "DROP TABLE IF EXISTS torture_log;",
    "DROP TABLE IF EXISTS torture_type;",
    "DROP TABLE IF EXISTS case_log;",
    "DROP TABLE IF EXISTS accusation_investigative_case;",
    "DROP TABLE IF EXISTS violation;",
    "DROP TABLE IF EXISTS investigative_case;",
    "DROP TABLE IF EXISTS accusation_record;",
    "DROP TABLE IF EXISTS accusation_process;",
    "DROP TABLE IF EXISTS inquisition_process;",
    "DROP TABLE IF EXISTS church;",
    "DROP TABLE IF EXISTS prison;",
    "DROP TABLE IF EXISTS bible_commandment;",
    "DROP TABLE IF EXISTS bible;",
    "DROP TABLE IF EXISTS commandment;",
    "DROP TABLE IF EXISTS official;",
    "DROP TABLE IF EXISTS punishment;",
    "DROP TYPE IF EXISTS case_log_result;",
    "DROP TABLE IF EXISTS person;",
    "DROP TABLE IF EXISTS locality;",
    "DROP TYPE IF EXISTS gender;",
    "DROP TYPE IF EXISTS case_log_status;",
    "DROP TYPE IF EXISTS official_name;",
    "DROP TYPE IF EXISTS accusation_status",
]

for query in drop_queries:
    cursor.execute(query)
    print(query)

# Commit the changes to the database.
connection.commit()
cursor.close()
connection.close()
