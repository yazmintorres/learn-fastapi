from pydantic_settings import BaseSettings, SettingsConfigDict

# creating pydantic model for expected environment variables
class Settings(BaseSettings):
    db_hostname: str 
    db_port: str
    db_password: str 
    db_name: str 
    db_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()



