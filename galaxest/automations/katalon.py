import subprocess
import os
import datetime
import galaxest.locale.en as locale

class App (object) :

    def __init__(self, app_path, project_path, project_file):
        self.app_name = "/katalon"
        self.app_path = app_path[:-len(self.app_name)] if app_path.endswith(self.app_name) else self.app_name
        self.project_path = project_path
        self.project_file = project_file

class Runner (object) :

    def __init__(self, katalon):
        self.katalon = katalon
        self.test_suite = None
        self.device = None
        self.run_options = None
        self.run_background = None
        self.report_path = None
        self.timestamp = None

    def run(self, test_suite, device, opts, timestamp, background):
        self.test_suite = test_suite
        self.device = device
        self.run_options = opts
        self.timestamp = timestamp
        self.run_background = background
        self.run_options = opts if not opts is None else ""
        self.report_path = self.create_report_path()
        execution_file = self.generate_test_run_files()
        print "%s %s" % (locale.INFO_KATALON_START, device.name)
        subprocess.call('"%s"' % (execution_file), shell=True)

    def generate_test_run_files(self):
        log_file = self.create_run_log_file()
        runner_file = self.create_katalon_runner(log_file)
        screen_file = self.create_screen_runner(runner_file)
        return screen_file

    def create_katalon_runner(self, log_file):
        command = './katalon --args -noSplash -runMode=console -consoleLog -testSuitePath="Test Suites/%s" -deviceId="%s" -browserType="Android" %s %s' % (
            self.test_suite, self.device.adb_id, self.get_report_folder(), self.run_options)
        if not '-projectPath=' in self.run_options :
            command = "%s -projectPath=%s" % (command, self.katalon.project_file)
        command = '%s 2>&1 | tee "%s"' % (command, log_file)
        filename = "%s/katalon_runner" % (self.report_path)
        f = open(filename, 'w+')
        f.write(
            """
        #!/bin/bash
        cd %s
        %s
        """ % (self.katalon.app_path, command)
        )
        subprocess.call('chmod +x "%s"' % (filename), shell=True)
        return filename

    def create_screen_runner(self, runner_file):
        filename = "%s/screen_runner" % (self.report_path)
        command = 'screen -dmS katalon "%s"' % (runner_file) if self.run_background else '"%s"' % (runner_file)
        f = open(filename, 'w+')

        f.write(
            """
        #!/bin/bash
        %s
        """ % (command)
        )
        subprocess.call('chmod +x "%s"' % (filename), shell=True)
        return filename

    def create_run_log_file(self):
        filename = "%s/run.log" % (self.report_path)
        subprocess.call('touch "%s"' % (filename), shell=True)
        return filename

    def get_report_folder(self):
        if not self.run_options is None and not "-reportFolder=" in self.run_options:
            return '-reportFolder="%s"' % (self.report_path)
        return ''

    def create_report_path(self):
        time_format = '%H.%M.%S %d-%m-%Y'
        report_path = "%s/Reports/%s/%s/%s_%s" % (self.katalon.project_path, self.test_suite, self.timestamp.strftime(time_format), self.device.name, self.device.serial)
        os.makedirs(report_path, 0755)
        return report_path