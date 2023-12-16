from socket import *
import time

DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)
IPS = ['192.168.0.100', '192.168.0.110', '192.168.0.120', '192.168.0.130', '192.168.0.140', '192.168.0.150']
LEASE_DURATION = 60  # Lease duration in seconds
SERVERIP = '192.168.0.1'

# Maintain a record of leased IP addresses along with MAC addresses and expiration times
LEASED_IPS = {}

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

# Receive a UDP message
ipnum = 0
while True:
    msg, addr = s.recvfrom(1024)

    # Extract relevant information from the DHCP header
    OP = msg[0]
    HTYPE = msg[1]
    HLEN = msg[2]
    HOPS = msg[3]
    XID = msg[4:8]
    SECS = msg[8:10]
    FLAGS = msg[10:12]
    CIADDR = msg[12:16]
    YIADDR = msg[16:20]
    SIADDR = msg[20:24]
    GIADDR = msg[24:28]
    CHADDR1 = msg[28:32]
    CHADDR2 = msg[32:36]
    CHADDR3 = msg[36:236]
    COOKIE = msg[236:240]
    DHCPTYPE = msg[240:243]
    REQUESTEDIP = msg[243:249]

    # Extract MAC address
    mac_address = ":".join(format(byte, '02x') for byte in msg[28:34])

    # Print the client's MAC Address from the DHCP header
    print("Client's MAC Address is " + mac_address)

    # Check DHCP message type
    if DHCPTYPE == b'\x35\x01\x01':
        # Check if the client has an existing IP
        existing_ip = LEASED_IPS.get(mac_address, None)

        if existing_ip:
            # If IP exists, use the existing one
            print("Reusing existing IP:", existing_ip)
            DHCPOFFER = b'\x02\x01\x06\x00'
            DHCPOFFER += XID
            DHCPOFFER += b'\x00\x00\x00\x00'
            DHCPOFFER += b'\x00\x00\x00\x00'
            DHCPOFFER += inet_aton(existing_ip)
            DHCPOFFER += inet_aton(SERVERIP)
            DHCPOFFER += b'\x00\x00\x00\x00'
            DHCPOFFER += CHADDR1 + CHADDR2 + CHADDR3
            DHCPOFFER += COOKIE
            DHCPOFFER += b'\x35\x01\x02'
            DHCPOFFER += b'\x01\x04' + inet_aton('255.255.255.0')
            DHCPOFFER += b'\x03\x04' + inet_aton(SERVERIP)
            DHCPOFFER += b'\x33\x04\x00\x00\x00\x3C'  # Lease time set to 60 seconds
            DHCPOFFER += b'\xff'
            s.sendto(DHCPOFFER, DHCP_CLIENT)

        else:
            # If IP doesn't exist, assign a new one
            leased_ip = IPS[ipnum]
            LEASED_IPS[mac_address] = leased_ip  # Store the new MAC-IP mapping
            print("Assigning new IP:", leased_ip)
            DHCPOFFER = b'\x02\x01\x06\x00'
            DHCPOFFER += XID
            DHCPOFFER += b'\x00\x00\x00\x00'
            DHCPOFFER += b'\x00\x00\x00\x00'
            DHCPOFFER += inet_aton(leased_ip)
            DHCPOFFER += inet_aton(SERVERIP)
            DHCPOFFER += b'\x00\x00\x00\x00'
            DHCPOFFER += CHADDR1 + CHADDR2 + CHADDR3
            DHCPOFFER += COOKIE
            DHCPOFFER += b'\x35\x01\x02'
            DHCPOFFER += b'\x01\x04' + inet_aton('255.255.255.0')
            DHCPOFFER += b'\x03\x04' + inet_aton(SERVERIP)
            DHCPOFFER += b'\x33\x04\x00\x00\x00\x3C'  # Lease time set to 60 seconds
            DHCPOFFER += b'\xff'
            s.sendto(DHCPOFFER, DHCP_CLIENT)
            ipnum = (ipnum + 1) % len(IPS)

    # DHCP Request handling
    elif DHCPTYPE == b'\x35\x01\x03':
        # Check if the client has a valid lease
        existing_ip = LEASED_IPS.get(mac_address, None)

        if existing_ip:
            # If lease exists, send DHCP ACK
            print("Renewing existing IP:", existing_ip)
            DHCPACK = b'\x02\x01\x06\x00'
            DHCPACK += XID
            DHCPACK += b'\x00\x00\x00\x00'
            DHCPACK += b'\x00\x00\x00\x00'
            DHCPACK += inet_aton(existing_ip)
            DHCPACK += inet_aton(SERVERIP)
            DHCPACK += b'\x00\x00\x00\x00'
            DHCPACK += CHADDR1 + CHADDR2 + CHADDR3
            DHCPACK += COOKIE
            DHCPACK += b'\x35\x01\x05'
            DHCPACK += b'\x01\x04' + inet_aton('255.255.255.0')
            DHCPACK += b'\x03\x04' + inet_aton(SERVERIP)
            DHCPACK += b'\x33\x04\x00\x00\x00\x3C'
            DHCPACK += b'\xff'
            s.sendto(DHCPACK, DHCP_CLIENT)
