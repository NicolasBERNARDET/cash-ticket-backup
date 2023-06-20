from src.cash_ticket_backup.converters.xml_to_json import convert_to_json
from src.cash_ticket_backup.models.document_type import DocumentType


class Document:
    def __init__(self, xml_data, filename):
        self.xml_data: str = xml_data
        self.filename: str = filename
        self.conversion_type: DocumentType = DocumentType.XML

    def to_json(self) -> str:
        success, converted_data = convert_to_json(self.xml_data)
        if success:
            self.conversion_type = DocumentType.JSON
        else:
            self.conversion_type = DocumentType.XML
        return converted_data

    def to_xml(self) -> str:
        self.conversion_type = DocumentType.XML
        return self.xml_data

    def __str__(self) -> str:
        return f"{self.filename}.{self.conversion_type.value.lower()}"
