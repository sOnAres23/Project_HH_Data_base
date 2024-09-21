from typing import Any
import psycopg2


def create_database(database_name: str, params):
    """Функция для создания базы данных и таблиц работодателей и их вакансиях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR(255) not null,
                employer_area VARCHAR(255) not null,
                url VARCHAR(255),
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255),
                vacancy_area VARCHAR(255),
                salary INTEGER,    
                employer_id INTEGER REFERENCES employers(employer_id),
                employer VARCHAR(255),
                experience VARCHAR(255),
                vacancy_url VARCHAR(255)
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data_employer: list[dict[str, Any]], data_vacancies: list[dict[str, Any]],
                          database_name: str, params: dict):
    """Функция для сохранения данных о работодателях и их вакансиях в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data_employer:
            cur.execute("""
                INSERT INTO employers (employer_id, employer_name, employer_area, url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                """,
                        (employer['id'], employer['name'], employer['area']['name'], employer['alternate_url'],
                         employer['open_vacancies']))
        for vacancy in data_vacancies:
            if vacancy["salary"]["from"]:
                salary = vacancy["salary"]["from"]
            elif vacancy["salary"]["to"]:
                salary = vacancy["salary"]["to"]
            else:
                salary = 0

            cur.execute("""
                    INSERT INTO vacancies (vacancy_name, vacancy_area, salary, 
                    employer_id, employer, experience, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                        (vacancy['name'], vacancy['area']['name'], salary, vacancy['employer']['id'],
                         vacancy['employer']['name'], vacancy["experience"]["name"], vacancy['alternate_url']))

    conn.commit()
    conn.close()
