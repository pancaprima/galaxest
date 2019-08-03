import subprocess
import os
import time


def run(app_path, project_path, project_file, test_suite, device_id, opts, background):
    project_file = "%s/%s" % (project_path, project_file)
    opts = opts if not opts is None else ""
    timestamp = int(time.time())
    prefix_id = "T"
    report_path = "%s/Reports/%s/%s%s__%s" % (
            project_path, test_suite, prefix_id, timestamp, device_id.replace(":","_"))
    log_file = "%s/run.log" % (report_path)
    runner_file = "%s/katalon_runner" % (report_path)
    screen_file = "%s/screen_runner" % (report_path)
    command = './katalon --args -noSplash -runMode=console -consoleLog -projectPath="%s" -testSuitePath="Test Suites/%s" -deviceId="%s" -browserType="Android" %s %s ' % (
        project_file, test_suite, device_id, get_report_folder(report_path, opts), opts)
    command_logged = '%s 2>&1 | tee "%s"' % (command, log_file)

    os.makedirs(report_path, 0755)
    create_katalon_runner(runner_file, app_path, command_logged)
    subprocess.call('touch "%s"' % (log_file), shell=True)
    if background:
        create_screen_runner(
            screen_file, 'screen -dmS katalon "%s"' % (runner_file))
    else:
        screen_command = '"%s"' % (runner_file)
        create_screen_runner(screen_file, screen_command)
    subprocess.call('"%s"' % (screen_file), shell=True)


def create_katalon_runner(filename, app_path, command):
    f = open(filename, 'w+')

    app_name = "/katalon"
    app_path = app_path[:-len(app_name)] if app_path.endswith(app_name) else app_name

    f.write(
        """
      #!/bin/bash
      cd %s
      %s
      """ % (app_path, command)
    )
    subprocess.call('chmod +x "%s"' % (filename), shell=True)


def create_screen_runner(filename, command):
    f = open(filename, 'w+')

    f.write(
        """
      #!/bin/bash
      %s
      """ % (command)
    )
    subprocess.call('chmod +x "%s"' % (filename), shell=True)

def get_report_folder(report_path, opts):
    if not opts is None and not "-reportFolder=" in opts :
        return '-reportFolder="%s"' % (report_path)
    return ''