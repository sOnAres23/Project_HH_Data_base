from abc import ABC, abstractmethod

import requests


class BaseHeadHunterAPI(ABC):
    """Абстрактный класс, для класса получения API с hh.ru"""
    pass

    @abstractmethod
    def get_employers(self):
        pass


class HeadHunterAPI(BaseHeadHunterAPI):
    """
    Класс для работы с API HeadHunter.
    Наследуется от класса BaseHeadHunterAPI, который является родительским.
    """
    def __init__(self):
        self.__url = 'https://api.hh.ru/'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = None
        self.employers = [3529, 2180, 9498112, 3776, 9498120, 78638, 23427, 3127, 4181, 80]

    def get_employers(self):
        """Метод получения 10-ти работодателей, у которых есть открытые вакансии"""
        emp_params = {
            "sort_by": "by_vacancies_open"
        }
        employers = []
        for employer_id in self.employers:
            emp_url = f"{self.__url}employers/{employer_id}"
            employer_info = requests.get(emp_url, headers=self.__headers, params=emp_params).json()
            employers.append(employer_info)

        return employers

    def get_vacancies(self, num_vac):
        """Метод получения n-ного количества вакансий для каждого заданного работодателя"""
        vac_url = f"{self.__url}vacancies"
        vacancies = []
        for emp in self.employers:
            vacancy_params = {
                "employer_id": emp,
                "per_page": num_vac,
                "only_with_salary": True
            }
            response = requests.get(vac_url, headers=self.__headers, params=vacancy_params)
            if response.status_code == 200:
                vac = response.json()["items"]
                vacancies.extend(vac)
            else:
                raise Exception(f"Ошибка {response.status_code}: {response.text}")
        return vacancies
