from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = 'errandzmedia'
    account_key = '8awAXJF7wt0mZxUCazvlZAOFOJrzWN2chLszZWv9FWYc2GFf4kpG4Lz78ONkRit0J+CufD3OdNjT+ASt/1X0hw=='
    azure_container = 'media'
    expiration_secs = None
