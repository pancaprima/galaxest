import automations
import automations.katalon as katalon
import locale.en as locale
import config
import subprocess
import time
import datetime

framework = config.data.framework if "framework" in config.data else None


def run(test_suite, devices_selected, opts=None, background=False):
    if len(devices_selected) > 1:
        background = True
    now = datetime.datetime.now()
    if framework == automations.KEY_FRAMEWORK_KATALON:
        katalon_app = katalon.App(config.data.katalon_app, config.data.katalon_project_path, config.data.katalon_project_file)
        for device in devices_selected:
            runner = katalon.Runner(katalon_app)
            runner.run(test_suite, device, opts, now, background)
    else:
        print locale.ERROR_TESTFW_NOT_FOUND


def is_using_device(local_id):
    if framework == automations.KEY_FRAMEWORK_KATALON:
        identifier = "deviceId=%s" % (local_id)
    proc = subprocess.Popen("ps xu | grep '%s' | grep -v grep | awk '{ print $2 }'" % (
        identifier), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.read()
    return True if output != "" else False

def _populate_adb_ids(devices_selected):
    adb_ids = list()
    for ds in devices_selected :
        adb_ids.append(ds.adb_id)
    return adb_ids

def wait_until_finish(devices_selected):
    automation_finish = False
    time.sleep(10)
    while not automation_finish:
        automation_finish = True
        for ds in devices_selected:
            if not 'being_used' in ds :
                ds.being_used = True
            if ds.being_used :
                ds.being_used = is_using_device(ds.adb_id)
                automation_finish = automation_finish and not ds.being_used
        if not automation_finish :
            time.sleep(30)