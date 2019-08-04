import time
import labs.const as labs_const
import config
import automation
import locale.en as locale
import parallel
from parallel import ParallelType

import devices.stf

sources = config.data.device_sources if "device_sources" in config.data else None

def init(device_id):
    for source in sources:
        if source == labs_const.KEY_DEVICELAB_OPENSTF:
            device = devices.stf.Stf(device_id)
            if device.is_exist():
                return device
    return None

def get_available_devices():
    available_devices = []
    for source in sources:
        if source == labs_const.KEY_DEVICELAB_OPENSTF:
            available_devices = available_devices + devices.stf.get_devices()
    return available_devices

def print_available_devices():
    print "[OpenSTF]"
    print "%-20s\t%-10s\t%s" % ("[Device Name]", "[Version]", "[Device ID]")
    devices.stf.print_devices()

def print_my_devices():
    check_connected_devices()
    devices = config.data.devices_connected
    print "%-10s\t%-20s\t%-10s\t%-20s\t%s" % (
        "[Source]", "[Device Name]", "[Version]", "[Device ID]", "[ADB ID]",)
    for key in devices:
        device = devices[key]
        source = device.source if "source" in device else None
        name = device.name if "name" in device else None
        version = device.version if "version" in device else None
        serial = device.serial if "serial" in device else None
        adb_id = device.adb_id if "adb_id" in device else None
        print "%-10s\t%-20s\t%-10s\t%-20s\t%s" % (source,name,version,serial,adb_id)

def connect(device):
    if device.is_available():
        connected_device = _create_connection(device)
        if not connected_device is None:
            return connected_device
    else:
        print locale.ERROR_DEVICE_UNAVAILABLE
    return None

def check_connected_devices():
    for source in sources:
        list_disconnected = []
        if source == labs_const.KEY_DEVICELAB_OPENSTF:
            list_disconnected = list_disconnected + devices.stf.get_disconnected_devices()
    for serial in list_disconnected:
        del config.data.devices_connected[serial]

def find_devices_to_run(parallel_type, parallel_specs):
    devices_selected = list()
    if not parallel_type is None :
        parallel_execution = parallel.ParallelExecution(parallel_type, parallel_specs)
        devices_selected = auto_choose_device(parallel_execution)
    else :
        any_spec = parallel.ParallelExecution(parallel.ParallelType.AMOUNT, 1)
        devices_selected = auto_choose_device(any_spec)
    return devices_selected

def auto_choose_device(parallel_data, use_connected_devices=True):
    devices_selected = []
    if use_connected_devices :
        devices_selected = _use_connected_devices(parallel_data, devices_selected)
    devices_selected = _use_available_devices(parallel_data, devices_selected)
    return devices_selected

def _is_connected_device_usable(device_connected):
    if not automation.is_using_device(device_connected.adb_id):
        return True
    return False

def _is_device_spec_match(parallel_data, desired_device):
    spec_match = True
    spec = None
    if parallel_data.type_val != ParallelType.AMOUNT :
        spec_match = False
        for i_spec in parallel_data.specs :
            if _is_spec_match(parallel_data.type_val, i_spec, desired_device) :
                spec = i_spec
                spec_match = True
    return spec_match, spec

def _is_spec_match(parallel_type, spec, desired_device):
    if parallel_type == ParallelType.OS and desired_device.version.startswith(spec) :
        return True
    elif parallel_type == ParallelType.DEVICE_ID and desired_device.serial == spec :
        return True
    return False
        

def _use_connected_devices(parallel_data, devices_selected=[]):
    check_connected_devices()
    if len(config.data.devices_connected) > 0:
        for key in config.data.devices_connected:
            if len(devices_selected) < parallel_data.specs_amount:
                device_connected = config.data.devices_connected[key]
                spec_match, spec = _is_device_spec_match(parallel_data, device_connected) 
                if spec_match and _is_connected_device_usable(device_connected):
                    parallel_data.remove_spec(spec)
                    devices_selected.append(device_connected)
            else : break
    return devices_selected

def _use_available_devices(parallel_data, devices_selected=[]):
    if len(devices_selected) < parallel_data.specs_amount:
        available_devices = get_available_devices()
        n_more_devices = parallel_data.specs_amount - len(devices_selected)
        if len(available_devices) >= n_more_devices:
            counter_device = 0
            for x in range(0, n_more_devices):
                device_found = False
                while not device_found and counter_device < len(available_devices):
                    serial = available_devices[counter_device]["serial"]
                    desired_device = init(serial)
                    spec_match, spec = _is_device_spec_match(parallel_data, desired_device)
                    if spec_match and desired_device.is_available():
                        connected_device = connect(desired_device)
                        if not connected_device is None:
                            parallel_data.remove_spec(spec)
                            devices_selected.append(
                                config.data.devices_connected[serial])
                            device_found = True
                    counter_device += 1
    return devices_selected

def _register_connected_device(device):
    if not "devices_connected" in config.data:
        config.data.devices_connected = dict()
    config.data.devices_connected[device.serial] = {
        "serial": device.serial,
        "adb_id": device.remote_url,
        "version": device.version,
        "name": device.name,
        "source": device.source
    }
    config.data.save()
    return config.data.devices_connected[device.serial]


def _create_connection(device):
    connection_status = device.connect()
    if connection_status:
        just_registered_device = _register_connected_device(device)
        return just_registered_device
    return None
