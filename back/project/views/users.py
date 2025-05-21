from project.schemas import UserSchema, Token, Message, OAuth2PasswordRequestFormSchema
from project.composers.users_compose import UsersCompose
from project.services.user_service import UserService
from project.models import Users
from project.infrastructure.repository import session
from project.settings import settings
from project.utils.general_utils import GeneralUtils
from project.utils.auth import Auth
from project.utils.constants import Constants
from fastapi import Depends
from typing import List

VIEWS = {
"ViewUser":{
"view": "ViewUser",
"cols": [ 'id', 'nickname', 'branch_id']}
}


def __get_service__(model=Users, config: List[str] = []) -> UserService:
    model = model
    composer = UsersCompose(
        model=model,
        notify='El usuario',
        repository=next(session()),
        settings=settings,
        generalUtils=GeneralUtils,
        constants=Constants,
        auth=Auth,
        config=config
    )
    service = UserService(compose=composer)
    return service

def users(app, route='/users', tags=["Users"]):
    @app.post(route, tags=tags)
    def post(schema: UserSchema):
        service = __get_service__(config=app.authConfig.get_info())
        request = service.create(schema=schema, refresh=False)
        return request
    
    @app.post(route + '/token', response_model=Token | Message, response_model_exclude_unset=True, tags=tags)
    def post(from_data: OAuth2PasswordRequestFormSchema=Depends()):
        service = __get_service__(config=app.authConfig.get_info())
        request = service.login(form_data=from_data)
        return request

    @app.put(route + "/{id}", tags=tags)
    def put(id: int, schema: UserSchema):
        service = __get_service__(config=app.authConfig.get_info())
        request = service.update(id, schema=schema)
        return request

    @app.get(route, tags=tags)
    def get(filters=None, or_filter=None, pagination=None):
        #[["id","=",1]]
        #{"sortBy":"grupo","descending":"false","page":1,"rowsNumber":0,"rowsPerPage":15}
        service = __get_service__(config=app.authConfig.get_info())
        request = service.pagination(
            filter=filters,
            or_filters=or_filter,
            pagination=pagination,
            columns=['id', 'nickname', 'fullname', 'email', 'branch_id']
        )
        return {"data": request}

    @app.get(route + "/get_pag", tags=tags)
    def get_pag(filters=None, or_filters=None, pagination=None, view=None):
        views = VIEWS.get(view)
        if views:
            service = __get_service__(model=views['view'],config=app.authConfig.get_info())
            request = service.pagination(
                filter=filters,
                or_filters=or_filters,pagination=pagination, columns=views['cols'])
        else:
            service = __get_service__(config=app.authConfig.get_info())
            request = service.pagination(
                filter=filters,
                or_filters=or_filters,pagination=pagination)

        return {"data": request}
    
    @app.delete(route + "/{id}", tags=tags)
    def delete(id: int):
        service = __get_service__(config=app.authConfig.get_info())
        request = service.delete(id=id)
        return request