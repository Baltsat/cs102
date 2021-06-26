from envparse import env

POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="postgres")
POSTGRES_USER = env.str("POSTGRES_USER", default="postgres")
POSTGRES_DB = env.str("POSTGRES_DB", default="notes")
POSTGRES_URI = (
    f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

SECRET_KEY = env.str("SECRET_KEY", default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES', default=30)
ALGORITHM = env.str("ALGORITHM", default="HS256")
