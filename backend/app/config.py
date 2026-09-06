from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="COACH_LUNA_")
    database_path: Path = Path(__file__).resolve().parents[1] / "coach_luna.db"
    cors_origins: list[str] = ["http://localhost:8081", "http://127.0.0.1:8081", "http://localhost:8083", "http://127.0.0.1:8083"]


settings = Settings()
