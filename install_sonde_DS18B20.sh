sudo modprobe w1-gpio
sudo modprobe w1-therm
echo $(ls /sys/bus/w1/devices/)

echo "IF NOTHING HAS BEEN DISPLAYED BEFORE, THE DS18B20 SENSORS ARE NOT RECOGNIZED:"
echo "add the following lines to the file /etc/modules:"
echo "      w1-therm"
echo "      w1-gpio pullup=1"
echo ""
echo "add the following lines to the file /boot/config.txt:"
echo "      dtoverlay=w1-gpio"
