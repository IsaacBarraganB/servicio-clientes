from project.services.service import Service
from project.composers.users_compose import UsersCompose

class UserService(Service):
    compose: UsersCompose
    def __init__(
        self,
        compose=None
        ) -> None:
        super().__init__(compose)
        self.compose = compose
    
    def login(self, form_data):
        return self.compose.login(form_data=form_data)