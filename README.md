# Tennis Booking Assistant

Welcome to the **Tennis Booking Assistant** repository! This project is designed to help you book tennis courts at your 10XTO with ease and efficiency.

## Features

- Automates the process of booking tennis courts at 10XTO using OpenAI APIs.
- Ensures you never miss an available slot.
- Written in Python for simplicity and flexibility.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- OpenAI Project API Key (Get it from here if you don't have one already: https://platform.openai.com/api-keys)
- Python 3.11 or later installed on your machine.
- [Pipenv](https://pipenv.pypa.io/en/latest/) installed for managing dependencies. 

## Installation

Follow these steps to set up your environment and get the code running:

1. **Clone the repository:**

    ```bash
    $ git clone https://github.com/yourusername/tennis-booking-assistant.git
    $ cd tennis-booking-assistant
    ```
   
2. **Set up the environment variables:**

   Create a `.env` file in the root directory of the project and add the following lines, replacing the placeholder values with your actual information:

   ```env
   OPENAI_API_KEY_BOOKING_PROJECT=<YOUR_OPENAO_PROJECT_API_KEY_HERE>
   LOGIN_USERNAME=<YOUR_10XTO_USERNAME_HERE>
   LOGIN_PASSWORD=<YOUR_10XTO_PASSWORD_HERE>
   HOST_NAME=<YOUR_FIRST_AND_LAST_NAME_HERE>   

3. **Set pyenv**

   ```bash
   $ pyenv local 3.11.0
   ```
4. **Install dependencies using Pipenv:**

    ```bash
    $ pipenv install
    ```

5. **Activate the virtual environment:**

   ```bash
   $ pipenv shell
   ```

6. **Usage:**
   ```bash
   $ streamlit run src/ui.py
   
   You can now view your Streamlit app in your browser
   
   Local URL: http://localhost:8501
   Network URL: http://10.88.111.4:8501
   
   ```


This command will start the booking assistant, which will attempt to book available tennis courts based on your conversation with the assistant.

# What to ask the assistant
Currently there are two services that the assistant can do for you

1. Reserve a tennis court
2. Check out the court availabilities

## How to reserve a tennis court:
Ask the assistant to reserve a tennis court for you. You may use the following prompt or anything similar to this. 

`book a court for me and Alejandro for tomorrow at 7pm.`

## How to check out the available spots:

`what are the available spots for next Friday?`





### Happy booking! 🏸


