from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
import random


def custom_handler400(request, exception):
    # Call when SuspiciousOperation raised
    return HttpResponseBadRequest('Неверный запрос!')


def custom_handler403(request, exception):
    # Call when PermissionDenied raised
    return HttpResponseForbidden('Доступ запрещен!')


def custom_handler404(request, exception):
    # Call when Http404 raised
    # Перезаписывается в tour_view и departure_view
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')


def main_view(request):
    from .mock_data import tours, departures
    title = "Stepik Travel"
    subtitle = "Для тех, кого отвлекают дома"
    description = "Лучшие направления, где никто не будет вам мешать сидеть на берегу и изучать программирование," \
                  " дизайн, разработку игр и управление продуктами"
    tours = dict(random.sample(tours.items(), 6))
    context_data = {
                    'title': title,
                    'subtitle': subtitle,
                    'description': description,
                    'tours_data': tours,
                    'departures': departures
                    }
    return render(request, 'tours/index.html', context=context_data)


def departure_view(request, departure):
    from .mock_data import tours, departures

    try:
        departure_data = departures[departure]

        # Отфильтровываем нужные туры
        tours_data = {}
        num_tours = 0
        prices = []
        nights = []
        for k, tour in tours.items():
            if tour['departure'] == departure:
                tours_data[k] = tour

                # Определяем вилку цен
                prices.append(tour['price'])

                # Определяем интервал ночей
                nights.append(tour['nights'])

                num_tours += 1
    except KeyError:
        raise Http404(f"Направление {departure} не найдено")

    return render(request, 'tours/departure.html', context={
        'tours': tours_data,
        'departure': departure_data,
        'max_nights': max(nights),
        'min_nights': min(nights),
        'max_price': max(prices),
        'min_price': min(prices),
        'num_tours': num_tours
    })


def tour_view(request, tour_id):
    from .mock_data import tours, departures
    try:
        tour = tours[tour_id]
        tour['departure_text'] = departures[tour['departure']]
        tour['stars_text'] = '★'*int(tour['stars'])
    except KeyError:
        raise Http404(f"Тур с номером {tour_id} не найден")

    return render(request, 'tours/tour.html', context={
        'tour': tour
    })
