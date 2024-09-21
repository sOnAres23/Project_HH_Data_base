import psycopg2


class DBManager:
    """Класс для взаимодействия с базой данных"""
    def __init__(self, db_name: str, params_db: dict):
        self.db_name = db_name  # Получаем имя базы данных
        self.params_db = params_db  # Создаем параметры для подключения

    def get_companies_and_vacancies_count(self):
        """Метод, который выводит список всех компаний и количество вакансий у каждой компании"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # подключение к базе данных

        with conn.cursor() as cur:
            cur.execute("""
                        SELECT employer_name, COUNT(vacancies.employer_id)
                        FROM employers
                        INNER JOIN vacancies USING (employer_id)
                        GROUP BY employer_name
                        ORDER BY employer_name
                        """)
            result = cur.fetchall()

        conn.close()

        return result

    def get_all_vacancies(self):
        """Метод, который выводит список вакансий со всеми данными"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # подключение к базе данных

        with conn.cursor() as cur:
            cur.execute("""
                        SELECT v.employer, v.vacancy_name, v.salary, v.experience, v.vacancy_url
                        FROM vacancies v
                        INNER JOIN employers e USING (employer_id)
                        ORDER BY v.salary DESC
                        """)
            result = cur.fetchall()

        conn.close()

        return result

    def get_avg_salary(self):
        """Метод, который получает среднюю зарплату по вакансиям среди всех компаний"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # подключение к базе данных

        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary) FROM vacancies""")
            result = cur.fetchall()

        conn.close()

        average = str(result[0]).split("'")[1]

        avg_salary = round(float(average), 2)

        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """Метод, который выводит список вакансий, у которых зарплата выше средней зарплаты"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # подключение к базе данных

        with conn.cursor() as cur:
            cur.execute("""
                        SELECT * FROM vacancies
                        WHERE salary >= (SELECT AVG(salary) FROM vacancies)
                        ORDER BY salary DESC
                        """)
            result = cur.fetchall()

        conn.close()

        return result

    def get_vacancies_with_keyword(self, keyword):
        """Метод, который выводит список всех вакансий по ключевому слову в названии"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # подключение к базе данных

        with conn.cursor() as cur:
            cur.execute(f"""
                        SELECT * FROM vacancies
                        WHERE vacancy_name LIKE '%{keyword}%'
                        """)
            result = cur.fetchall()

        conn.close()

        return result
