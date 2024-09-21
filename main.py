from src.config import config
from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.utils import create_database, save_data_to_database


def main():
    company_in_db = ['Сбербанк', 'Ozon',
                     'Яндекс Крауд', 'МТС',
                     'Яндекс для бизнеса', 'Т-Банк',
                     'РЖД', 'Мегафон',
                     'ВТБ', 'Альфа-банк']

    print("\nДобрый день!\n\nВы можете посмотреть вакансии по следующим компаниям:")
    for i, vacancy in enumerate(company_in_db):
        print(i + 1, vacancy)

    params = config()  # конфигурация параметров для DB

    employers = HeadHunterAPI().get_employers()  # получаем работодателей

    answer_num = int(input("\nВведите количество вакансий, которое хотите получить по каждой компании: "))
    vacancies = HeadHunterAPI().get_vacancies(num_vac=answer_num)  # получаем вакансии

    create_database('head_hunter_db', params)

    save_data_to_database(employers, vacancies, 'head_hunter_db', params)

    db_interaction = DBManager('head_hunter_db', params)

    user_enter = input("""\nВыберите действие, введя цифру:
    1. Получить количество вакансий по каждой компании?
    2. Получить все вакансии по каждой компании?
    3. Получить среднюю зарплату по вакансиям среди всех компаний?
    4. Вывести вакансии, у которых зарплата больше чем средняя з/п всех вакансий?
    5. Вывести вакансии по ключевому слову в названии вакансии?\n
    """)
    if user_enter == "1":
        result = db_interaction.get_companies_and_vacancies_count()
        for i, res in enumerate(result):
            print(i + 1, f"{res[0]} - {res[1]} вакансий.")

    elif user_enter == "2":
        result = db_interaction.get_all_vacancies()
        for i, res in enumerate(result):
            print(i + 1, f"Компания: {res[0]}, Вакансия: {res[1]}, Зарплата: {res[2]} руб., "
                  f"Опыт работы: {res[3]} Ссылка на вакансию: {res[4]}")

    elif user_enter == "3":
        print(f"Средняя зарплата составляет: {db_interaction.get_avg_salary()}")

    elif user_enter == "4":
        result = db_interaction.get_vacancies_with_higher_salary()
        for i, res in enumerate(result):
            print(i + 1, f"{res[1]}, Город: {res[2]}, Зарплата: {res[3]} руб., Ссылка на вакансию: {res[7]}")

    elif user_enter == "5":
        keyword = input("Введите ключевое слово: \n")
        result = db_interaction.get_vacancies_with_keyword(f"{keyword}")

        for i, res in enumerate(result):
            print(i + 1, f"{res[1]}, Город: {res[2]}, Зарплата: {res[3]} руб., Ссылка на вакансию: {res[7]}")


if __name__ == "__main__":
    main()
