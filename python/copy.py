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

# List of \copy commands
copy_commands = [
    "\\copy locality from '/home/studs/s336768/backup/locality' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/church' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/prison' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/bible' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/commandment' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/bible_commandment' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/person' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/official' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/inquisition_process' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/accusation_process' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/accusation_record' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/punishment' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/violation' delimiter ',' csv header",
    "\\copy locality from '/home/studs/s336768/backup/torture_type' delimiter ',' csv header"
]

# Execute the \copy commands
for copy_command in copy_commands:
    cursor.execute(copy_command)

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()
