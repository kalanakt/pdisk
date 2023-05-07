import unittest
from unittest.mock import patch, MagicMock
from pdisk import Pdisk, AccountInfo, AccountStat, UploadResponse, FileInfo
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TestPdisk(unittest.TestCase):
    def setUp(self):
        api_key = os.environ.get("API")
        self.pdisk = Pdisk(self.api_key)

    @patch('pdisk.requests.get')
    async def test_account_info(self, mock_get):
        expected_result = {
            "status": 200,
            "result": {
                "email": "test@test.com",
                "balance": "10.00",
                "storage_used": "0"
            }
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_result
        mock_get.return_value = mock_response

        result = await self.pdisk.account_info()

        self.assertIsInstance(result, AccountInfo)
        self.assertEqual(result.email, expected_result['result']['email'])
        self.assertEqual(result.balance, float(
            expected_result['result']['balance']))
        self.assertEqual(result.storage_used,
                         expected_result['result']['storage_used'])

    @patch('pdisk.requests.get')
    async def test_account_stats(self, mock_get):
        expected_result = {
            "status": 200,
            "result": [
                {
                    "downloads": "10",
                    "refs": "5",
                    "profit_total": "5.00"
                },
                {
                    "downloads": "20",
                    "refs": "10",
                    "profit_total": "10.00"
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_result
        mock_get.return_value = mock_response

        result = await self.pdisk.account_stats()

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], AccountStat)
        self.assertEqual(result[0].downloads, int(
            expected_result['result'][0]['downloads']))
        self.assertEqual(result[0].refs, int(
            expected_result['result'][0]['refs']))
        self.assertEqual(result[0].profit_total, float(
            expected_result['result'][0]['profit_total']))

    @patch('pdisk.requests.get')
    async def test_upload_server(self, mock_get):
        expected_result = {
            "status": 200,
            "result": "https://srv1.pdisk.pro/upload"
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_result
        mock_get.return_value = mock_response

        result = await self.pdisk.upload_server()

        self.assertIsInstance(result, str)
        self.assertEqual(result, expected_result['result'])

    @patch('builtins.open')
    @patch('pdisk.Pdisk.upload_server')
    @patch('pdisk.requests.post')
    async def test_upload_file(self, mock_post, mock_upload_server, mock_open):
        # Simulate file upload
        filename = 'test_file.txt'
        file_contents = b'This is a test file.'
        expected_response = {'status': 'success'}

        mock_open.return_value.__enter__.return_value.read.return_value = file_contents
        mock_post.return_value.json.return_value = expected_response

        # Call the function being tested
        response = await self.upload_file(filename, mock_upload_server)

        # Check that the file was opened and read correctly
        mock_open.assert_called_once_with(filename, 'rb')
        mock_open.return_value.__enter__.return_value.read.assert_called_once_with()

        # Check that the file was uploaded to the correct URL
        mock_upload_server.assert_called_once_with('/upload')
        mock_post.assert_called_once_with(
            mock_upload_server.return_value, files={'file': file_contents})

        # Check that the function returned the expected response
        assert response == expected_response
