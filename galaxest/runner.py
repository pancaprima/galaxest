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
            desired_device = device.init(options.device_id_to_disconnect)
            desired_device.remote_url = config.data.devices_connected[options.device_id_to_disconnect]["adb_id"]
            desired_device.disconnect()
            device.check_connected_devices()
        else :
            print locale.ERROR_DISCONNECT_ID_NOT_FOUND
    
    # --run
    if not options.test_suite is None :
        devices_selected = list()
        devices_selected = device.find_devices_to_run(options.parallel_type, options.parallel_specs)
        adb_ids = _populate_adb_ids(devices_selected)
        if not adb_ids is None :
            automation.run(options.test_suite, adb_ids, options.opts)
            if not options.skip_disconnect :
                _watch_to_disconnect(devices_selected)
        else :
            print locale.ERROR_DEVICE_NOT_FOUND

def _watch_to_disconnect(devices_selected):
    automation_finish = False
    time.sleep(10)
    while not automation_finish:
        automation_finish = True
        for ds in devices_selected:
            if not 'being_used' in ds :
                ds.being_used = True
            if ds.being_used :
                ds.being_used = automation.is_using_device(ds.adb_id)
                automation_finish = automation_finish and not ds.being_used
                if not ds.being_used :
                    device.init(ds.serial).disconnect()
                    device.check_connected_devices()
        if not automation_finish :
            time.sleep(30)

def _populate_adb_ids(devices_selected):
    adb_ids = list()
    for ds in devices_selected :
        adb_ids.append(ds.adb_id)
    return adb_ids

