from passlib.hash import pbkdf2_sha256
from sqlalchemy import String, Text, ForeignKey, or_
from sqlalchemy.orm import Mapped, mapped_column
from project.models.base import Model

class Users(Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(30), nullable=False)
    fullname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable= False)
    
    def __init__(self, nickname, fullname, email, password):
        self.nickname = nickname
        self.fullname = str.upper(fullname)
        self.email = str.lower(email)
        self.password = pbkdf2_sha256.hash(password)

    @classmethod
    def authenticate(user, repository: any, nickname: str, password: str):
        if not nickname or not password:
            return None

        
        user = (
            repository.query(user)
            .filter(or_(user.nickname == nickname, user.email == nickname))
            .first()
        )
        if not user or not pbkdf2_sha256.verify(password, user.password):
            return None

        return user

    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, nickname={self.nickname!r}, fullname={self.fullname!r}, email={self.email!r}, password={self.password!r})"
    