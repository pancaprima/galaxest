import galaxest.config as config
import galaxest.adb as adb
import galaxest.labs.const as labs_const
import galaxest.locale.en as locale
from galaxest.labs.stf import Stf as StfApi

stf_api = None


def init_stf():
    global stf_api
    stf_api = StfApi(config.data.stf_host, config.data.stf_token)


if "stf" in config.data and config.data.stf:
    init_stf()

def get_devices():
    return stf_api.get_devices()

def get_disconnected_devices():
    list_disconnected = []
    user_devices = stf_api.get_user_devices()
    for key in config.data.devices_connected :
        still_connected = False
        device_connected = config.data.devices_connected[key]
        for user_device in user_devices : 
            if user_device["serial"] == key or device_connected.source != labs_const.KEY_DEVICELAB_OPENSTF :
                still_connected = True
        if not still_connected :
            list_disconnected.append(device_connected.serial)
    return list_disconnected

def print_devices():
    available_devices = get_devices()
    if len(available_devices) > 0:
        for device in available_devices:
            device_name = "%s(%s)" % (
                device["manufacturer"].strip(), device["model"].strip())
            print "%-20s\t%-10s\t%s" % (device_name, device['version'], device["serial"])  


class Stf(object):
    def __init__(self, serial):
        self.source = labs_const.KEY_DEVICELAB_OPENSTF
        self.serial = serial
        self.remote_url = None
        res = stf_api.get_device(self.serial)
        self.info = res["device"] if "device" in res else None
        self.exist = res["success"] if "success" in res else False
        if not self.info is None :
            self.name = "%s(%s)" % (self.info["manufacturer"].strip(), self.info["model"].strip())
            self.version = self.info["version"]
        if serial in config.data.devices_connected :
            self.remote_url = config.data.devices_connected[serial].adb_id

    def connect(self):
        print locale.INFO_DEVICE_CONNECTING
        if stf_api.user_use_device(self.serial):
            self.remote_url = stf_api.device_remote_connect(self.serial)
            if not self.remote_url is None:
                adb.adb_connect(self.remote_url)
                print "%s %s %s" % (
                    self.serial,
                    locale.SUCCESS_DEVICE_CONNECT,
                    self.remote_url)
                return True
            else:
                print locale.ERROR_CONNECT_ADB_KEY
        else:
            print locale.ERROR_CONNECT_DEVICE
        return False

    def disconnect(self):
        print locale.INFO_DEVICE_DISCONNECTING
        adb.adb_disconnect(self.remote_url)
        if stf_api.device_remote_disconnect(self.serial) and stf_api.user_stop_use_device(self.serial):
            adb.adb_disconnect(self.remote_url)
            print locale.SUCCESS_DEVICE_DISCONNECT
            return True
        else:
            print locale.ERROR_DISCONNECT_HUNG
        return False

    def is_available(self):
        if self.exist and self.info["owner"] is None:
            return True
        return False

    def is_exist(self):
        return self.exist
