import automations.const as automations_const
import automations.katalon as katalon
import locale.en as locale
import config
import subprocess

framework = config.data.framework if "framework" in config.data else None


def run(test_suite, adb_ids, opts=None, background=False):
    if len(adb_ids) > 1:
        background = True
    if framework == automations_const.KEY_FRAMEWORK_KATALON:
        for adb_id in adb_ids:
            katalon.run(config.data.katalon_app, config.data.katalon_project_path,
                        config.data.katalon_project_file, test_suite, adb_id, opts, background)
    else:
        print locale.ERROR_TESTFW_NOT_FOUND


def is_using_device(local_id):
    if framework == automations_const.KEY_FRAMEWORK_KATALON:
        identifier = "deviceId=%s" % (local_id)
    proc = subprocess.Popen("ps xu | grep '%s' | grep -v grep | awk '{ print $2 }'" % (
        identifier), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.read()
    return True if output != "" else False
