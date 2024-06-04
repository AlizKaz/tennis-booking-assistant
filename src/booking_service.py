import json

import booking_api


def process_gpt_response(response, access_token, host_name):
    # TODO: check out this reason
    # chat_response.choices[0].finish_reason

    if response.content:
        result = response.content
        return result
    elif response.tool_calls:
        function = response.tool_calls[0].function
        function_call = function.name
        function_call += "("
        arguments = json.loads(function.arguments)

        for arg_name, arg_value in arguments.items():
            function_call += arg_name + "=" + arg_value + ","

        function_call += ")"
        print(f"function_call : {function_call}")

        if function.name.startswith("search_availability"):
            date = arguments['date']
            availabilities = booking_api.search_availabilities(access_token=access_token, date=date, host_name=host_name,
                                                               participant_name=arguments['participant_name'])
            result = to_text(availabilities=availabilities, date=date)
            return result
        elif function.name.startswith("book_tennis_court"):
            print(f"time: {arguments['time']}")
            result = booking_api.book_tennis_court(access_token="", host_name=host_name,
                                                   partner_name=arguments['partner_name'],
                                                   date=arguments['date'], time=arguments['time'])

            return result


def to_text(date, availabilities):
    if len(availabilities) == 0:
        return f"there are no open slots for {date}"
    text = f"the followings are the open slots for date\n"
    for avail in availabilities:
        text += avail['startTime'] + ","
    return text
