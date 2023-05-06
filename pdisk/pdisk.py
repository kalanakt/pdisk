# Copyright (c) 2023. kalanakt

import re
import asyncio
from typing import List
import requests
from urllib.parse import urlparse

from .type import AccountInfo, AccountStat, ClonFile, DeletedFile, File, FileInfo, Folder, FolderList, UploadResponse


class Pdisk:
    "Unofficial PDisk.pro API Wrapper By Kalanakt"

    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__base_url = 'https://pdisk.pro/api'

        if not self.__api_key:
            raise Exception("API key not provided")

    ###################### ACCOUNT ######################

    async def account_info(self) -> AccountInfo:
        url = f"{self.__base_url}/account/info?key={self.__api_key}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve account info: {response.text}")
        data = response.json()
        if data["status"] != 200:
            raise Exception(f"Failed to retrieve account info: {data['msg']}")
        result = data["result"]
        return AccountInfo(result["email"], float(result["balance"]), result["storage_used"])

    async def account_stats(self) -> List[AccountStat]:
        url = f"{self.__base_url}/account/stats?key={self.__api_key}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve account stats: {response.text}")
        data = response.json()
        if data["status"] != 200:
            raise Exception(f"Failed to retrieve account stats: {data['msg']}")
        result = data["result"]
        return [AccountStat(int(r["downloads"]), int(r["refs"]), float(r["profit_total"])) for r in result]

    ###################### UPLOAD ######################

    async def upload_server(self) -> str:
        url = f"{self.__base_url}/upload/server?key={self.__api_key}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(
                f"Failed to retrieve upload server: {response.text}")
        data = response.json()
        if data["status"] != 200:
            raise Exception(f"Failed to retrieve upload server: {data['msg']}")
        return data["result"]

    async def upload_file(self, file_path: str) -> List[UploadResponse]:
        server_url = await self.upload_server()
        files = {"file_0": open(file_path, "rb")}
        data = {"sess_id": "", "utype": "prem"}
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.post(server_url, files=files, data=data))
        if response.status_code != 200:
            raise Exception(f"Failed to upload file: {response.text}")
        data = response.json()
        return [UploadResponse(file["file_code"], file["file_status"]) for file in data]

    async def upload_remote_file(self, url: str, folder_id: int) -> List[UploadResponse]:
        upload_url = f"{self.__base_url}/upload/url?key={self.__api_key}&url={url}&fld_id={folder_id}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(upload_url))
        if response.status_code != 200:
            raise Exception(f"Failed to upload remote file: {response.text}")
        data = response.json()
        return [UploadResponse(file["file_code"], None) for file in data]

    async def check_upload_status(self, file_code: str) -> str:
        isLink = await self.is_pdisk_link(file_code)
        if isLink:
            file_code = await self.extract_file_code(file_code)

        url = f"{self.__base_url}/upload/url?key={self.__api_key}&file_code={file_code}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to check upload status: {response.text}")
        data = response.json()
        return data[0]["file_code"]

    ###################### FILE MANAGEMENT ######################

    async def file_info(self, file_code: str) -> List[FileInfo]:
        isLink = await self.is_pdisk_link(file_code)
        if isLink:
            file_code = await self.extract_file_code(file_code)

        url = f"{self.__base_url}/file/info?key={self.__api_key}&file_code={file_code}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve file info: {response.text}")
        data = response.json()
        if data["status"] != 200:
            raise Exception(f"Failed to retrieve file info: {data['msg']}")
        result = data["result"]
        return [FileInfo(
            f["filecode"], f["name"], f["status"], int(
                f["size"]), f["uploaded"], int(f["downloads"])
        ) for f in result]

    async def get_file_list(self, page: int = 1, per_page: int = 20, fld_id: int = None, public: int = None, created: str = None, name: str = None) -> List[File]:
        url = f"{self.__base_url}/file/list?key={self.__api_key}&page={page}&per_page={per_page}"
        if fld_id is not None:
            url += f"&fld_id={fld_id}"
        if public is not None:
            url += f"&public={public}"
        if created is not None:
            url += f"&created={created}"
        if name is not None:
            url += f"&name={name}"

        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve file list: {response.text}")

        data = response.json()
        if data["msg"] != "OK":
            raise Exception(f"Failed to retrieve file list: {data['msg']}")

        return [
            File(
                file_data["name"],
                file_data["file_code"],
                file_data["downloads"],
                file_data["thumbnail"],
                file_data["public"],
                file_data["size"],
                file_data["link"],
                file_data["fld_id"],
                file_data["uploaded"],
            )
            for file_data in data["result"]["files"]
        ]

    async def rename_file(self, file_code: str, new_name: str) -> bool:
        isLink = await self.is_pdisk_link(file_code)
        if isLink:
            file_code = await self.extract_file_code(file_code)

        url = f"{self.__base_url}/file/rename?key={self.__api_key}&file_code={file_code}&name={new_name}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to rename file: {response.text}")
        data = response.json()
        return data["result"]

    async def clone_file(self, file_code: str) -> ClonFile:
        isLink = await self.is_pdisk_link(file_code)
        if isLink:
            file_code = await self.extract_file_code(file_code)

        url = f"{self.__base_url}/file/clone?key={self.__api_key}&file_code={file_code}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to clone file: {response.text}")
        data = response.json()
        result = data["result"]
        return ClonFile(result["filecode"], result["url"])

    async def set_file_folder(self, file_code: str, folder_id: int):
        isLink = await self.is_pdisk_link(file_code)
        if isLink:
            file_code = await self.extract_file_code(file_code)

        url = f"{self.__base_url}/file/set_folder?file_code={file_code}&fld_id={folder_id}&key={self.__api_key}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to clone file: {response.text}")

    async def deleted_files(self, file_code: str) -> List[DeletedFile]:
        isLink = await self.is_pdisk_link(file_code)
        if isLink:
            file_code = await self.extract_file_code(file_code)

        url = f"{self.__base_url}/files/deleted?key={self.__api_key}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to clone file: {response.text}")
        data = response.json()
        result = data["result"]
        return [DeletedFile(f["deleted_ago_sec"], f["deleted"], f["file_code"], f["name"]) for f in result]

    ###################### FOLDER MANAGEMENT #######################

    async def get_folder_list(self, folder_id: int = 0) -> FolderList:
        url = f"{self.__base_url}/folder/list?key={self.__api_key}&fld_id={folder_id}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve folder list: {response.text}")
        data = response.json()
        if data["status"] != 200:
            raise Exception(f"Failed to retrieve folder list: {data['msg']}")
        result = data["result"]
        folders = [Folder(fld["fld_id"], fld["name"], fld["code"])
                   for fld in result["folders"]]
        files = [File(f["file_id"], f["name"], f["file_code"],
                      f["uploaded"], f["fld_id"]) for f in result["files"]]
        return FolderList(folders, files)

    async def create_folder(self, parent_id: int, name: str) -> int:
        url = f"{self.__base_url}/folder/create?key={self.__api_key}&parent_id={parent_id}&name={name}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to create folder: {response.text}")
        data = response.json()
        if data["status"] != 200:
            raise Exception(f"Failed to create folder: {data['msg']}")
        result = data["result"]
        return int(result["fld_id"])

    async def rename_folder(self, folder_id: int, new_name: str) -> bool:
        url = f"{self.__base_url}/folder/rename?fld_id={folder_id}&name={new_name}&key={self.__api_key}"
        response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
        if response.status_code != 200:
            raise Exception(f"Failed to rename folder: {response.text}")
        data = response.json()
        if data["status"] != 200:
            raise Exception(f"Failed to rename folder: {data['msg']}")
        return data["result"] == "true"

    @staticmethod
    async def is_pdisk_link(link: str) -> bool:
        domain = urlparse(link).netloc
        return 'pdisk.pro' in domain

    @staticmethod
    async def extract_file_code(link: str) -> bool:
        return link.replace('https://pdisk.pro/', '')
