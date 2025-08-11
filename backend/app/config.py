import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or os.getenv(
        "POSTGRES_URL",
        "postgresql+psycopg2://goldcert:goldcert@db:5432/goldcert",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "change-me")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
