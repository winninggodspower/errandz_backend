from storages.backends.azure_storage import AzureStorage
from errandz_backend import settings


class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = 'media'
    expiration_secs = None
