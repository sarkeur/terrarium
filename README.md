# Automatic control of a terrarium
This repository aims to automatically control the terrarium environment. It is supposed to regulate the temperature, activate the day/night switch and send informations on a server.

# Example
Let's take the example of a Pogona (lezard). Its natural environment is located in Australia, so the temperature and the day duration is not the same than in my country. The solar time calendar of Australia has been downloaded and will be used to activate the day or night switch, turning on and off an UV neon and an incandescente lamp (also producing light). The day temperature should be 38°C and will be obtained with the incandescente lamp and a ceramic lamp (which do not procude light) if necessary. During night, only the ceramic lamp can be on to maintain a temperature of 22°C. Finally, the calendar will also be used to create seasons and reproduce an natural changment. The day duration should be around 14 hours during summer and 9 hours during winter.

# Start a script on reboot
- modify launcher.sh
- sudo crontab -e
- @reboot /home/pi/terrarium/launcher.sh &

add a sleep before connecting to mysql
