from client_functions import *

#from broadcaster import *

class VebusState:
    Off, Low_Power, Fault, Bulk, Absorption, Float, Storage, Equalize, Passthru, Inverting, Power_assist, Power_supply, Bulk_protection = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 252]

class VebusError:
    # Error 1: Device is switched off because one of the other phases in the system has switched off
    # Error 2: New and old types MK2 are mixed in the system
    # Error 3: Not all, or more than, the expected devices were found in the system
    # Error 4: No other device whatsoever detected
    # Error 5: Overvoltage on AC-out
    # Error 6: in DDC Program
    # Error 7: BMS connected, which requires an Assistant, but no assistant found;
    # Error 10: System time synchronisation problem occurred
    # Error 14: Device cannot transmit data
    # Error 16: Dongle missing
    # Error 17: One of the devices assumed master status because the original master failed
    # Error 18: AC Overvoltage on the output of a slave has occurred while already switched off
    # Error 22: This device cannot function as slave
    # Error 24: Switch-over system protection initiated
    # Error 25: Firmware incompatibility.
    # Error 26: Internal error
    No_error, VEBus_Error_1, VEBus_Error_2, VEBus_Error_3, VEBus_Error_4, VEBus_Error_5, VEBus_Error_6, VEBus_Error_7, VEBus_Error_10, VEBus_Error_14, VEBus_Error_16, VEBus_Error_17, VEBus_Error_18, VEBus_Error_22, VEBus_Error_24, VEBus_Error_25, VEBus_Error_26 = [0, 1, 2, 3, 4, 5, 6, 7, 10, 14, 16, 17, 18, 22, 24, 25, 26] # Internal error

class VebusMode:
    Charger_Only, Inverter_Only, On, Off = [1, 2, 3, 4]

class VebusAlarm:
    Ok, Warning, Alarm = [0, 1, 2]

