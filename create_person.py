# import psycopg2
import random
from datetime import timedelta, datetime

# # Modify these variables according to your PostgreSQL configuration.
# DATABASE = "YourDatabaseName"
# USERNAME = "YourUsername"
# PASSWORD = "YourPassword"
# HOST = "localhost"
# PORT = "5432"

# connection = psycopg2.connect(
#     dbname=DATABASE,
#     user=USERNAME,
#     password=PASSWORD,
#     host=HOST,
#     port=PORT
# )
# cursor = connection.cursor()

# # Use this function to generate date_between
# def random_date(start, end):
#     return (start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))).strftime('%Y-%m-%d')

# def insert_person(name, surname, birth_date, person_gender):
#     query = "INSERT INTO person (name, surname, birth_date, person_gender) VALUES (%s, %s, %s, %s);"
#     data = (name, surname, birth_date, person_gender)
#     cursor.execute(query, data)
#     connection.commit()

# # Define start and end date range for birthdate
# start = datetime(1400, 1, 1)
# end = datetime(1420, 12, 31)

russian_male_names = [
    ["Александр", "M"],
    ["Сергей", "M"],
    ["Владимир", "M"],
    ["Иван", "M"],
    ["Андрей", "M"],
    ["Михаил", "M"],
    ["Дмитрий", "M"],
    ["Николай", "M"],
    ["Алексей", "M"],
    ["Максим", "M"],
    ["Евгений", "M"],
    ["Артем", "M"],
    ["Роман", "M"],
    ["Олег", "M"],
    ["Кирилл", "M"],
]

russian_male_surnames = [
    ["Иванов", "M"],
    ["Петров", "M"],
    ["Сидоров", "M"],
    ["Кузнецов", "M"],
    ["Смирнов", "M"],
    ["Васильев", "M"],
    ["Зайцев", "M"],
    ["Павлов", "M"],
    ["Соколов", "M"],
    ["Попов", "M"],
    ["Лебедев", "M"],
    ["Козлов", "M"],
    ["Новиков", "M"],
    ["Морозов", "M"],
    ["Поляков", "M"],
]

# # Loop to generate SQL queries for inserting records
# for i in range(25000):
#     gender = random.choice(['M', 'F'])
#     name = random.choice(russian_male_names)
#     surname = random.choice(russian_male_surnames)
#     birth_date = random_date(start, end)

#     # SQL query to insert data
#     query = f"INSERT INTO person (name, surname, birth_date, person_gender) VALUES ('{name}', '{surname}', '{birth_date}', '{gender}');"

#     # print(query)
#     insert_person(*person)

russian_female_names = [
    ["Анна", "F"],
    ["Елена", "F"],
    ["Татьяна", "F"],
    ["Ольга", "F"],
    ["Ирина", "F"],
    ["Екатерина", "F"],
    ["Марина", "F"],
    ["Наталья", "F"],
    ["Тамара", "F"],
    ["Юлия", "F"],
    ["Виктория", "F"],
    ["Светлана", "F"],
    ["Оксана", "F"],
    ["Анастасия", "F"],
    ["Алена", "F"],
]

russian_female_surnames = [
    ["Иванова", "F"],
    ["Петрова", "F"],
    ["Сидорова", "F"],
    ["Кузнецова", "F"],
    ["Смирнова", "F"],
    ["Васильева", "F"],
    ["Зайцева", "F"],
    ["Павлова", "F"],
    ["Соколова", "F"],
    ["Попова", "F"],
    ["Лебедева", "F"],
    ["Козлова", "F"],
    ["Новикова", "F"],
    ["Морозова", "F"],
    ["Полякова", "F"],
]

# cursor.close()
# connection.close()
