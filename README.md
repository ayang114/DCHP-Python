# DHCP (Dynamic Host Configuration Protocol)

A Python DHCP server that automatically assigns IP addresses and network settings to clients via discover -> offer -> request -> ack.
<img width="1512" alt="Screenshot 2023-12-15 at 5 31 34 PM" src="https://github.com/ayang114/PythonDCHP/assets/102551386/5b6540e7-0bfe-4a7b-a4f1-6f87e71753f4">

## Getting Started

<b>Setting Up and Running Guide</b>

Step 1: Open the terminal and run the code below
```bash
sudo mn --custom=mytopo0-1.py --topo=mytopo
```
```bash
server ip address add 192.168.0.1/24 dev server-eth0
```
```bash
server ip route add default dev server-eth0
```
```bash
xterm server
```
```bash
python3 dhserver.py
```
<br>

-> Run mytopo0-1 for a <b>single</b> client
First Run:
```bash
client dhclient -r
```
Then run:
```bash
client dhclient -4 -v client-eth0
```

-> Run mytopo1-1 for <b>multiple</b> client
First Run:
```bash
client0 dhclient -r
client1 dhclient -r
client2 dhclient -r
client3 dhclient -r
```
Then run:
```bash
client0 dhclient -4 -v client0-eth0
client1 dhclient -4 -v client1-eth0
client2 dhclient -4 -v client2-eth0
client3 dhclient -4 -v client3-eth0
```
