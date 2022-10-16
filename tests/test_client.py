"""
This file contains tests for functions in client.py
"""

import unittest
from client import client


class TestPrepareResponse(unittest.TestCase):
    def test_prepare_response_returns_a_valid_response(self):
        self.assertEqual(client.prepare_response([2, 3]), b'[2, 3]\n')


if __name__ == '__main__':
    unittest.main()
