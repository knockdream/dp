import random
import os

from cereal import log
from selfdrive.hardware.base import HardwareBase, ThermalConfig

NetworkType = log.DeviceState.NetworkType
NetworkStrength = log.DeviceState.NetworkStrength


class Jetson(HardwareBase):


  def get_os_version(self):
    return None

  def get_device_type(self):
    return "jetson"

  def get_sound_card_online(self):
    return True

  def reboot(self, reason=None):
    os.system("sudo reboot")

  def uninstall(self):
    pass

  def get_imei(self, slot):
    return "%015d" % random.randint(0, 1 << 32)

  def get_serial(self):
    return "cccccccc"

  def get_subscriber_info(self):
    return ""

  def get_network_type(self):
    return NetworkType.wifi

  def get_sim_info(self):
    return {
      'sim_id': '',
      'mcc_mnc': None,
      'network_type': ["Unknown"],
      'sim_state': ["ABSENT"],
      'data_connected': False
    }

  def get_network_strength(self, network_type):
    return NetworkStrength.unknown

  def get_battery_capacity(self):
    return 100

  def get_battery_status(self):
    return ""

  def get_battery_current(self):
    return 0

  def get_battery_voltage(self):
    return 0

  def get_battery_charging(self):
    return True

  def set_battery_charging(self, on):
    pass

  def get_usb_present(self):
    return False

  def get_current_power_draw(self):
    return 0

  def shutdown(self):
    os.system("sudo poweroff")

  def get_thermal_config(self):
    return ThermalConfig(cpu=((None,), 1), gpu=((None,), 1), mem=(None, 1), bat=(None, 1), ambient=(None, 1))

  def set_screen_brightness(self, percentage):
    pass

  def set_power_save(self, enabled):
    pass

  def get_gpu_usage_percent(self):
    return 0

  def get_modem_version(self):
    return None

  def initialize_hardware(self):
    pass

  def get_networks(self):
    return None

  def led(self, on=False):
    os.system("echo \"268\" > /sys/class/gpio/export")
    os.system("echo \"out\" > /sys/class/gpio/gpio268/direction")
    os.system("echo \"%s\" > /sys/class/gpio/gpio268/value" % "1" if on else "0")