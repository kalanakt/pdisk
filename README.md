<p align="center">
  <a href="http://nestjs.com/" target="blank"><img src="https://pdisk.pro/img-custom/logo-s.png" width="120" alt="Nest Logo" /></a>
</p>
  <h1 align="center">pdisk</h1>
  <p align="center">A Python package to interact with the unofficial API of PDisk.pro.</p>
    <p align="center">
<!-- <p align='center'>
  <img alt="GitHub Sparkline" src="https://github.com/gramscript/gramscript">
</p> -->
        <a href=""><img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/kalanakt/pdisk?logo=files&logoColor=f72585"></a>
        <a href="https://github.com/kalanakt/pdisk" target="_blank"><img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/kalanakt/pdisk?color=8eecf5&logo=anaconda&logoColor=06d6a0"></a>
        <a href="https://github.com/kalanakt/pdisk" target="_blank"><img alt="GitHub" src="https://img.shields.io/github/license/kalanakt/pdisk?logo=adguard&logoColor=390099"></a>
        <a href="https://github.com/kalanakt/pdisk" target="_blank"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/kalanakt/pdisk?color=90e0ef&logoColor=ff4d6d"></a>
        <a href="https://github.com/kalanakt/pdisk"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/kalanakt/pdisk?logo=electron&logoColor=89fc00"></a>
        <a href="https://pypi.org/project/pdisk/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pdisk?logo=adguard&logoColor=89fc00"></a>
        <a href="https://github.com/kalanakt/pdisk"><img alt="GitHub" src="https://img.shields.io/github/license/kalanakt/pdisk?logo=adguard&logoColor=89fc00"></a>
        <a href="https://pypi.org/project/pdisk"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/pdisk?color=06d6a0&logo=adguard&logoColor=89fc00"></a>
        <a href="https://github.com/kalanakt/pdisk"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/kalanakt/pdisk?color=06d6a0&logo=adguard&logoColor=89fc00"></a>
        <a href="https://pypi.org/project/pdisk/"><img alt="PyPI - Format" src="https://img.shields.io/pypi/format/pdisk"></a>
        <a href="https://github.com/kalanakt/pdisk"><img alt="Sourcegraph for Repo Reference Count" src="https://img.shields.io/sourcegraph/rrc/https://github.com/kalanakt/pdisk"></a>
        <a href="https://github.com/kalanakt/pdisk"><img alt="Maintenance" src="https://img.shields.io/maintenance/yes/2023"></a></p>
        
## Installation
> To install the package, you can use pip:

```bash
pip install pdisk
```

## Usage
>To use the package, you must first create an instance of the Pdisk class, passing your API key as a parameter:

```python
from pdisk import Pdisk

api_key = "YOUR_API_KEY_HERE"
pdisk = Pdisk(api_key)
```

## Account
>You can retrieve your account info and stats using the following methods:

```python
account_info = await pdisk.account_info()
print(account_info.email, account_info.balance, account_info.storage_used)

account_stats = await pdisk.account_stats()
for stat in account_stats:
    print(f"{stat.profit_total} : {stat.downloads} : {stat.refs}")
```

## File Upload
>You can upload files using the following methods:

```python
# Upload a file from local storage
responses = await pdisk.upload_file("/path/to/file")
for response in responses:
    print(response)

# Upload a remote file
responses = await pdisk.upload_remote_file("https://example.com/file.mp4", folder_id=12345)
for response in responses:
    print(response)
```

>You can check the upload status of a file using the following method:

```python
file_code = "FILE_CODE"
status = await pdisk.check_upload_status(file_code)
print(status)
```

## File Management
>You can retrieve information about a file using the following method:

```python
file_code = "FILE_CODE"
file_info = await pdisk.file_info(file_code)
for info in file_info:
    print(info)
```

>You can also retrieve a list of files using the following method:

```python
files = await pdisk.get_file_list(page=1, per_page=20)
for file in files:
    print(file)
```

Check Documentaion For More ... `comming soon ...`

## License
_`This project is licensed under the MIT License (c) 2023 kalanakt.`_