class VebusClient:

    # CCGX VE.Bus port (ttyO1)
    unit = 0xF6   # Unit ID = 246

    # pass ModbusTcpClient client
    def __init__(self, client):
        self.client = client

    # Get functions

    # return list with input voltage of L1, L2 and L3
    def get_input_voltage(self):
        return ClientFunctions.get_three_phase_values(self.client, 3, self.unit, 10.0, False)

    def get_input_current(self):
        return ClientFunctions.get_three_phase_values(self.client, 6, self.unit, 10.0, True)

    def get_input_frequency(self):
        return ClientFunctions.get_three_phase_values(self.client, 9, self.unit, 100.0, True)

    def get_input_power(self):
        return ClientFunctions.get_three_phase_values(self.client, 12, self.unit, 0.1, True)

    def get_output_voltage(self):
        return ClientFunctions.get_three_phase_values(self.client, 15, self.unit, 10, False)

    def get_output_current(self):
        return ClientFunctions.get_three_phase_values(self.client, 18, self.unit, 10, True)

    # returns the frequency of L1
    def get_output_frequency(self):
        return ClientFunctions.get_single_value(self.client, 21, self.unit, 100.0, True)

    def get_active_input_current_limit(self):
        return ClientFunctions.get_single_value(self.client, 22, self.unit, 10.0, True)

    def get_output_power(self):
        return ClientFunctions.get_three_phase_values(self.client, 23, self.unit, 0.1, True)

    # better to use bmv output
    def get_battery_voltage(self):
        return ClientFunctions.get_single_value(self.client, 26, self.unit, 100.0, False)

    def get_battery_current(self):
        return ClientFunctions.get_single_value(self.client, 27, self.unit, 10.0, True)

    def get_battery_state(self):
        return ClientFunctions.get_single_value(self.client, 844, self.unit, 10.0, True)

    def get_phase_count(self):
        return ClientFunctions.get_single_value(self.client, 28, self.unit, 1, False)

    def get_pv_voltage(self):
        return ClientFunctions.get_single_value(self.client, 777, self.unit, 10.0, False)

    # returns 0="Input 1" 1="Input 2" etc
    def get_active_input(self):
        return ClientFunctions.get_single_value(self.client, 29, self.unit, 1, False)

    # returns the state of charge in percent
    def get_soc(self):
        return ClientFunctions.get_single_value(self.client, 30, self.unit, 10.0, False)

    def get_vebus_state(self):
        return VebusState(ClientFunctions.get_single_value(self.client, 31, self.unit, 1, False))

    def get_vebus_error(self):
        return VebusError(ClientFunctions.get_single_value(self.client, 32, self.unit, 1, False))

    def get_vebus_mode(self):
        return VebusMode(ClientFunctions.get_single_value(self.client, 33, self.unit, 1, False))

    def get_vebus_tempature_alarm(self):
        return VebusAlarm(ClientFunctions.get_single_value(self.client, 34, self.unit, 1, False))

    def get_vebus_low_battery_alarm(self):
        #return VebusAlarm(ClientFunctions.get_single_value(self.client, 35, self.unit, 1, False))
        return ClientFunctions.get_single_value(self.client, 35, self.unit, 1, False)

    def get_vebus_overload_alarm(self):
        return VebusAlarm(ClientFunctions.get_single_value(self.client, 36, self.unit,  1, False))

    # Hub4 get functions:

    def get_hub4_power_setpoint_phase1(self):
        return ClientFunctions.get_single_value(self.client, 37, self.unit, 1, True)

    def get_hub4_disable_charge_flag(self):
        return bool(ClientFunctions.get_single_value(self.client, 38, self.unit, 1, False))

    def get_hub4_disable_feedback_flag(self):
        return bool(ClientFunctions.get_single_value(self.client, 39, self.unit, 1, False))

    def get_hub4_power_setpoint_phase2(self):
        return ClientFunctions.get_single_value(self.client, 40, self.unit, 1, True)

    def get_hub4_power_setpoint_phase3(self):
        return ClientFunctions.get_single_value(self.client, 41, self.unit, 1, True)

    # Hub4 control get functions

    def get_hub4_control_loop_setpoint(self):
        return ClientFunctions.get_single_value(self.client, 2700, self.unit, 1, True)

    # returns the current in percent
    def get_hub4_max_charge_current(self):
        return ClientFunctions.get_single_value(self.client, 2701, self.unit, 1, False)

    def get_hub4_max_discharge_current(self):
        return ClientFunctions.get_single_value(self.client, 2702, self.unit, 1, False)


    # Set functions

    def set_active_input_current_limit(self, limit):
        return ClientFunctions.set_single_value(self.client, 22, self.unit, limit, 10, True)

    # mode = VebusMode.name
    def set_mode(self, mode):
        return ClientFunctions.set_single_value(self.client, 33, self.unit, mode.value, 1, False)
  

    # Hub4 set functions:

    def set_hub4_power_setpoint_phase1(self, setpoint):
        #obj = {
        #    'id': 1,
        #    'unit': str(self.unit),
        #    'service': 'com.victronenergy.vebus',
        #    'address': 37,
        #    'value': setpoint
        #}
        #broadcast(obj)
        return ClientFunctions.set_single_value(self.client, 37, self.unit, setpoint, 1, True)

    def set_hub4_disable_charge_flag(self, boolean):
        return ClientFunctions.set_single_value(self.client, 38, self.unit, int(boolean), 1, False)

    def set_hub4_disable_feedback_flag(self, boolean):
        return ClientFunctions.set_single_value(self.client, 39, self.unit, int(boolean), 1, False)

    def set_hub4_power_setpoint_phase2(self, setpoint):
        obj = {
            'id': 1,
            'unit': str(self.unit),
            'service': 'com.victronenergy.vebus',
            'address': 40,
            'value': setpoint
        }
        return ClientFunctions.set_single_value(self.client, 40, self.unit, setpoint, 1, True)

    def set_hub4_power_setpoint_phase3(self, setpoint):
        obj = {
            'id': 1,
            'unit': str(self.unit),
            'service': 'com.victronenergy.vebus',
            'address': 41,
            'value': setpoint
        }
        return ClientFunctions.set_single_value(self.client, 41, self.unit, setpoint, 1, True)

    # Hub4 control set functions

    def set_hub4_control_loop_setpoint(self, watt):
        return ClientFunctions.set_single_value(self.client, 2700, self.unit, watt, 1, True)

    # returns the current in percent
    def set_hub4_max_charge_current(self, percent):
        return ClientFunctions.set_single_value(self.client, 2701, self.unit, percent, 1, False)

    def set_hub4_max_discharge_current(self, percent):
        return ClientFunctions.set_single_value(self.client, 2702, self.unit, percent, 1, False)


    # function for closing connection
    def close_connection(self):
        self.client.close()
