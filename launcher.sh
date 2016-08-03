cd /opt/terrarium/scripts
sudo python raspberry.py &
cd /opt/terrarium/database
sudo python fill_db_temperature.py &
sudo python rotate_delete_db.py &
cd /opt/terrarium
sudo python server.py
cd /
