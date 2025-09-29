# import os
import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.routing import APIRoute
# from bot_processing.submit_form import submit_form
from endpoints.bot import main_bot
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse, RedirectResponse
# from endpoints.bot_register_url import bot_register_url
# # from endpoints.change_registered import change_registered
# from endpoints.send_messages_user import send_messages_user
# from pg.pg_add_tables import bd_create_tables
# from middleware.verify_ones import verify_endpoints


async def ping(request: Request):
    print("client_host:", request.client.host)
    return "YOU ARE ON THE MAIN PAGE"

async def submit_form(request: Request):
    req = await request.json()
    print("req", req)
    # print("client_host:", request.client.host)
    return "YOU ARE ON THE MAIN PAGE"

# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# async def base(request: Request):
#     return templates.TemplateResponse("base.html", {"request": request})

# async def root():
#     return {"message": "Hello World"}

routes = [
    APIRoute(path="/bot", endpoint=main_bot, methods=["POST"]),
    # APIRoute(path="/sub", endpoint=submit_form, methods=["POST"]),
    APIRoute(path="/ping", endpoint=ping, methods=["GET"]),
    # APIRoute(path="/index", endpoint=index, methods=["GET"]),
    # APIRoute(path="/base", endpoint=base, methods=["GET"]),
    # APIRoute(path="/read_root", endpoint=root, methods=["GET"]),
    
    # APIRoute(path="/index", endpoint=ping, methods=["GET"]),
    # APIRoute(path="/bot_register_url", endpoint=bot_register_url, methods=["GET"]),
    # APIRoute(path="/create_table", endpoint=bd_create_tables, methods=["GET"]),
    # APIRoute(
    #     path="/change_registered",
    #     endpoint=change_registered,
    #     methods=["POST"],
    #     dependencies=[Depends(verify_endpoints)],
    # ),
    # APIRoute(
    #     path="/send_messages_user",
    #     endpoint=send_messages_user,
    #     methods=["POST"],
    #     dependencies=[Depends(verify_endpoints)],
    # ),
]

app = FastAPI()
app.include_router(APIRouter(routes=routes))
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
# templates = Jinja2Templates(directory="app/templates")

# print("Current working directory:", os.getcwd())

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)  