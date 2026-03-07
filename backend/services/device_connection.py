from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def run_command_on_device(ip, username, password, command):

    device = {
        "device_type": "mikrotik_routeros",
        "host": ip,
        "username": username,
        "password": password,
        "timeout": 10,           # seconds to wait for TCP connection
        "banner_timeout": 15,    # seconds to wait for SSH banner
        "auth_timeout": 15,      # seconds to wait for authentication
        "session_timeout": 30,   # seconds before idle session closes
    }

    try:
        connection = ConnectHandler(**device)
        output = connection.send_command(command)
        connection.disconnect()
        return output

    except NetmikoTimeoutException:
        raise Exception(f"Connection timed out to device {ip}")

    except NetmikoAuthenticationException:
        raise Exception(f"Authentication failed for device {ip}")

    except Exception as e:
        raise Exception(f"SSH error on device {ip}: {str(e)}")


def push_config_to_device(ip, username, password, commands):

    device = {
        "device_type": "mikrotik_routeros",
        "host": ip,
        "username": username,
        "password": password,
        "timeout": 10,
        "banner_timeout": 15,
        "auth_timeout": 15,
        "session_timeout": 30,
    }

    try:
        connection = ConnectHandler(**device)
        output = connection.send_config_set(commands)
        connection.disconnect()
        return output

    except NetmikoTimeoutException:
        raise Exception(f"Connection timed out to device {ip}")

    except NetmikoAuthenticationException:
        raise Exception(f"Authentication failed for device {ip}")

    except Exception as e:
        raise Exception(f"SSH config push error on device {ip}: {str(e)}")  