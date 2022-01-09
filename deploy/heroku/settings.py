from recipebook.config.settings.base import *
import os
import ssl
import dj_database_url

INSTALLED_APPS = INSTALLED_APPS + ["storages"]

DEBUG = True
ALLOWED_HOSTS += [f'{os.getenv("HEROKU_APP_NAME")}.herokuapp.com']
MEDIA_ROOT = "/recipebook/media"

# MJML_BACKEND_MODE = "cmd"
# MJML_EXEC_CMD = "mjml"

# FROM_EMAIL = f"no-reply@{os.environ['MAILGUN_DOMAIN']}"
# CELERY_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_USE_TLS = False
# EMAIL_HOST = os.environ["MAILGUN_SMTP_SERVER"]
# EMAIL_PORT = os.environ["MAILGUN_SMTP_PORT"]
# EMAIL_HOST_USER = os.environ["MAILGUN_SMTP_LOGIN"]
# EMAIL_HOST_PASSWORD = os.environ["MAILGUN_SMTP_PASSWORD"]

# We need to set the certificate check to None, otherwise it is not compatible with the
# `heroku-redis:hobby-dev` addon. The URL generated by that addon is over a secured
# connection with a self signed certificate. The redis broker could fail if the
# certificate can't be verified.
# CELERY_REDBEAT_REDIS_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE}
ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE
# CHANNELS_REDIS_HOST = {"address": REDIS_URL, "ssl": ssl_context}
# CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [CHANNELS_REDIS_HOST]

# Set the limit of the connection pool based on the amount of workers that must be
# started with a limit of 10, which is the default value. This is needed because the
# `heroku-redis:hobby-dev` doesn't accept more than 20 connections.
# CELERY_BROKER_POOL_LIMIT = min(
#     4 * int(os.getenv("recipebook_AMOUNT_OF_WORKERS", "1")), 10)
# CELERY_REDIS_MAX_CONNECTIONS = min(
#     4 * int(os.getenv("recipebook_AMOUNT_OF_WORKERS", "1")), 10
# )

DATABASES = {
    "default": dj_database_url.parse(os.environ["DATABASE_URL"], conn_max_age=600)
}

if os.getenv("AWS_ACCESS_KEY_ID", "") != "":
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
        "ContentDisposition": "attachment",
    }
    AWS_S3_FILE_OVERWRITE = True
    AWS_DEFAULT_ACL = "public-read"

if os.getenv("AWS_S3_REGION_NAME", "") != "":
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")

if os.getenv("AWS_S3_ENDPOINT_URL", "") != "":
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")

if os.getenv("AWS_S3_CUSTOM_DOMAIN", "") != "":
    AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN")