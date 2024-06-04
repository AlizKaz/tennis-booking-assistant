import requests

search_api_url = "https://10xtoronto.clubautomation.com/api/reservation/search"
auth_api_url = "https://10xtoronto.clubautomation.com/api/v4/auth"
player_lookup_url = "https://10xtoronto.clubautomation.com/api/account/lookup"
init_cancel_reservation_url = "https://10xtoronto.clubautomation.com/api/reservation/cancel-reservation"
confirm_cancel_reservation_url = "https://10xtoronto.clubautomation.com/api/reservation/cancel-reservation"
user_activities_url = "https://10xtoronto.clubautomation.com/api/v4/user-activities"
init_reserve_url = "https://10xtoronto.clubautomation.com/api/reservation/reserve"
confirm_reserve_url = "https://10xtoronto.clubautomation.com/api/reservation/reserve"
reserver_info_url = "https://10xtoronto.clubautomation.com/api/reservation/reserve-info"

# ['Invalid Access Token', 'The access token is missing or malformed.']
def get_reserve_info(api_url, access_token, user_id, event_id, date):
    params = {
        'access_token': access_token,
        'userId': user_id,
        'eventId': event_id,
        'date': date,
    }

    r = requests.get(api_url, params=params)
    if r.json()['success']:
        return True, r.json()['data']
    else:
        error = r.json()['error']
        return False, error


def player_lookup(api_url, access_token, player_name):
    params = {
        'access_token': access_token,
        'text': player_name,
    }

    r = requests.get(api_url, params=params)
    if r.json()['success']:
        return True, r.json()['data'][0]['id']
    else:
        error = r.json()['error']
        return False, error


def confirm_reserve(api_url, access_token, service_location_id, resource_id, ball_machine,
                    date, start_time, duration, host_id, participant_ids):
    payload = {
        'access_token': access_token,
        'serviceLocationId': service_location_id,
        'resourceId': resource_id,
        'ballMachine': ball_machine,
        'date': date,
        'startTime': start_time,
        'duration': duration,
        'hostId': host_id,
        'participantIds[]': [participant_ids]
    }

    r = requests.post(api_url, data=payload)
    if r.json()['success']:
        if r.json()['data']['isSaved']:
            return True, r.json()['data']['id']
        else:
            return False
    else:
        error = r.json()['error']
        return False, error


# service_location_id for example indoor
# resource_id --> court id
def init_reserve(api_url, access_token, service_location_id,
                 resource_id, ball_machine, date, start_time,
                 duration: int, host_id, participant_ids):
    params = {
        'access_token': access_token,
        'serviceLocationId': service_location_id,
        'resourceId': resource_id,
        'ballMachine': ball_machine,
        'date': date,
        'startTime': start_time,
        'duration': duration,
        'hostId': host_id,
        'participantIds[]': participant_ids
    }

    r = requests.get(api_url, params=params)
    if r.json()['success']:
        return True, r.json()['data']
    else:
        return False, r.json()['error']


def user_activities(api_url, access_token, user_id, date):
    params = {
        'access_token': access_token,
        'user_id': user_id,
        'date': date,
    }

    r = requests.get(api_url, params=params)
    if r.json()['success']:
        # {
        #     "data": [
        #         {
        #             "eventId": 122261,
        #             "startTime": "8:00 PM",
        #             "department": "Tennis",
        #             "entity": "10XTO",
        #             "duration": "1 HR",
        #             "instructor": null,
        #             "itemName": null,
        #             "lessonTerminology": null,
        #             "eventType": "reservation",
        #             "canBeCanceled": true,
        #             "resourcesInfo": "Court 4",
        #             "attendee": "",
        #             "scheduleId": null
        #         }
        #     ],
        #     "success": true,
        #     "error": null,
        #     "formErrors": null
        # }
        return True, r.json()['data']
    else:
        error = r.json()['error']
        return False, error


def confirm_cancel_reservation(api_url, access_token, event_id):
    payload = {
        'access_token': access_token,
        'eventId': event_id,
    }

    r = requests.post(api_url, data=payload)
    # {
    #   "data": {
    #     "reservationHasBeenCanceled": true
    #   },
    #   "success": true,
    #   "error": null,
    #   "formErrors": null
    # }
    if r.json()['success']:
        return True, r.json()['data']['reservationHasBeenCanceled']
    else:
        error = r.json()['error']
        return False, error


def init_cancel_reservation(api_url, access_token, event_id):
    params = {
        'access_token': access_token,
        'eventId': event_id
    }

    r = requests.get(api_url, params=params)
    if r.json()['success']:
        # {
        #   "data": {
        #     "isCancellationPeriod": false,
        #     "cancellationFeeType": null,
        #     "feeValue": null
        #   },
        #   "success": true,
        #   "error": null,
        #   "formErrors": null
        # }
        return True, r.json()['data']
    else:
        error = r.json()['error']
        return False, error


