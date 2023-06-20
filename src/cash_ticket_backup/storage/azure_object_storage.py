from azure.storage.blob import BlobServiceClient

from src.cash_ticket_backup.settings import AzureObjectStorageSettings


class BlobStorageClient:
    def __init__(self, settings: AzureObjectStorageSettings) -> None:
        self.blob_service_client = BlobServiceClient.from_connection_string(settings.connection_string)

    def upload_blob(self, data, filename, container_name: str):
        try:
            # create container if not exist
            if not self.blob_service_client.get_container_client(container_name).exists():
                self.blob_service_client.create_container(container_name)

            blob_client = self.blob_service_client.get_blob_client(container=container_name,
                                                                   blob=filename)
            blob_client.upload_blob(data, overwrite=True)
        except Exception as e:
            raise Exception(f'Error uploading the document: {str(e)}')
