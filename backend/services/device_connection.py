from netmiko import ConnectHandler


def run_command_on_device(ip, username, password, command):

    device = {
        "device_type": "mikrotik_routeros",
        "host": ip,
        "username": username,
        "password": password
    }

    connection = ConnectHandler(**device)

    output = connection.send_command(command)

    connection.disconnect()

    return output


def push_config_to_device(ip, username, password, commands):

    device = {
        "device_type": "mikrotik_routeros",
        "host": ip,
        "username": username,
        "password": password
    }

    connection = ConnectHandler(**device)

    output = connection.send_config_set(commands)

    connection.disconnect()

    return output