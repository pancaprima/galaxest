import sys
import json
import device
import automation
import setup
import config
import time
import locale.en as locale

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
        device.available_devices()
        sys.exit(0)

    if options.want_my_devices:
        device.my_devices()
        sys.exit(0)

    # --connect or --disconnect
    if options.want_connect or options.want_disconnect:
        if options.want_connect and options.want_disconnect:
            print locale.ERROR_CD_TOGETHER
        else:
            if not options.device_id is None:
                desired_device = device.init(options.device_id)
                if options.want_connect:
                    device.connect(desired_device)
                else:
                    if options.device_id in config.data.devices_connected :
                        desired_device.remote_url = config.data.devices_connected[options.device_id]["adb_id"]
                        desired_device.disconnect()
                        device.check_connected_devices()
                    elif not options.local_id is None:
                        desired_device.remote_url = options.local_id
                        desired_device.disconnect()
                        device.check_connected_devices()
                    else:
                        print locale.ERROR_CD_NO_ID
            else:
                print locale.HELP_DEVICE_ID
    
    # --run
    if not options.test_suite is None :
        device_selected = list()
        parallel_run = False
        if not options.parallel_number is None :
            devices_selected = device.auto_choose_device(n=options.parallel_number)
        elif not options.parallel_os is None :
            parallel_os = options.parallel_os.split(',')
            devices_selected = device.auto_choose_device(os_versions=parallel_os)
        elif not options.device_id is None :
            device.check_connected_devices()
            device_ids = options.device_id.split(',')
            for device_id in device_ids :
                if options.device_id in config.data.devices_connected :
                    devices_selected.append(config.data.devices_connected[options.device_id])
                else :
                    desired_device = device.init(options.device_id)
                    devices_selected.append(device.connect(desired_device))
                if device_selected is None :
                    print locale.ERROR_CONNECT_DEVICE
        elif options.any_device is True or options.local_id is None :
            devices_selected = device.auto_choose_device(n=1)
 
        if len(devices_selected) > 1 :
            parallel_run = True
            adb_ids = list()
            for ds in devices_selected :
                adb_ids.append(ds.adb_id)
            options.local_id = ','.join(adb_ids)
        elif len(devices_selected) == 1:
            options.local_id =  devices_selected[0].adb_id

        if not options.local_id is None :
            if not automation.is_using_device(options.local_id) :
                automation.run(options.test_suite, options.local_id, options.opts, parallel_run)
                # Disconnect if automation finish
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
            else :
                print locale.ERROR_DEVICE_BUSY
        else :
            print locale.ERROR_DEVICE_NOT_FOUND