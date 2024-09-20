#!/usr/bin/env python

from fastapi import FastAPI, Request
from pydantic import BaseModel 
from typing import List
from dotenv import load_dotenv
import argparse
import os
import json

app = FastAPI()
args = None


class FrontBotResponse(BaseModel):
    text: str | None = None
    error: str | None = None
    forms: dict[str, dict] | None = dict()
    popup: str | None = None

users = dict()

@app.get("/frontbot", response_model=FrontBotResponse)
@app.post("/frontbot", response_model=FrontBotResponse)
async def frontbot(request: Request):
    global users
    
    if not 'authorization' in request.headers:
        return FrontBotResponse(error='Missing authorization header')

    token = request.headers.get('authorization').split(' ')[1]
    username = request.headers.get('x-username')
    userid = request.headers.get('x-userid')

    if token != args.token:
        return FrontBotResponse(error=f'Bad token')

    users[userid] = users.get(userid, 0) + 1

    msg = ""

    data = FrontBotResponse(text=f'Hello **{username}**!\n\nYour userID is {userid}\nCounter is {users[userid]}\n')

    if request.method == "POST":
        form = await request.form()
        if form["_fronbot_form_name"] == "reset":
            users[userid] = 0
            data.popup = "Counter **reset**<br>start from beginning"
        elif form["_fronbot_form_name"] == "hundred":
            users[userid] += 100
            data.popup = "+100"
        elif form["_fronbot_form_name"] == "set":
            users[userid] = int(form["new_value"])
            data.popup = f"Set to {form['new_value']}"


    data.forms["reset"]  = {"submit": "Reset counter", "class": "is-warning"}
    data.forms["hundred"] = {"submit": "+100" }
    data.forms["set"] = {"submit": "set specific value", 
                         "fields": {
                             "new_value": {
                                 "title": "New value",
                             },
        }
    }
    return data

def get_args():
    parser = argparse.ArgumentParser(description='FrontBot-protected demo application')

    def_host = os.getenv('FRONTBOT_APP_HOST', 'localhost')
    def_port = int(os.getenv('FRONTBOT_APP_POST', '8899'))
    def_token = os.getenv('APP_TOKEN')

    parser.add_argument('--host', type=str, default=def_host)
    parser.add_argument('--port', '-p', type=int, default=def_port)
    parser.add_argument('--token', '-t', type=str, default=def_token)
    return parser.parse_args()

def main():
    global args
    import uvicorn
    load_dotenv()
    args = get_args()
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()