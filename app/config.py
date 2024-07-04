import os

from dotenv import load_dotenv

load_dotenv()


def get_env():
    env = BaseConfig.ENVIRONMENT

    if env in ["dev", "develop", "development"]:
        return DevelopmentConfig
    elif env in ["production", "prod", "staging", "stag"]:
        return ProductionConfig
    elif env in ["testing", "test"]:
        return TestingConfig


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY") or "abcdefg132456"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL = os.getenv("DATABASE_DEV")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    OPENAI_ORG = os.getenv("OPENAI_ORG")
    ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")
    STARTING_CONTEXT = os.getenv("STARTING_CONTEXT")


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DATABASE_URL = os.getenv("DATABASE_TEST")


config = get_env()
