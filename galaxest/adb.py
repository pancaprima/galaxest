import subprocess


def adb_connect(device_id):
    subprocess.call("adb connect %s" % (device_id), shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def adb_disconnect(device_id):
    subprocess.call("adb disconnect %s" % (device_id), shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
