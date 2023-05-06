# PDisk.pro API Wrapper
>A Python package to interact with the unofficial API of PDisk.pro.


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