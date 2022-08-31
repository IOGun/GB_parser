#2. Работа будет состоять с недокументированным API. Нужно ввести релевантный запрос на сайте
# https://www.delivery-club.ru/search
#(а) из предложенных точек с помощью API найти долю (в %) с бесплатной и платной доставкой.
# Для каждой категории рассчитать среднюю минимальную стоимость заказа.

#(б) для каждой из категорий из пункта (а) рассчитать долю (в %) магазинов и ресторанов

import requests
from pprint import pprint

url = 'https://api.delivery-club.ru/api1.2/vendors/search'

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

params = {
    'latitude' : 55.80186,
    'longitude': 49.260556,
    'query': 'манты'
}

def free_and_pay(vendors, free, pay):
    if free == 0:
        percent_free = 0
    else:
        percent_free = 100/(vendors/free)

    if pay == 0:
        percent_pay = 0
    else:
        percent_pay = 100/(vendors/pay)

    print(f"""Всего вендоров {vendors} из них:
        с бесплатной доставкой - {free} ({percent_free})%, 
        с платной доставкой - {pay} ({percent_pay})%.\n"""
          )

def shop_and_restaurant(vendors, shop, restaurant):
    another = vendors-shop-restaurant

    if shop == 0:
        percent_shop = 0
    else:
        percent_shop = 100/(vendors/shop)

    if restaurant == 0:
        percent_restaurant = 0
    else:
        percent_restaurant = 100/(vendors/restaurant)

    print(f"""Всего вендоров {vendors} из них:
        магазинов - {shop} ({percent_shop})%, 
        ресторанов - {restaurant} ({percent_restaurant})%, 
        другое - {another}. \n"""
          )




try:
    response = requests.get(url = url, headers = headers, params = params )
except requests.ConnectionError:
    print('Ошибка подключения.')
    exit()


vendors = response.json()['vendors']

total_min_order_price = 0

pay_delivery = 0
free_delivery = 0

shop = 0
restaurant = 0
another = 0

amount_vendors = len(vendors)

for vendor in vendors:
    #print(vendor['name'])
    total_min_order_price += vendor['delivery']['minOrderPrice']['value']
    if vendor['categoryId'] == 1:
        restaurant += 1
    elif vendor['categoryId'] == 5:
        shop += 1
    else:
        another += 1
    if vendor['delivery']['price']['value'] == 0:
        free_delivery += 1
    else:
        pay_delivery += 1

print(f"Средняя минимальная стоимость заказа в категории '{params['query']}': {total_min_order_price/amount_vendors} \n")

free_and_pay(amount_vendors, free_delivery, pay_delivery)

shop_and_restaurant(amount_vendors, shop, restaurant)

