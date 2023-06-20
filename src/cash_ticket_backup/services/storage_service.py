import logging
import re

from src.cash_ticket_backup.models.document import Document
from src.cash_ticket_backup.models.document_type import DocumentType
from src.cash_ticket_backup.settings import AzureObjectStorageSettings
from src.cash_ticket_backup.storage.azure_object_storage import BlobStorageClient

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self):
        self.blob_client = BlobStorageClient(AzureObjectStorageSettings())

    def store_document(self, document: Document, document_type: DocumentType, container_name: str) -> None:
        data: str
        extension: str

        if document_type == DocumentType.JSON:
            json_data: str = document.to_json()
            if document.conversion_type == DocumentType.JSON:
                data = json_data
                extension = document_type.value.lower()
            else:  # fail to convert
                data = document.to_xml()
                extension = document_type.value.lower()
        else:
            data = document.to_xml()
            extension = document_type.value.lower()

        # Pluralize name
        document_name = f'{(document.filename.split("--")[0])}s'
        computer_id = 'undefined'
        creation_date = 'undefined'

        # Extract computer ID from filename
        match_computer = re.search(r"--(\d+)--", document.filename)
        if match_computer:
            computer_id = match_computer.group(1)
        else:
            logger.warning("The file name does not appear to contain a computer ID.")

        # Extract creation date from filename
        match_date = re.search(r"--(\d{4}-\d{2}-\d{2})", document.filename)
        if match_date:
            creation_date = match_date.group(1)
        else:
            logger.warning("The file name does not appear to contain a creation date.")

        blob_path =  f'{computer_id}/{document_name}/{creation_date}/{document.filename}.{extension}'
        self.blob_client.upload_blob(data, blob_path, container_name)
