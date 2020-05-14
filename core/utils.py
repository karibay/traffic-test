import requests


def personal_number_is_ie(personal_number):
    url = f'https://stat.gov.kz/api/juridical/gov/?bin={personal_number}&lang=ru'
    response = requests.get(url, verify=False)
    if not response:
        raise Exception()
    return response.json()['success']
