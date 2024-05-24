""" This module contains the StorageAccountOptions class. """
from dataclasses import dataclass

@dataclass
class StorageAccountOptions:
    """
    Options for configuring the Storage Account where the original documents are stored.
    Args:
        url: The base url of the storage account.
    Note: The system expects that the container name will be returned with the document metadata.
    """
    url: str
