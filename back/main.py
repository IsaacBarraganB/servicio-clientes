from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from project.views.view_routes import add_routes
from project.utils.auth import Auth
from project.utils.openapi_config import schemas_openapi_config
from fastapi.openapi.utils import get_openapi
from project.lib.auth_config import AuthConfig


class Manager(FastAPI):
    def __init_service__(self):
        self.authConfig = AuthConfig()

def create_app() -> Manager:
    app = Manager()
    add_routes(app)
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom FastAPI",
        version="3.1.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["components"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
    schemas_openapi_config(openapi_schema["components"])
    openapi_schema["security"] = [
        {
            "bearerAuth": []
        }
    ]
    app.openapi_schema = openapi_schema
    app.__init_service__()
    return app

app = create_app()


origins = [
    'http://localhost:9000',
    'http://localhost:9300',
    'http://localhost:9001',
    'http://127.0.0.1:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_request(request: Request, call_next):
    is_valid = False
    data = {"message": "No tiene permiso para acceder a este recurso."}
    expire = {"message": "La sesion caducó, inicia sesion de nuevo."}

    if request.method == "OPTIONS":
        return await call_next(request)

    if request.url.path == "/users/token" and request.method == "POST":
        return await call_next(request)
    
    if request.url.path == "/users" and request.method == "POST":
        return await call_next(request)
    
    if request.url.path == "/account/addAccountUser" and request.method == "POST":
        return await call_next(request)
    
    if request.url.path == "/docs" or request.url.path == "/openapi.json":
        return await call_next(request)
    
    
    if request.url.path != "/users/token" and request.method != "OPTIONS":
        if request.headers.get("authorization"):
            _, token = request.headers.get("authorization").split("Bearer ")
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content=data
            )
        
        is_valid = Auth.verify_token(token)
        if is_valid['valid']:
            app.authConfig.set_info(info=is_valid['data'])
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content=expire
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content=data
        )