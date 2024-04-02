import asyncio
import datetime
import logging

import boto3
import requests
from dateutil import tz

_LOGGER = logging.getLogger(__name__)


def _get_last_updated_remote(token: str):
    headers = {
        'authorization': 'Bearer ' + token,
    }

    raw_data = '{"method":"get-profile-summary","limit":"500"}'
    resp = requests.post('https://api.tracker-suivi.apps.cic.gc.ca/user', data=raw_data, headers=headers).json()
    return resp['lastUpdated']


def _auth(uci: str, pwd: str):
    client = boto3.client('cognito-idp', 'ca-central-1')
    resp = client.initiate_auth(
        ClientId="mtnf1qn9p739g2v8aij2anpju",
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            "USERNAME": uci,
            "PASSWORD": pwd,
        }
    )

    return resp['AuthenticationResult']['IdToken']


class ApiClient(object):
    application_updated_at: datetime.datetime

    data_synced_at: datetime.datetime

    def __init__(self, uci: str, pwd: str):
        self.__uci = uci
        self.__pwd = pwd

    async def update(self):
        _LOGGER.info(f"Updating data for {self.__uci[-4:]}")

        token = await asyncio.to_thread(_auth, self.__uci, self.__pwd)
        if token:
            epoch_ms = await asyncio.to_thread(_get_last_updated_remote, token)
            self.application_updated_at = datetime.datetime.fromtimestamp(epoch_ms / 1000, tz.UTC)
            self.data_synced_at = datetime.datetime.now(tz.UTC)
            return True

        return False
