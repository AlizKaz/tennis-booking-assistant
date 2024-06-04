import datetime as datetime

import pytz
from termcolor import colored

from gpt_service import init_client


def init():
    gpt_model = "gpt-4o"

    tools = get_tools()

    date_message_content = get_date_message()

    messages = []
    system_message = f"You are an assistant in helping me book a tennis court. " \
                     "You are able to have a conversation or perform the tasks specified in the tools. " \
                     "The user must specify if a task from one of the tools should be called, not by AI guessing. " \
                     "Please ask the user for follow up question if you are uncertain." \
                     f" {date_message_content}. Don't make " \
                     "assumptions about what values to plug into functions. Ask " \
                     "for clarification only if a user request is ambiguous."
    messages.append({"role": "system", "content": system_message})
    # messages.append({"role": "user", "content": "Book a court with me and Negar on Friday 31 May at 4pm"})
    # messages.append({"role": "user", "content": "Book a court with me and Negar on upcoming Friday at 4pm"})
    # chat_response = chat_completion_request(
    #     messages, tools=tools, tool_choice="auto"
    # )
    # tool_choice={"type": "function", "function": {"name": "book_tennis_court"}
    # assistant_message = chat_response.choices[0].message
    # messages.append({"role": assistant_message.role, "content": assistant_message.content})
    # assistant_message
    # pretty_print_conversation(messages)

    # messages.append({"role": "user", "content": "I wanna play next Thursday at 6pm with Alejandro."})
    # chat_response = chat_completion_request(
    #     messages, tools=tools, tool_choice="auto"
    # )
    # tool_choice={"type": "function", "function": {"name": "book_tennis_court"}
    # assistant_message = chat_response.choices[0].message
    # messages.append({"role": assistant_message.role, "content": assistant_message.content})
    # assistant_message
    # pretty_print_conversation(messages)
    return tools, gpt_model, system_message


def get_tools():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "book_tennis_court",
                "description": "book a tennis court with a partner at a specified data nad time",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "partner_name": {
                            "type": "string",
                            "description": "Name of the partner",
                        },
                        "date": {
                            "type": "string",
                            # "enum": ["celsius", "fahrenheit"],
                            "description": "The date that we are going to play",
                        },
                        "time": {
                            "type": "string",
                            # "enum": ["6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM",
                            #          "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM"],
                            "description": "The time that we are going to play. formatted as HH:MM:SS",
                        }
                    },
                    "required": ["partner_name", "date", "time"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_availability",
                "description": "Get all the court availabilities for a date with a player",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "the date formatted YYYY-MM-DD",
                        },
                        "participant_name": {
                            "type": "string",
                            "description": "the first name and last name of the participant. First name and last name "
                                           "should be delimited by space",
                        },
                    },
                    "required": ["date", "participant_name"]
                },
            }
        },
        # {
        #     "type": "function",
        #     "function": {
        #         "name": "get_n_day_weather_forecast",
        #         "description": "Get an N-day weather forecast",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "location": {
        #                     "type": "string",
        #                     "description": "The city and state, e.g. San Francisco, CA",
        #                 },
        #                 "format": {
        #                     "type": "string",
        #                     "enum": ["celsius", "fahrenheit"],
        #                     "description": "The temperature unit to use. Infer this from the users location.",
        #                 },
        #                 "num_days": {
        #                     "type": "integer",
        #                     "description": "The number of days to forecast",
        #                 }
        #             },
        #             "required": ["location", "format", "num_days"]
        #         },
        #     }
        # },
    ]

    return tools


# response = client.chat.completions.create(
#     model=MODEL,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]
# )


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))


def get_date_message():
    my_locale = pytz.timezone('Canada/Eastern')
    now_datetime = datetime.datetime.now(my_locale)
    now_of_year = now_datetime.strftime("%Y")
    now_of_month = now_datetime.strftime("%m")
    now_of_day = now_datetime.strftime("%d")
    now_of_time = now_datetime.strftime("%H:%M")
    day_of_week = now_datetime.strftime('%A')
    month_name = now_datetime.strftime("%B")
    date_message_content = f"Today is {day_of_week}, the year {now_of_year}, month is {month_name}, and date is " \
                           f"{now_of_day}. " \
        # f"The current time is {now_of_time}."
    print(date_message_content)
    return date_message_content
