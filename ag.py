#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import readline
from client.myclient import Client


def signal_handler(signal, frame):
    print("\n\n\033[0;31m" + "exit" + "\033[0m")
    os._exit(0)


def talk_gpt(myclient):
    response = ""
    try:
        response = myclient.client.chat.completions.create(
            model=myclient.Config.model,
            messages=myclient.get_context(),
            stream=True,
            presence_penalty=1,
            frequency_penalty=1,
            temperature=1.0,
            n=1
        )
    except Exception as e:
        print("\033[0;31m" + "连接超时, 请检查你的api_key与base_url" + "\033[0m")
        os._exit(0)

    gptcontent = ""
    print(myclient.display_model + " > ", end="")
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            gptcontent += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="", flush=True)

    myclient.put({"role": "assistant", "content": gptcontent})
    print("")

    with open(myclient.history, "a+") as file:
        file.write("*" + myclient.Config.model + " > *\n\n")
        file.write(gptcontent + "\n\n")
    return gptcontent


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    myClient = Client()
    myClient.put(myClient.Config.prompt)

    while True:
        user_content = ""
        try:
            user_content = input(myClient.display_user + " > ")
            if user_content == "q" or user_content == "exit":
                print("\033[0;31m" + "exit" + "\033[0m")
                break
        except EOFError:
            print("\n\n\033[0;31m" + "exit" + "\033[0m")
            os._exit(0)

        print("")

        with open(myClient.history, "a+") as file:
            file.write("*" + myClient.user + " > *\n\n")
            file.write(user_content + "\n\n")

        myClient.put({"role": "user", "content": user_content})

        gpt_content = talk_gpt(myClient)
        print("")
