from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_simple_auth import SimpleAuth, logged_in_user
from pydantic_settings import BaseSettings
import requests
from fastapi.templating import Jinja2Templates



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    auth_secret_key: str = "secret_key"
    api_url: str = "http://localhost:8899/frontbot"

settings = Settings()

simpleauth = SimpleAuth(app)

@app.get("/")
async def frontbot_view(rq: Request, user: logged_in_user) -> str:    

    r = requests.get(f"{settings.api_url}")
    print(r)
    return templates.TemplateResponse(
        request=rq, name="index.html", context={"id": id}
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
