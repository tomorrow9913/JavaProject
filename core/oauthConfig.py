from fastapi.security import OAuth2PasswordBearer

ACCESS_TOKEN_EXPIRE_MINUTES = 60 # config('ALGORITHM')
SECRET_KEY = "5b8994d916c07caaa2adf3f4d5c785bc8f0912532808806d62f4f5da375ebfa8" # config('SECRET_KEY')
ALGORITHM = "HS256" # config('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
