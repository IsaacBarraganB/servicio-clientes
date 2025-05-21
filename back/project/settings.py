from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
class Settings:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Settings, cls).__new__(cls)
        return cls.instance

    SQLALCHEMY_DATABASE_URI = DATABASE_URL #"postgresql://postgres:1234567@localhost/db_base"
    API_V1_STR = "/api/v1"
    SECRET_KEY = (
        "021BA6E2EE85A9C41A49A008DCD5782EAC5F9E4FEE80324D708B1C22CCE9B32F"
    )
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 120


settings = Settings()
