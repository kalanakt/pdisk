from typing import List

class AccountInfo:
    "Object representing account information"

    def __init__(self, email: str, balance: float, storage_used: float or None):
        self.email = email
        self.balance = balance
        self.storage_used = None if storage_used is None else float(
            storage_used)


class AccountStat:
    "Object representing account statistics"

    def __init__(self, downloads: int, refs: int, profit_total: float):
        self.downloads = downloads
        self.refs = refs
        self.profit_total = profit_total


class UploadResponse:
    "Object representing uploaded file information"

    def __init__(self, file_code: str, file_status: str):
        self.file_code = file_code
        self.file_status = file_status


class FileInfo:
    "Object representing file information"

    def __init__(self, file_code: str, name: str, status: int, size: int, uploaded: str, downloads: int):
        self.file_code = file_code
        self.name = name
        self.status = status
        self.size = size
        self.uploaded = uploaded
        self.downloads = downloads


class File:
    "Object representing file"

    def __init__(self, name: str, file_code: str, downloads: int, thumbnail: str, public: int, size: int, link: str, fld_id: int, uploaded: str):
        self.name = name
        self.file_code = file_code
        self.downloads = downloads
        self.thumbnail = thumbnail
        self.public = public
        self.size = size
        self.link = link
        self.fld_id = fld_id
        self.uploaded = uploaded

class Folder:
    "Object representing a folder"

    def __init__(self, id: int, name: str, code: str or None):
        self.id = id
        self.name = name
        self.code = code

class FolderList:
    "Object representing the list of folders and files in a folder"

    def __init__(self, folders: List[Folder], files: List[File]):
        self.folders = folders
        self.files = files

class ClonFile:
    "Object representing cloned file information"

    def __init__(self, file_code: str, url: str):
        self.file_code = file_code
        self.url = url

class DeletedFile:
    "Object representing deleted file information"

    def __init__(self, deleted_ago_sec: int, deleted: str, file_code: str, name: str):
        self.deleted_ago_sec = deleted_ago_sec
        self.deleted = deleted
        self.file_code = file_code
        self.name = name