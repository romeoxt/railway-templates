from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    blog_title: str = "My Blog"
    blog_tagline: str = "Notes and updates"
    admin_api_key: str = ""


settings = Settings()
