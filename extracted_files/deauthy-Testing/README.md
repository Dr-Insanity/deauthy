# DeAuthy
DeAuthy is a Python 3 application for keeping Wi-Fi devices, such as laptops, mobile phones, anything that can connect to a Wi-Fi network off multiple Wi-Fi networks.

# DEAUTHY IS NOT WORKING YET.

## Requirements
- The latest [Python 3](https://www.python.org/downloads/) version
- [Git](https://git-scm.com/downloads)
- [Aircrack-ng](https://www.aircrack-ng.org/doku.php?id=Main)
- **[Hardware Requirement]**-**[Internal/External]** A [NIC](https://en.wikipedia.org/wiki/Network_interface_controller) with a chipset that supports monitor/promiscuous mode & packet/frame injection.

that is pretty much all for the dependencies. The rest is auto-installed, assuming [`pip`](https://pypi.org/project/pip/) is on your system variables, better known as PATH.

The auto-installed dependencies are:
- [`colorama`](https://pypi.org/project/colorama/)
- [`pyroute2`](https://pypi.org/project/pyroute2/)
- [`halo`](https://github.com/manrajgrover/halo)
## platforms / compatibility
DeAuthy is developed mainly for Linux. More specifically **Debian**. With a lot of code changes by yourself, you _could_ make it work on Windows. **DeAuthy is not developed for Windows**.
## Installation
Clone the **specific** branch
```bash
git clone --branch Production/Release https://github.com/Dr-Insanity/deauthy.git
```
## Usage
DeAuthy does not perform recon/discovering. You'd have to do discovery on your own.
### Things you'll need
> 1.) The target's MAC address (Of a client. _i.e. Laptop, Phone_)

> 2.) Choose an approach beforehand: Will you target a network with multiple access points? Discover some BSSIDs of the network(s) you wish to block for the target MAC address. Otherwise, you could just do ESSID, which is simply the name of a wireless network.

The rest of the usage is explained in the application itself. Still having issues? Please create an issue [here](https://github.com/Dr-Insanity/deauthy/issues/new)

## License
Since I can't really make Python code closed source, I'm rather forced to say "You can modify/redistribute DeAuthy as you wish". But hey, In the end, everything can be reverse engineered. You just need the right tools for the job.