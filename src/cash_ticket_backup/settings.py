from src.cash_ticket_backup.utils.settings import HashableSettings


class AzureObjectStorageSettings(HashableSettings):
    """Azure Object Storage settings"""

    connection_string: str = ''
    extension_file: str = ''

    class Config:
        env_prefix = "aoz_"
        env_file = '.env'
        env_file_encoding = 'utf-8'