def search_availability(api_url, access_token, date, host_id, participant_id, start_time_from="06:00:00",
                        start_time_to="22:00:00"):
    params = {
        'access_token': access_token,
        'serviceId': 2,
        'locationIds[]': [1],
        'date': date,
        'duration': 60,
        'hostId': host_id,
        'participantIds[]': [participant_id],
        'startTimeFrom': start_time_from,
        'startTimeTo': start_time_to,
    }

    r = requests.get(api_url, params=params)

    if r.json()['success']:
        return True, r.json()['data']
    else:
        error = r.json()['error']
        return False, error


def login(api_url, username, password):
    payload = {
        'username': username,
        'password': password,
        'client_id': '0QqRwc8J9YlnGaVFRhDjohDjD6evGh7Z',
        'client_secret': 'xSYge0xNo61llBZAvEg2JGhnzJg4FiA5',
        'scope': "private"
    }

    r = requests.post(api_url, data=payload)

    if r.json()['success']:
        return True, r.json()['data']
    else:
        return False, r.json()['error']


def search_availabilities(access_token, date, host_name, participant_name):
    success, host_id = player_lookup(player_lookup_url, access_token=access_token, player_name=host_name)
    if not success:
        return f"unable to find host id for host name: {host_name}"

    success, participant_id = player_lookup(api_url=player_lookup_url, access_token=access_token, player_name=participant_name)
    if not success:
        return f"unable to find host id for participant name: {participant_name}"

    availability_result = search_availability(search_api_url, access_token=access_token, date=date,
                                              host_id=host_id,
                                              participant_id=participant_id)
    if availability_result[0]:
        print(availability_result[1])
    else:
        print(f'unexpected error. error: {availability_result[1]}')
        raise Exception(f'unexpected error. error: {availability_result[1]}')
    return availability_result[1]


def next_hour(time_str):
    # Split the input string into hours, minutes, and seconds
    hh, mm, ss = map(int, time_str.split(':'))

    # Increment the hour by 1
    hh += 1

    # If the hour is 24, reset it to 0 (24-hour format)
    if hh == 24:
        hh = 0

    # Format the new time as "HH:MM:SS"
    next_time_str = f"{hh:02}:{mm:02}:{ss:02}"

    return next_time_str


def to_text_get_reserve_info(reserve_info):
    resource_title = reserve_info['resourceTitle']
    host = reserve_info['host']
    partner_name = reserve_info['participants'][0]['name']
    court = reserve_info['courtType']
    location = reserve_info['location']
    date = reserve_info['date']
    time = reserve_info['time']

    text = f"Just booked a {resource_title} for {host} and {partner_name} on {court} at {location} on {date} at {time}"
    return text


def book_tennis_court(access_token, host_name, partner_name, date, time):
    if not access_token:
        success, login_result = login(api_url=auth_api_url, username=username, password=password)
        if not success:
            return f"unable to login due to {login_result}"
        else:
            access_token = login_result['token']
    success, partner_id = player_lookup(player_lookup_url, access_token=access_token, player_name=partner_name)
    if not success:
        return f"unable to find partner id for partner name: {partner_name}"
    print(f"partner id found: {partner_id}")
    success, host_id = player_lookup(player_lookup_url, access_token=access_token, player_name=host_name)
    if not success:
        return f"unable to find host id for host name: {host_name}"

    print(f"host id found: {host_id}")
    successful, availabilities = search_availability(search_api_url, access_token=access_token, date=date,
                                                     host_id=host_id,
                                                     participant_id=partner_id, start_time_from=time,
                                                     start_time_to=next_hour(time))
    if not successful:
        return f"unable to book a court. the reason might be {availabilities}"
    elif len(availabilities) == 0:
        return f"there is no court available on {date} at {time}"

    service_location_id = availabilities[0]['serviceLocation']['id']
    resource_id = availabilities[0]['resource']['id']
    result = confirm_reserve(confirm_reserve_url, access_token=access_token, service_location_id=service_location_id,
                             resource_id=resource_id,
                             ball_machine=0, date=date, start_time=time, duration=60, host_id=host_id,
                             participant_ids=partner_id)
    if result[0]:
        event_id = result[1]
        result = get_reserve_info(reserver_info_url, access_token=access_token, user_id=host_id, event_id=event_id,
                                  date=date)
        if result[0]:
            return to_text_get_reserve_info(result[1])
        else:
            return f"unable to book a court. the reason might be {result[1]}"
    else:
        return f"unable to book a court. the reason might be {result[1]}"
