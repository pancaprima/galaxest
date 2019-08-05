import subprocess


def connect(device_id):
    subprocess.call("adb connect %s" % (device_id), shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def disconnect(device_id):
    subprocess.call("adb disconnect %s" % (device_id), shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
