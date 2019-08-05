import sys
import json
import device
import automation
import setup
import config
import time
import locale.en as locale
import parallel

options = None

def run():
    # --show-config
    if options.want_show_config:
        config.show_config()
        sys.exit(0)

    # --reset-config
    if options.want_reset_config:
        config.data.reset = True

    # check if configuration had configured
    config_blank = True
    if config.data and "reset" in config.data and config.data.reset is False:
        config_blank = False
    if config_blank:
        setup.init()
    
    if not "devices_connected" in config.data :
        config.data.devices_connected = {}

    # --devices
    if options.want_list_devices:
        device.print_available_devices()
        sys.exit(0)

    if options.want_my_devices:
        device.print_my_devices()
        sys.exit(0)

    # --connect
    if options.want_connect != False :
        if options.want_connect == True :
            any_spec = parallel.ParallelExecution(parallel.ParallelType.AMOUNT, 1)
            devices_selected = device.auto_choose_device(any_spec, False)
        else :
            desired_device = device.init(options.want_connect)
            device.connect(desired_device)

    # --disconnect
    if not options.device_id_to_disconnect is None :
        if options.device_id_to_disconnect in config.data.devices_connected :
            device.disconnect(options.device_id_to_disconnect)
        else :
            print locale.ERROR_DISCONNECT_ID_NOT_FOUND
    
    # --run
    if not options.test_suite is None :
        devices_selected = list()
        devices_selected = device.find_devices_to_run(options.parallel_type, options.parallel_specs)
        if len(devices_selected) > 0 :
            automation.run(options.test_suite, devices_selected, options.opts)
            if not options.skip_disconnect :
                automation.wait_until_finish(devices_selected)
                for ds in devices_selected :
                    device.disconnect(ds.serial)
        else :
            print locale.ERROR_DEVICE_NOT_FOUND



