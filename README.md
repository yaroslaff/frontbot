# frontbot

Fronbot is lightweight authentication frontend/proxy for your API admin part

## start
Start with `fronbot` or  `uvicorn --reload frontbot.frontbo:app` (with any other args)

## How to write fronbot-protected app

If user authenticated with fronbot, frontbot will make requests to application ()

See `frontbot/demoapp.py` for full example, but essential code is:
~~~python
@app.get("/frontbot", response_model=FrontBotResponse)
def frontbot(request: Request):
    token = request.headers.get('authorization').split(' ')[1]
    username = request.headers.get('x-username')
    userid = request.headers.get('x-userid')

    if token != args.token:
        return FrontBotResponse(error=f'Bad token')

    vnum = record_visit(userid)

    data = FrontBotResponse(text=f'Hello **{username}**!\n\nYour userID is {userid}\n\nThis is your visit #{vnum}')
    return data
~~~

## Example .env config
~~~
APP_TITLE="FrontBot"

APP_TOKEN="my-bearer-secret"
APP_URL="http://localhost:8899/frontbot"

CLIENT_IP_HEADER="x-forwarded-for"

TURNSTILE_SITEKEY=0x...
TURNSTILE_SECRET=0x...
~~~