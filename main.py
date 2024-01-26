import requests
import threading


print(f'{"-" * 50}')
city = input(f'Enter the city you are interested in - ')


class Connection(threading.Thread):
    url_cities = 'https://countriesnow.space/api/v0.1/countries/population/cities'
    url_currency = 'https://countriesnow.space/api/v0.1/countries/currency'

    def __init__(self, num_thread: int, flag: int) -> None:
        super().__init__()
        self.num_thread = num_thread
        self.url = self.conn_request_flag(flag)
        self.url_get_answer = self.conn_request()
        if self.url_get_answer is not False:
            if self.conn_request_response_status():
                self.answer_json = self.getting_conn_request()
            else:
                output_answer(f'System Error - conn_request_response_status()')
                exit()
        else:
            output_answer(f'System Error - url_get_answer is not False')
            exit()

    def conn_request(self):
        try:
            return requests.get(self.url)
        except Exception as e:
            return False

    def conn_request_flag(self, flag: int) -> str:
        return self.url_cities if flag else self.url_currency

    def conn_request_response_status(self):
        if 200 <= self.url_get_answer.status_code <= 299:
            return True
        else:
            return False

    def getting_conn_request(self):
        if type(self.url_get_answer.json()) is str:
            output_answer(f'System Error - getting_conn_request()')
            exit()
        return self.url_get_answer.json()


class Search:
    def __init__(self, find_city, connect_cities, connect_currency):
        self.find_city = find_city
        self.search_cities = connect_cities.answer_json['data']
        self.search_currency = connect_currency.answer_json['data']
        self.answer = self.find_answer_in_request()
        output_answer(self.assign_answer_variable())

    def find_answer_in_request(self):
        answer = list()
        for item in self.search_cities:
            if item['city'].upper().startswith(self.find_city.upper()):
                answer.append([item['city'], item['country'], item['populationCounts'][0]['value']])
        for item in self.search_currency:
            for country in answer:
                if country[1].upper().startswith(item['name'].upper()):
                    country.append(item['currency'])
        if not answer:
            answer.append(f'{self.find_city}\nInvalid city name: {self.find_city}')
        return answer

    def assign_answer_variable(self):
        result = list()
        for item in self.answer:
            if type(item) is list:
                result.append(f'City - {item[0]}\nCountry - {item[1]}\nCurrency - {item[3]}\nPopulation - {item[2]} people')
            else:
                result.append(f'City "{self.find_city}" - not found\nInvalid city name: {self.find_city}')
        return result

def output_answer(result):
    print('-' * 50)
    if type(result) is str:
        print(result)
    else:
        for item in result:
            print(item)
    print('-' * 50)
    return None


ObjCities = Connection(1, 1)
ObjCities.start()
ObjCurrency = Connection(2, 0)
ObjCurrency.start()
ObjSearch = Search(city, ObjCities, ObjCurrency)