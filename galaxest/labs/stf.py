import requests
import galaxest.locale.en as locale

class Stf(object):

    def __init__(self, host, token):
        self.host = host if host[len(host)-1] == '/' else '%s/' % (host)
        self.token = token
        self.user = None
        self.adb_key_exist = False
        self.auth = "Bearer %s" % (self.token)

    def healthy(self):
        if not self.host is None and not self.token is None:
            self.user = self.get_user()
            if not self.user is None:
                print "%s %s (%s)" % (
                    locale.INFO_LOGGED_IN, self.user["name"], self.user["email"])
                if len(self.user["adbKeys"]) > 0:
                    self.adb_key_exist = True
                    return True
                else:
                    print locale.ERROR_ADB_KEY_NOT_FOUND
        else:
            print locale.ERROR_STF_CONFIG
        return False

    def get_user(self):
        headers = {
            "Authorization": self.auth
        }
        path = "api/v1/user"
        res = requests.get(self.host+path, headers=headers).json()
        if "success" in res and res["success"] and "user" in res:
            return res["user"]
        else:
            return None

    def get_devices(self):
        headers = {
            "Authorization": self.auth
        }
        path = "api/v1/devices"
        res = requests.get(self.host+path, headers=headers).json()
        available_devices = list()
        if "success" in res and res["success"] and "devices" in res:
            devices = res["devices"]
            for device in devices:
                if device["ready"] and device["present"] and device["owner"] is None:
                    available_devices.append(device)
        else:
            print "failed to get list of devices"
        return available_devices

    def get_device(self, serial):
        headers = {
            "Authorization": self.auth
        }
        path = "api/v1/devices/%s" % (serial)
        return requests.get(self.host+path, headers=headers).json()

    def get_user_devices(self):
        headers = {
            "Authorization": self.auth
        }
        path = "api/v1/user/devices"
        res = requests.get(self.host+path, headers=headers).json()
        user_devices = list()
        if "success" in res and res["success"] and "devices" in res:
            user_devices = res["devices"]
        else:
            print locale.ERROR_STF_FETCH_DEVICES
        return user_devices

    def user_use_device(self, serial):
        headers = {
            "Authorization": self.auth
        }
        body = {
            "serial": serial
        }
        path = "api/v1/user/devices"
        res = requests.post(self.host+path, headers=headers, json=body).json()
        if "success" in res and res["success"]:
            return True
        else:
            print res["description"] if "description" in res else locale.ERROR_STF_USE_DEVICE
            return False

    def user_stop_use_device(self, serial):
        headers = {
            "Authorization": self.auth
        }
        path = "api/v1/user/devices/%s" % serial
        res = requests.delete(self.host+path, headers=headers).json()
        if "success" in res and res["success"]:
            return True
        else:
            print locale.ERROR_STF_STOP_DEVICE
            return False

    def device_remote_connect(self, serial):
        headers = {
            "Authorization": self.auth
        }
        path = "api/v1/user/devices/%s/remoteConnect" % (serial)
        res = requests.post(self.host+path, headers=headers).json()
        return res["remoteConnectUrl"] if "remoteConnectUrl" in res else None

    def device_remote_disconnect(self, serial):
        headers = {
            "Authorization": self.auth
        }
        path = "api/v1/user/devices/%s/remoteConnect" % (serial)
        res = requests.delete(self.host+path, headers=headers).json()
        return True if "success" in res and res["success"] else False
