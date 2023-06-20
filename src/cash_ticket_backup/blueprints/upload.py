import logging

from flask import Blueprint, request

from src.cash_ticket_backup.blueprints.schemas.logics import required_params
from src.cash_ticket_backup.blueprints.schemas.upload_schema import UploadSchema
from src.cash_ticket_backup.models.document import Document
from src.cash_ticket_backup.models.document_type import DocumentType
from src.cash_ticket_backup.services.storage_service import StorageService
from src.cash_ticket_backup.settings import AzureObjectStorageSettings

upload_blueprint = Blueprint('upload', __name__)

logger = logging.getLogger(__name__)


@upload_blueprint.route('/upload', methods=['POST'])
@required_params(UploadSchema())
def upload_document():
    try:
        data = request.get_json()

        # Récupérer les données XML et le nom du document depuis la requête
        xml_data = data.get('xml_data')
        filename = data.get('filename')
        container_name = data.get('client_name')

        settings = AzureObjectStorageSettings()
        document_type = settings.extension_file

        logger.info('Creating document: %s', filename)
        document = Document(xml_data, filename)

        logger.info('Storing document : %s', filename)
        storage_service = StorageService()
        storage_service.store_document(document, DocumentType(document_type), container_name)

        logger.info('Document %s saved successfully', str(document))
        return 'Document saved successfully.'
    except Exception as e:
        logger.error(str(e))
        return str(e), 400
