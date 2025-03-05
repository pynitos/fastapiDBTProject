from io import BytesIO

from boto3 import client
from botocore.client import BaseClient
from botocore.config import Config

from src.diary_ms.application.common.interfaces.file_manager import FileManager
from src.diary_ms.infrastructure.s3.config import S3Config


class S3FileManager(FileManager):
    def __init__(self, config: S3Config):
        self._config: S3Config = config
        self._bucket: str = "diary_cards"

    @property
    def _client(self) -> BaseClient:
        return client(
            "s3",
            endpoint_url=self._config.endpoint_url,
            aws_access_key_id=self._config.aws_access_key_id,
            aws_secret_access_key=self._config.aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    def save(self, payload: bytes, path: str) -> None:
        with BytesIO(payload) as file_obj:
            self._client.upload_fileobj(file_obj, self._bucket, path)

    def get_by_file_id(self, file_path: str) -> bytes | None:
        data = self._client.get_object(Bucket=self._bucket, Key=file_path)

        if not data:
            return None
        return data["Body"].read()

    def delete_object(self, path: str) -> None:
        self._client.delete_object(Bucket=self._bucket, Key=path)

    def delete_folder(self, folder: str) -> None:
        objects_to_delete = self._client.list_objects_v2(
            Bucket=self._bucket,
            Prefix=folder,
        )
        if "Contents" in objects_to_delete:
            for obj in objects_to_delete["Contents"]:
                self._client.delete_object(Bucket=self._bucket, Key=obj["Key"])
