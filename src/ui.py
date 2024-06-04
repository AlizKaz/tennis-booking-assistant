import os

import streamlit as st

import booking_api
import booking_prompt
import booking_service
import gpt_service

from dotenv import load_dotenv

st.title("ChatGPT Booking Assistant")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "init_env" not in st.session_state:
    load_dotenv()
    # print(os.environ)
    # os.environ.get('OPENAI_API_KEY_BOOKING_PROJECT')
    # print(os.environ.get('OPENAI_API_KEY_BOOKING_PROJECT'))
    st.session_state.init_env = True
    username = os.environ.get('LOGIN_USERNAME')
    password = os.environ.get('LOGIN_PASSWORD')
    host_name = os.environ.get('HOST_NAME')
    st.session_state.username = username
    st.session_state.password = password
    st.session_state.host_name = host_name

if "init_client" not in st.session_state:
    st.session_state.init_client = True
    client = gpt_service.init_client()
    st.session_state.client = client


if "init_booking_prompt" not in st.session_state:
    st.session_state.init_booking_prompt = True
    tools, gpt_model, system_message = booking_prompt.init()
    st.session_state.system_message = system_message
    st.session_state.tools = tools
    st.session_state.gpt_model = gpt_model
    st.session_state.messages = []

if "access_token" not in st.session_state:
    username = st.session_state.username
    password = st.session_state.password

    if "failed_login" not in st.session_state:
        success, login_result = booking_api.login(api_url=booking_api.auth_api_url, username=username, password=password)
        if not success:
            st.session_state.failed_login = True
            st.session_state.login_error = login_result
        else:
            st.session_state.access_token = login_result['token']
            st.session_state.host_id = login_result['profileId']
    else:
        st.write(f"unable to login {st.session_state.login_error}")

# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "system", "content": st.system_message}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_response = gpt_service.chat_completion_request(
            client=st.session_state.client,
            system_message=st.session_state.system_message,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ], tools=st.session_state.tools, tool_choice="auto", model=st.session_state.gpt_model
        )
        response = chat_response.choices[0].message

        result = booking_service.process_gpt_response(response, access_token=st.session_state.access_token,
                                                      host_name=st.session_state.host_name)

        st.write(result)

        st.session_state.messages.append({"role": "assistant", "content": result})
