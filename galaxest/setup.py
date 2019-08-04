import inquirer
import labs.const as labs_key
import automations.const as automations_key
import devices.stf as stf
import config
import locale.en as locale


def init():
    setup_status = True
    print locale.INFO_SETUP_FIRST
    print locale.INFO_SETUP_SUB
    reset_q = [
        inquirer.List("ready",
                      message=locale.INFO_PROMPT_READY,
                      choices=[locale.INFO_YES, locale.INFO_NO]
                      )
    ]
    reset_answers = inquirer.prompt(reset_q)
    if reset_answers["ready"] == locale.INFO_NO:
        config.data.reset = False
        return False
    
    if setup_status:
        device_sources_q_key = "device_sources"
        device_sources_q = [
            inquirer.Checkbox(device_sources_q_key,
                              message=locale.INFO_SETUP_Q_DEVICE_FARM,
                              choices=[labs_key.KEY_DEVICELAB_OPENSTF]
                              )
        ]
        device_sources_answers = inquirer.prompt(device_sources_q)
        config.data.device_sources = device_sources_answers[device_sources_q_key]
        setup_status = setup_device_sources()

    if setup_status:
        framework_q_key = "framework"
        framework_q = [
            inquirer.List(framework_q_key,
                        message=locale.INFO_SETUP_Q_TEST_FW,
                        choices=[automations_key.KEY_FRAMEWORK_KATALON]
                        )
        ]
        framework_answers = inquirer.prompt(framework_q)
        config.data.framework = framework_answers[framework_q_key]
        setup_status = setup_automation()

    if setup_status:
        config.data.reset = False
        print locale.SUCCESS_SETUP

    return setup_status

def setup_automation():
    setup_status = True
    if config.data.framework == automations_key.KEY_FRAMEWORK_KATALON :
        setup_status = setup_katalon()
    return setup_status

def setup_katalon():
    setup_status = True
    init_katalon_q = [
        inquirer.Text('katalon_path',
                      message=locale.INFO_SETUP_Q_KATALON_PATH,
                      default=config.data.katalon_app if "katalon_app" in config.data else None
                      ),
        inquirer.Text('project_path',
                      message=locale.INFO_SETUP_Q_KATALON_PROJECT_PATH,
                      default=config.data.katalon_project_path if "katalon_project_path" in config.data else None
                      ),
        inquirer.Text('project_name',
                      message=locale.INFO_SETUP_Q_KATALON_PROJECT_NAME,
                      default=config.data.katalon_project_file if "katalon_project_file" in config.data else None
                      )
    ]
    init_katalon_answers = inquirer.prompt(init_katalon_q)
    config.data.katalon_app = init_katalon_answers["katalon_path"] if not init_katalon_answers["katalon_path"].endswith(".app") else '%s/Contents/MacOS/katalon' % (init_katalon_answers["katalon_path"])
    config.data.katalon_project_path = init_katalon_answers["project_path"] if not init_katalon_answers["project_path"].endswith('/') else init_katalon_answers["project_path"][:-1]
    config.data.katalon_project_file = init_katalon_answers["project_name"] if init_katalon_answers["project_name"].endswith(".prj") else '%s.prj' % (init_katalon_answers["project_name"])
    config.data.katalon = True
    return setup_status

def setup_device_sources():
    setup_status = True
    for source in config.data.device_sources:
        if source == labs_key.KEY_DEVICELAB_OPENSTF:
            setup_status = setup_stf()
    return setup_status

def setup_stf():
    setup_status = True
    init_stf_q = [
        inquirer.Text('host',
                      message=locale.INFO_SETUP_Q_STF_HOST,
                      default=config.data.stf_host if "stf_host" in config.data else None
                      ),
        inquirer.Text('token',
                      message=locale.INFO_SETUP_Q_STF_TOKEN,
                      default=config.data.stf_token if "stf_token" in config.data else None
                      ),
    ]
    init_stf_answers = inquirer.prompt(init_stf_q)
    config.data.stf_host = init_stf_answers["host"]
    config.data.stf_token = init_stf_answers["token"]
    config.data.stf = True
    stf.init_stf()
    print locale.INFO_SETUP_STF_TEST_CONN
    if not stf.stf_api.healthy():
        print locale.ERROR_STF_TEST_CONN
        setup_status = False
    print ""
    return setup_status
