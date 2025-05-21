from jose import JWTError, jwt, exceptions
from datetime import datetime, timedelta
from project.settings import settings
from datetime import timezone
from fastapi import Depends, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

class Auth:
    def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
        if not token or token.credentials != 'expected_token':
            raise HTTPException(status_code=403, detail="Invalid authorization token")
        return token.credentials

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    
    def verify_token(token: str, algorithm="HS256"):
        valid = True
        try:
            token_decode = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[algorithm]
            )
            expiration = token_decode["exp"]
            
            #utc_timestamp = datetime.now(timezone.utc).timestamp()
            #jwt_timestamp = expiration
            #utc_datetime = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
            #jwt_datetime = datetime.fromtimestamp(jwt_timestamp, tz=timezone.utc)
            if datetime.now(timezone.utc).timestamp() >= expiration:
                return {"valid": False, "data": []}
        except (JWTError, KeyError) as e:
            print(e)
            return {"valid": False, "data": []}
        return {"valid": valid, "data": token_decode}