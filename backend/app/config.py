from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    APP_NAME: str = "GENESIS"
    APP_ENV: str = "development"
    DEBUG: bool = True
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://genesis_user:genesis_secret_password@localhost:5432/genesis_db"
    DATABASE_URL_SYNC: str = "postgresql://genesis_user:genesis_secret_password@localhost:5432/genesis_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "genesis_graph_pass"

    # Storage
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "genesis_admin"
    S3_SECRET_KEY: str = "genesis_minio_pass"
    S3_BUCKET_NAME: str = "genesis-documents"
    S3_REGION: str = "us-east-1"

    # Auth & Tokens
    JWT_SECRET_KEY: str = "genesis_dev_jwt_insecure_key_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI Keys
    OPENAI_API_KEY: str = ""
    COHERE_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
