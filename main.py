import platform
import subprocess
import re

def get_available_interfaces():
    try:
        result = subprocess.check_output("netsh interface show interface", shell=True, text=True)
        interfaces = [line.split()[-1] for line in result.split('\n') if "Connected" in line and "Loopback" not in line]
        return interfaces
    except Exception as e:
        print(f"Error fetching interfaces: {e}")
        return []

def validate_ip(ip):
    return re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip) and all(0 <= int(octet) <= 255 for octet in ip.split('.'))

def set_static_ip(interface, ip, gateway):
    try:
        cmd = f'netsh interface ip set address "{interface}" static {ip} 255.255.255.0 {gateway}'
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

interfaces = get_available_interfaces()
if not interfaces:
    print("No available interfaces found!")
    exit()

print("Available network interfaces:")
for i, interface in enumerate(interfaces):
    print(f"{i + 1}. {interface}")

while True:
    try:
        choice = int(input("Select interface (number): "))
        if 1 <= choice <= len(interfaces):
            selected_interface = interfaces[choice - 1]
            break
        print("Invalid choice! Try again.")
    except ValueError:
        print("Please enter a number!")

while True:
    user_ip = input("Enter IP: ").strip()
    if validate_ip(user_ip):
        break
    print("Invalid IP! Example: 192.168.1.100")

gateway = "192.168.1.1"
print("\nGateway options:")
print("1. Default Gateway (192.168.1.1)")
print("2. Custom Gateway")
while True:
    try:
        gateway_choice = int(input("Choose an option (1 or 2): "))
        if gateway_choice == 1:
            print("Using Default Gateway: 192.168.1.1")
            break
        elif gateway_choice == 2:
            while True:
                custom_gateway = input("Enter Custom Gateway IP: ").strip()
                if validate_ip(custom_gateway):
                    gateway = custom_gateway
                    break
                print("Invalid Gateway IP! Example: 192.168.1.1")
            break
        else:
            print("Invalid choice! Please enter 1 or 2.")
    except ValueError:
        print("Please enter a number!")

if set_static_ip(selected_interface, user_ip, gateway):
    print(f"IP {user_ip} and Gateway {gateway} set successfully on {selected_interface}!")
else:
    print("Failed to set IP. Run as administrator.")
