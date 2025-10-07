from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "School Management System"
    database_url: str = "sqlite+aiosqlite:///./school.db"

    class Config:
        env_file = ".env"

settings = Settings()
