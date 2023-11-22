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
    "DROP FUNCTION start_inquisition_process;",
    "DROP FUNCTION finish_inquisition_process;",
    "DROP FUNCTION start_accusation_process;",
    "DROP FUNCTION finish_accusation_process;",
    "DROP FUNCTION add_accusation_record;",
    "DROP PROCEDURE get_not_resolved_accusation_record;",
    "DROP PROCEDURE find_in_bible;",
    "DROP PROCEDURE connect_commandment_with_record;",
    "DROP PROCEDURE add_record_to_case;",
    "DROP PROCEDURE generate_cases;",
    "DROP PROCEDURE handle_simple_cases;",
    "DROP PROCEDURE handle_cases_with_grave_sin;",
    "DROP PROCEDURE get_not_resolved_cases;",
    "DROP FUNCTION get_best_principal;",
    "DROP FUNCTION get_best_prison;",
    "DROP FUNCTION start_discussion;",
    "DROP FUNCTION start_torture;",
    "DROP FUNCTION make_torture_step;",
    "DROP FUNCTION finish_case_log_process;",
    "DROP FUNCTION assign_punishment;",
    "DROP TABLE torture_log;",
    "DROP TABLE torture_type;",
    "DROP TABLE case_log;",
    "DROP TABLE accusation_investigative_case;",
    "DROP TABLE violation;",
    "DROP TABLE investigative_case;",
    "DROP TABLE accusation_record;",
    "DROP TABLE accusation_process;",
    "DROP TABLE inquisition_process;",
    "DROP TABLE church;",
    "DROP TABLE prison;",
    "DROP TABLE bible_commandment;",
    "DROP TABLE bible;",
    "DROP TABLE commandment;",
    "DROP TABLE locality;",
    "DROP TABLE official;",
    "DROP TABLE punishment;",
    "DROP TABLE person;",
    "DROP TYPE gender;",
    "DROP TYPE case_log_result;",
    "DROP TYPE case_log_status;",
    "DROP TYPE official_name;",
    "DROP TYPE accusation_status",
]

for query in drop_queries:
    cursor.execute(query)

# Commit the changes to the database.
connection.commit()
cursor.close()
connection.close()
