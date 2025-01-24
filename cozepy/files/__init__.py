from typing import List, Optional, Dict, Any, IO, Union, Tuple
from enum import IntEnum
from cozepy.model import CozeModel, NumberPaged, AsyncNumberPaged, NumberPagedResponse
from cozepy.auth import Auth
from cozepy.request import HTTPRequest, Requester
from cozepy.util import remove_url_trailing_slash
from pathlib import Path
import os

FileContent = Union[IO[bytes], bytes, str, Path]
FileTypes = Union[
    # file (or bytes)
    FileContent,
    # (filename, file (or bytes))
    Tuple[Optional[str], FileContent],
]


def _try_fix_file(file: FileTypes) -> FileTypes:
    if isinstance(file, Path):
        if not file.exists():
            raise ValueError(f"File not found: {file}")
        return open(file, "rb")

    if isinstance(file, str):
        if not os.path.isfile(file):
            raise ValueError(f"File not found: {file}")
        return open(file, "rb")

    return file


class File(CozeModel):
    """Uploaded file ID."""

    id: str
    """Total bytes of the file."""
    bytes: Optional[int] = None
    """The upload time of the file, formatted as a 10-digit Unix time stamp in seconds (s)."""
    created_at: Optional[int] = None
    """Document Name."""
    file_name: Optional[str] = None


class ResponseDetail(CozeModel):
    pass


"""
API Client for files endpoints
"""


class FilesClient(object):
    def __init__(self, base_url: str, auth: Auth, requester: Requester):
        self._base_url = remove_url_trailing_slash(base_url)
        self._auth = auth
        self._requester = requester

    """
    View the details of uploaded files.
    :param file_id: Uploaded file ID.
    :return: 
    """

    def retrieve(
        self,
        *,
        file_id: str,
    ) -> File:
        url = f"{self._base_url}/v1/files/retrieve"
        params = {
            "file_id": file_id,
        }
        return self._requester.request(
            "GET",
            url,
            False,
            cast=File,
            params=params,
        )

    """
    Upload a file to the Coze platform.
**API description**
Local files cannot be directly used in messages. Before creating a message or conversation, you need to call this API to upload local files to Coze. After uploading the file, you can directly use it in multimodal content by specifying the `file_id` in the message. For usage instructions, see [Create a conversation](https://www.coze.cn/docs/developer_guides/create_conversation).

* Supported file formats:
   Document**:** DOC, DOCX, XLS, XLSX, PPT, PPTX, PDF, Numbers, and CSV
   Image**:** JPG, JPG2, PNG, GIF, WEBP, HEIC, HEIF, BMP, PCD, and TIFF
* File upload size limit:** **Each file can be up to 512 MB.
* Files uploaded to Coze can only be viewed or used by the account that uploaded them.
* Files must be uploaded using the `multipart/form-data` method.
* Files uploaded using the API expire after 3 months.
    :param file: Supported file formats for upload:
Documents: DOC, DOCX, XLS, XLSX, PPT, PPTX, PDF, Numbers, CSV
Images: JPG, JPG2, PNG, GIF, WEBP, HEIC, HEIF, BMP, PCD, TIFF
File upload size limit: Each file is a maximum of 512 MB.
Files uploaded to the platform are for viewing or use by this account only.
Files must be uploaded using the multipart/form-data method.
Files uploaded using the API expire after 3 months. 
    :return: 
    """

    def upload(
        self,
        *,
        file: FileTypes,
    ) -> File:
        url = f"{self._base_url}/v1/files/upload"
        files = {"file": _try_fix_file(file)}
        return self._requester.request(
            "POST",
            url,
            False,
            cast=File,
            files=files,
        )


"""
Async API Client for files endpoints
"""


class AsyncFilesClient(object):
    def __init__(self, base_url: str, auth: Auth, requester: Requester):
        self._base_url = remove_url_trailing_slash(base_url)
        self._auth = auth
        self._requester = requester

    """
    View the details of uploaded files.
    :param file_id: Uploaded file ID.
    :return: 
    """

    async def retrieve(
        self,
        *,
        file_id: str,
    ) -> File:
        url = f"{self._base_url}/v1/files/retrieve"
        params = {
            "file_id": file_id,
        }
        return await self._requester.arequest(
            "GET",
            url,
            False,
            cast=File,
            params=params,
        )

    """
    Upload a file to the Coze platform.
**API description**
Local files cannot be directly used in messages. Before creating a message or conversation, you need to call this API to upload local files to Coze. After uploading the file, you can directly use it in multimodal content by specifying the `file_id` in the message. For usage instructions, see [Create a conversation](https://www.coze.cn/docs/developer_guides/create_conversation).

* Supported file formats:
   Document**:** DOC, DOCX, XLS, XLSX, PPT, PPTX, PDF, Numbers, and CSV
   Image**:** JPG, JPG2, PNG, GIF, WEBP, HEIC, HEIF, BMP, PCD, and TIFF
* File upload size limit:** **Each file can be up to 512 MB.
* Files uploaded to Coze can only be viewed or used by the account that uploaded them.
* Files must be uploaded using the `multipart/form-data` method.
* Files uploaded using the API expire after 3 months.
    :param file: Supported file formats for upload:
Documents: DOC, DOCX, XLS, XLSX, PPT, PPTX, PDF, Numbers, CSV
Images: JPG, JPG2, PNG, GIF, WEBP, HEIC, HEIF, BMP, PCD, TIFF
File upload size limit: Each file is a maximum of 512 MB.
Files uploaded to the platform are for viewing or use by this account only.
Files must be uploaded using the multipart/form-data method.
Files uploaded using the API expire after 3 months. 
    :return: 
    """

    async def upload(
        self,
        *,
        file: FileTypes,
    ) -> File:
        url = f"{self._base_url}/v1/files/upload"
        files = {"file": _try_fix_file(file)}
        return await self._requester.arequest(
            "POST",
            url,
            False,
            cast=File,
            files=files,
        )
