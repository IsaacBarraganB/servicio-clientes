from project.composers.compose import Compose
from project.settings import Settings
from project.utils.constants import Constants
from project.utils.general_utils import GeneralUtils
from project.utils.auth import Auth
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
class UsersCompose(Compose):
    def __init__(
        self,
        model: any = None,
        notify: str = None,
        repository=None,
        settings: Settings = None,
        generalUtils: GeneralUtils = None,
        constants: Constants = None,
        auth:Auth = None,
        config=None,
        modelAccount: any = None
        ) -> None:
        super().__init__(model, notify, repository, settings, generalUtils, constants, config)
        self.auth = auth
        self.repository = repository
        self.settings = settings
        self.modelAccount = modelAccount
    

    def login(self, form_data: OAuth2PasswordRequestForm):
        user = self.model.authenticate(
            self.repository,
            form_data.username,
            form_data.password,
        )
        if user:
            access_token_expires = timedelta(
            minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            access_token = self.auth.create_access_token(
                data={"name": user.fullname, "sub":f'{user.id}', "account_id": user.account_id },
                expires_delta=access_token_expires
            )
            account = self.modelAccount.search(
                self.repository,
                user.account_id
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user.id,
                "user_email": user.email,
                "fullname": user.fullname,
                "account": account.name,
                "result": True,
                "message": "Iniciaste sesión correctamente"
            }
        else:
            return {
                "message": "No se encontro el usuario.",
                "result": False
            }

        