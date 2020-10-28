# sys-hidplus
A Nintendo Switch sysmodule to use up to 3 inputs over the network and useful to use with services such as Parsec for remote play


# Disclaimer
Bugs occur and I'm in no way responsible of any damage caused by this sysmodule or its misuse. If you get any issue, please report it on the Issues tab or report it on the gbatemp thread.


# Instructions
Just copy the contents of the switch folder in the build zip file to the microSD card and be sure to use Atmosphere because this CFW isn't tested with other CFWs.

After that, make sure you have Python3 installed and open cmd on where you extracted the pc folder from the build zip file and execute `py -3 -m pip install inputs`, you'll have to do this step only once. Once inputs is installed, you can then connect to your switch by using `python3 input_pc.py {SWITCH IP}`, replacing {SWITCH IP} with the IP address of your Switch (You can check it by going to Settings > Internet on your system).

You can modify the behaviour of the controller emulation on the python file by changing the conType values. If you set it to 0, you'll be able to disconnect the controller (useful if the Switch disconnects the controller for some reason), if you set it to 1, you'll be able to emulate a Pro Controller, if you set it to 2 or 3, you'll be able to use the experimental sideways joycon emulation, it has some issues but in some games such as Clubhouse Games, it'll be playable.


# Stuff to do
* Make the compatibility for sideways joycons emulation better
* Add 4th controller emulation
* Add 5-8th controller emulation
* Add gyro compatibility
* Add USB compatibility


# Known issues
* Input lag is increased on demanding games such as Super Mario Odyssey


# Unsupported games
* All games that require the gyroscope or the SL/SR buttons (For example, 1-2-Switch, Pokémon Let's Go or Super Mario Party)


# Support
The best way to get your questions answered is by asking me in Discord (IgnacIo#0001) or by asking on the gbatemp thread.


# Special Thanks
* jakibaki - base and inspiration for this sysmodule (hid-mitm), a lot of the code comes from it
* cathery - helping me with my dumb questions and issues
* ReSwitched Discord Server - help in the support channels
* **Everyone using this sysmodule - thanks a lot!**


# Donations
No, use your money to buy games for yourself or something idk
