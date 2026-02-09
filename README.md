# STRONG IPAQ REPLACEMENT

This project targets to replace the DIGIBOX REMOTE CONTROL software installed on the IPAQ handheld, to move up and down the lamps in the Senate of Spain's old meeting room.

After some investigation,  the protocol is DMX512, a variant over RS845 protocol used for manage lights and so on.
[I found some specific info about strong's board](http://www.strong.es/upfiles/productes/fitxers/A316890026.pdf)
There's also some [implementations](https://github.com/tigoe/sACNSource) for arduino. The motor control box is a
[Motor Digi BOX from strong](http://www.strong.es/producto.asp?strong=0&stage=1&id=237).

## Configuration

On IPAQ, we have a configuration file under `Archivos de Programa\Digibox` (`params.txt`). This is an XML file, with the following
information:

* IP_LOCAL: `192.168.72.228`
* IP_REMOTA: `192.168.72.226`
* PORT_SERVER: `53704`
* FPS: `8`
* PASSWORD: `1234`

After some investigation, the connection is done using  `UDP`. After FPS packets, an ICMP packet is send to port 590.
**NOTE** this happens because the port is unrecheable. Fixed with the iptables command.


## PineApple Configuration

Pineapple default password is `hak5pineapple`

IP must be 192.168.72.1. Create a OpenAP to mimic the software, and install the folling packages:

* tcpdump
* netcat

Then, Create an alias on br-lan so the IPAQ can connect to the "server"

`ifconfig br-lan:0 192.168.72.226 netmask 255.255.255.0 up`

allow incoming packets

`iptables -I INPUT -p udp --dport 53704 -j ACCEPT`

Then start a echo netcat.

`netcat -x -u -l 192.168.72.226 -p 53704 -o /tmp/netcat.out`

To check the UDP ports, we can issue a `nmap` command from a client machine:

`nmap -sU -p 53704 -T4 -A -v 192.168.72.226`


## Battery Tests

These are the following tests to reverse engineer the packages

| **Test** | **Mode**		| **Description**		|
|----------|-----------------|------------------------|
| 0		| empty		   | don't sent any packets |
| 1		| 1 D			 |						|
| 2		| 2 D			 |						|
| 3		| 3 D			 |						|
| 4		| 1,2 D		   |						|
| 5		| 1,2,3 D		 |						|
| 6		| 1 U			 |						|
| 7		| 2 U			 |						|
| 8		| 3 U			 |						|
| 9		| 1,2 U		   |						|
| 10	   | 1,2,3 U		 |						|
| 11	   | STOP (empty)	|						|
| 12	   | REARM (empty)   |						|
| 13	   | ALL D		   |						|
| 14	   | ALL U		   |						|
| 15	   | 1-12 U, 13-24 D |						|
| 16	   | 1-12 D, 13-24 U |						|


* 1 D means signal 1, Down
* 2 U means signal 2, Up
* Files are named `t_<n>.pcap`
* Captured packets as: `tcpdump -i wlan0 -e -s 0 -w t_0.pcap`


## Packet format.

* The packet is an UDP packet, sent from 192.168.72.228 to 192.168.72.226 to port 53704
* The packet is sent FPS times per second (e.g. 8 packets per second).
* Package size is 1036 bytes. Only first bytes are shown.
* From byte 0 to 11 is the "header": `44 4d 58 35 31 32 2d 02  00 01 00 02`
* From byte 12 to byte 59 (starting of 0) two bytes indicate what to do with the position: (24 positions, from 0 to 23 as expected on the app)
* `00 ff` means does nothing
* `1e e1` means down
* `96 69` means up

```
								from here |
                                          v
0000  44 4d 58 35 31 32 2d 02  00 01 00 02 00 ff 00 ff   DMX512-· ········
0010  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0020  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0030  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 00 00 00   ········ ········
                                          ^
										  | till here
...                                          
```

### Emtpy package

```
0000  44 4d 58 35 31 32 2d 02  00 01 00 02 00 ff 00 ff   DMX512-· ········
0010  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0020  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0030  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 00 00 00   ········ ········
...
```

### Signal 1 Down

```
0000  44 4d 58 35 31 32 2d 02  00 01 00 02 1e e1 00 ff   DMX512-· ········
0010  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0020  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0030  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 00 00 00   ········ ········
0040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ········ ········
...
```

### Signal 2 Up

```
0000  44 4d 58 35 31 32 2d 02  00 01 00 02 00 ff 96 69   DMX512-· ·······i
0010  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0020  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 ff 00 ff   ········ ········
0030  00 ff 00 ff 00 ff 00 ff  00 ff 00 ff 00 00 00 00   ········ ········
0040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ········ ········
...

```

### All signals up 

```
0000  44 4d 58 35 31 32 2d 02  00 01 00 02 96 69 96 69   DMX512-· ·····i·i
0010  96 69 96 69 96 69 96 69  96 69 96 69 96 69 96 69   ·i·i·i·i ·i·i·i·i
0020  96 69 96 69 96 69 96 69  96 69 96 69 96 69 96 69   ·i·i·i·i ·i·i·i·i
0030  96 69 96 69 96 69 96 69  96 69 96 69 00 00 00 00   ·i·i·i·i ·i·i····
0040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   ········ ········
...
```

Special buttons `EMERGENCY STOP` and `REARM` send empty packet.

## Python command line interface.

* You must send empty commands to start the power in the motor control box.
* The command length must be 32 or greater in order to command all the motors. More motors, more pacakges.

```
python.exe .\strong_dmx.py -c up -i 1 -i 2 -i 3 -n 32
```
