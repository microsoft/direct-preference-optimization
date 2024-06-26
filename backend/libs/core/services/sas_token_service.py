"""Module to generate SAS token for Azure Blob Storage"""
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse
from azure.storage.blob import generate_blob_sas, BlobServiceClient, BlobSasPermissions, UserDelegationKey
from azure.identity import DefaultAzureCredential
from libs.core.models.options import StorageAccountOptions

class SasTokenService:
    """Manage the generation of SAS tokens for Azure Blob Storage."""

    def __init__(self, storage_account_options: StorageAccountOptions):
        self._storage_account_options = storage_account_options
        self._blob_service_client: BlobServiceClient = None
        self._user_delegation_key: UserDelegationKey = None

    def _create_blob_service_client(self):
        """Create a BlobServiceClient based on the connection string."""
        if self._storage_account_options.use_account_key:
            connection_string = f"DefaultEndpointsProtocol=https;AccountName={self._storage_account_options.account_name};AccountKey={self._storage_account_options.account_key};EndpointSuffix=core.windows.net"
            self._blob_service_client = BlobServiceClient.from_connection_string(
                conn_str=connection_string)
        else:
            self._blob_service_client = BlobServiceClient(
                self._storage_account_options.url,
                credential=DefaultAzureCredential()
            )

    def _get_user_delegation_key(self):
        """Get the user delegation key for the storage account."""
        if not self._blob_service_client:
            self._create_blob_service_client()

        if not self._user_delegation_key or isoparse(self._user_delegation_key.signed_expiry) < datetime.now(timezone.utc):
            self._user_delegation_key = self._blob_service_client.get_user_delegation_key(
                key_start_time=datetime.now(timezone.utc),
                key_expiry_time=datetime.now(timezone.utc) + timedelta(hours=1)
            )

        return self._user_delegation_key

    def get_sas_token_for_blob(
        self,
        blob_name: str,
        container_name: str,
        expiry: int = 3600
    ):
        """Generates a SAS token for the given blob."""

        if not self._blob_service_client:
            self._create_blob_service_client()

        if self._storage_account_options.use_account_key:
            sas_token = generate_blob_sas(
                account_name=self._storage_account_options.account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=self._storage_account_options.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.now(timezone.utc) + timedelta(seconds=expiry)
            )
        else:
            sas_token = generate_blob_sas(
                account_name=self._storage_account_options.account_name,
                container_name=container_name,
                blob_name=blob_name,
                user_delegation_key=self._get_user_delegation_key(),
                permission=BlobSasPermissions(read=True),
                expiry=datetime.now(timezone.utc) + timedelta(seconds=expiry)
            )

        return sas_token
