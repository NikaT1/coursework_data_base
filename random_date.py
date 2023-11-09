import datetime
import random
# from datetime import date


def random_date(year_start, year_end):
    return datetime.date(
        random.randint(year_start, year_end),
        random.randint(1, 12),
        random.randint(1, 28)  # Using 28 to avoid issues with leap years and months with 30 or 31 days
    )

for i in range(30):
    print(random_date(1400, 1420).strftime('%Y, %m, %d'))

for i in range(8):
    print(random_date(1488, 1488).strftime('%Y, %m, %d'))