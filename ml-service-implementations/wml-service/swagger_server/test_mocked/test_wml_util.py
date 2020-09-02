# coding: utf-8

from __future__ import absolute_import

import unittest
from unittest import mock

from swagger_server.test import BaseTestCase
from swagger_server.wml_util import get_wml_credentials

from swagger_server.test_mocked.util import mock_wml_env, MOCKED_CREDENTIALS_VARS


class TestWMLUtil(BaseTestCase, unittest.TestCase):
    """WML util integration test stubs"""

    @mock_wml_env()
    @mock.patch("swagger_server.wml_util.requests.request")
    def test_get_wml_credentials(self, mock_request):
        """Test case for get_wml_credentials

        Get WML credentials
        """

        mock_request.return_value.json.return_value = {
            "access_token": "token",
            "refresh_token": "refresh_token",
            "token_type": "Bearer",
            "expires_in": 3600,
            "expiration": 1598543068,
            "scope": "ibm openid"
        }

        expected = ("{'token': 'token', 'instance_id': '" + MOCKED_CREDENTIALS_VARS['WML_INSTANCE_ID'] + "', 'url': '" + MOCKED_CREDENTIALS_VARS['WML_URL'] + "'}")

        response = get_wml_credentials()

        assert isinstance(response, object)
        assert str(response) == expected, 'response is not matching expected response'

        mock_request.assert_called_once_with("POST", 'https://iam.cloud.ibm.com/identity/token', data='grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=apikey', headers=mock.ANY)