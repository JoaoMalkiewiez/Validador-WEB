import importlib
import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


class ValidatorWebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        mock_client = MagicMock()
        fake_supabase = types.ModuleType("supabase")
        fake_supabase.create_client = MagicMock(return_value=mock_client)
        cls.mock_client = mock_client
        cls.modules_patch = patch.dict(sys.modules, {"supabase": fake_supabase})
        cls.env_patch = patch.dict(
            os.environ,
            {"SUPABASE_URL": "https://example.supabase.co", "SUPABASE_ANON_KEY": "test-key"},
        )
        cls.modules_patch.start()
        cls.env_patch.start()
        cls.app_module = importlib.import_module("app")
        cls.client = cls.app_module.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.env_patch.stop()
        cls.modules_patch.stop()

    def setUp(self):
        self.mock_client.reset_mock()
        self.mock_client.table.return_value.select.return_value.execute.return_value.data = []

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_list_records(self):
        response = self.client.get("/criticas")
        self.assertEqual(response.status_code, 200)
        self.mock_client.table.assert_called_with("criticas")

    def test_database_error_does_not_leak_details(self):
        self.mock_client.table.side_effect = RuntimeError("private database details")
        response = self.client.get("/criticas")
        self.assertEqual(response.status_code, 500)
        self.assertNotIn(b"private database details", response.data)


if __name__ == "__main__":
    unittest.main()
