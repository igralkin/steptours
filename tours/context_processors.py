
def departures_data(request) -> dict:
    departures_links = {
            "msk": "Из Москвы",
            "spb": "Из Петербурга",
            "nsk": "Из Новосибирска",
            "ekb": "Из Екатеринбурга",
            "kazan": "Из Казани"
    }
    return {
        'departures_links': departures_links
    }
