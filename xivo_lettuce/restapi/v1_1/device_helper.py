# -*- coding: UTF-8 -*-

import json
import requests
from xivo_lettuce.restapi.config import get_config_value
from xivo_lettuce.remote_py_cmd import remote_exec

AUTOPROV_URL = 'https://%s/xivo/configuration/json.php/restricted/provisioning/autoprov?act=configure'
HEADERS = {'Content-Type': 'application/json'}


def provision_device_using_webi(provcode, device_ip):
    hostname = get_config_value('xivo', 'hostname')
    data = json.dumps({'code': provcode, 'ip': device_ip})
    requests.post(url=AUTOPROV_URL % hostname,
                  headers=HEADERS,
                  auth=_prepare_auth(),
                  data=data,
                  verify=False)


def _prepare_auth():
    username = get_config_value('webservices_infos', 'login')
    password = get_config_value('webservices_infos', 'password')

    auth = requests.auth.HTTPBasicAuth(username, password)
    return auth


def delete_all():
    remote_exec(_delete_all)


def _delete_all(channel):
    from xivo_dao.data_handler.device import services as device_services

    for device in device_services.find_all():
        device_services.delete(device)


def create_device(deviceinfo):
    remote_exec(_create_device, deviceinfo=deviceinfo)


def _create_device(channel, deviceinfo):
    from xivo_dao.data_handler.device import services as device_services
    from xivo_dao.data_handler.device.model import Device

    device = Device(**deviceinfo)
    device_services.create(device)
