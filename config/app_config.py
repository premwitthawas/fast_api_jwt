from dotenv import load_dotenv
import os
load_dotenv()

class DbConfig:
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_DB")
    DB_PORT = os.getenv("POSTGRES_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")

class JwtConfig:
    JWT_ACESSS_SECRET_KEY = os.getenv("JWT_ACESSS_SECRET_KEY")
    JWT_ACESSS_ALGORITHM = os.getenv("JWT_ACESSS_ALGORITHM")
    JWT_ACCESS_EXPIRATION_TIME_MINUTES = os.getenv("JWT_ACCESS_EXPIRATION_TIME_MINUTES")
