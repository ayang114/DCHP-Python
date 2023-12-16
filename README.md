Things to run
sudo mn --custom=mytopo0-1.py --topo=mytopo

server ip address add 192.168.0.1/24 dev server-eth0
server ip route add default dev server-eth0

xterm server
python3 dhserver.py

mytopo0-1:
client dhclient -r

client dhclient -4 -v client-eth0

mytopo1-1:
client0 dhclient -r
client1 dhclient -r
client2 dhclient -r
client3 dhclient -r

client0 dhclient -4 -v client0-eth0
client1 dhclient -4 -v client1-eth0
client2 dhclient -4 -v client2-eth0
client3 dhclient -4 -v client3-eth0

discover
offer
request
ack
<img width="1512" alt="Screenshot 2023-12-15 at 5 31 34 PM" src="https://github.com/ayang114/PythonDCHP/assets/102551386/5b6540e7-0bfe-4a7b-a4f1-6f87e71753f4">
