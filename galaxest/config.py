import json, subprocess
from tweak import Config

data = Config(name="galaxest")

def show_config():
    configuration = data
    proc = subprocess.Popen("cat %s/config.json" % (configuration.user_config_dir), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print json.dumps(json.loads(str(proc.stdout.read())), indent=4, sort_keys=True)
