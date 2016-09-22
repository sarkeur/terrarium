import subprocess
import os

subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'mysql-server'])
subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'python-dev', 'libmysqlclient-dev'])
subprocess.check_call(['sudo', 'pip', 'install', 'MySQL-python'])

subprocess.check_call('mysqladmin -uroot -pnairolfuaebel create terrarium')
subprocess.check_call('echo "USE terrarium; CREATE TABLE IF NOT EXISTS temperature(date_heure DATETIME NOT NULL,TerraLowTemp SMALLINT UNSIGNED NOT NULL,TerraColdTemp SMALLINT UNSIGNED NOT NULL,TerraWarmTemp SMALLINT UNSIGNED NOT NULL,RoomTemp SMALLINT UNSIGNED NOT NULL,RaspberryTemp SMALLINT UNSIGNED NOT NULL);" | mysql -u root -pnairolfuaebel')
