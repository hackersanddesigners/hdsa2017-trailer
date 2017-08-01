
class ClientFunctions:

    @staticmethod
    def get_single_value(client, address, unit, factor, signed):
        rr = client.read_holding_registers(address, 1, unit = unit)
        if signed and rr.registers[0] >= 32768:
            return (rr.registers[0] - 65536) / factor
        else:
            return rr.registers[0] / factor

    @staticmethod
    def get_three_phase_values(client, start_address, unit, factor, signed):
        rr = client.read_holding_registers(start_address, 3, unit = unit)
        result = []
        for i in range(0,3):
            if signed and rr.registers[i] >= 32768:
                result.append(rr.registers[i] - 65536 / factor)
            else:
                result.append(rr.registers[i] / factor)
        return result

    @staticmethod
    def set_single_value(client, address, unit, value, factor, signed):
        result = 0
        if signed and value < 0:
            result += 65536
        result = (value * factor) + result
        return client.write_register(address, result, unit = unit)
