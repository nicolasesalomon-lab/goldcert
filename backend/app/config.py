import os
class Config:
    API_TITLE="GoldCert API v2"; API_VERSION="2.0"; OPENAPI_VERSION="3.1.0"
    OPENAPI_URL_PREFIX="/"; OPENAPI_JSON_PATH="openapi.json"
    OPENAPI_SWAGGER_UI_PATH="/swagger-ui"; OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL","sqlite:///goldcert.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False; PROPAGATE_EXCEPTIONS=True
    JWT_SECRET_KEY=os.getenv("SECRET_KEY","changeit")
    JWT_ACCESS_TOKEN_EXPIRES=int(os.getenv("ACCESS_TOKEN_EXPIRES","86400"))
    MAX_CONTENT_LENGTH=int(os.getenv("MAX_CONTENT_LENGTH","10485760"))
    UPLOAD_DIR=os.getenv("UPLOAD_DIR","/app/storage")
