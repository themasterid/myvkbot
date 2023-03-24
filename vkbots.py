# my vk bot
from vk_api.longpoll import VkLongPoll, VkEventType
import vk, vk_api
import requests
from secret import mytoken
from city_kz import listkz


def make_url(city):
    return f'http://wttr.in/{city}'

def make_parameters():
    return {
        'format': 2,
        'M': ''}

def what_weather(city):
    try:
        response = requests.get(make_url(city), params=make_parameters())
    except requests.ConnectionError:
        return '<сетевая ошибка>'
    if response.status_code == 200:
        return response.text
    else:
        return '<ошибка на сервере погоды>'

def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


vk = vk_api.VkApi(token=mytoken)
longpoll = VkLongPoll(vk)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text
        write_msg(event.user_id, 'Привет :)')
        if request in listkz:
            otvet = f'Погода в городе - {request}' + '\n' + what_weather(request)
        else:
            otvet = 'Пожалуйста введите название крупного города в Казахстане, например, Алматы'
        write_msg(event.user_id, otvet)

bot.polling(none_stop=True)
