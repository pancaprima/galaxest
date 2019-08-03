import devices.stf
import time
import labs.const as labs_const
import config
import automation
import locale.en as locale

sources = config.data.device_sources if "device_sources" in config.data else None

def init(device_id):
    for source in sources:
        if source == labs_const.KEY_DEVICELAB_OPENSTF:
            device = devices.stf.Stf(device_id)
            if device.is_exist():
                return device
    return None


def register_connected_device(device):
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


def create_connection(device):
    connection_status = device.connect()
    if connection_status:
        just_registered_device = register_connected_device(device)
        return just_registered_device
    return None


def connect(device):
    if device.is_available():
        connected_device = create_connection(device)
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


def auto_choose_device(n=1,os_versions=None):
    devices_selected = []
    check_connected_devices()
    by_os = True if not os_versions is None else False
    
    # set length of needed number of devices if auto choose not by n
    if by_os :
        n = len(os_versions)
    n = int(n)

    # check from already connected devices
    if len(config.data.devices_connected) > 0:
        counter = 0
        for key in config.data.devices_connected:
            if counter < n:
                device_connected = config.data.devices_connected[key]
                use_device = True
                if by_os :
                    use_device = False
                    for os in os_versions :
                        if device_connected.version.startswith(os) :
                            os_versions.remove(os)
                            use_device = True
                if use_device and not automation.is_using_device(device_connected.adb_id):
                    devices_selected.append(device_connected)
            else:
                break
            counter += 1

    # Check if still need more devices to be connected
    if len(devices_selected) < n:
        available_devices = []

        # Collect all available devices
        for source in sources:
            if source == labs_const.KEY_DEVICELAB_OPENSTF:
                available_devices = available_devices + devices.stf.stf_api.get_devices()

        # Connecting to the available devices to fulfill the desired amount of devices
        n_more_devices = n - len(devices_selected)
        if len(available_devices) >= n_more_devices:
            counter_device = 0
            for x in range(0, n_more_devices):
                device_found = False
                while not device_found and counter_device < len(available_devices):
                    serial = available_devices[counter_device]["serial"]
                    desired_device = init(serial)
                    use_device = True
                    if by_os :
                        use_device = False
                        for os in os_versions :
                            if desired_device.version.startswith(os) :
                                os_versions.remove(os)
                                use_device = True
                    if use_device and desired_device.is_available():
                        connected_device = create_connection(desired_device)
                        if not connected_device is None:
                            devices_selected.append(
                                config.data.devices_connected[serial])
                            device_found = True
                    counter_device += 1
    return devices_selected


def available_devices():
    print "[OpenSTF]"
    print "%-20s\t%-10s\t%s" % ("[Device Name]", "[Version]", "[Device ID]")
    devices.stf.get_devices()


def my_devices():
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
