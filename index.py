#!/usr/bin/env python
# -*- coding: utf-8 -*-

## IMPORT ##
import MySQLdb 
import time 
import cgitb 
import cgi

## FUNCTIONS ##
# get data from the database
def get_data():
    db = MySQLdb.connect(host="localhost",user="root",passwd="nairolfuaebel", db="terrarium")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM temperature")
    rows = cursor.fetchall()
    cursor.close()
    return rows 

def get_max(column):
    db = MySQLdb.connect(host="localhost",user="root",passwd="nairolfuaebel", db="terrarium")
    cursor = db.cursor()
    cursor.execute("SELECT MAX(%s) FROM temperature" % column)
    row = cursor.fetchone()
    cursor.close()
    return row 

def get_min(column):
    db = MySQLdb.connect(host="localhost",user="root",passwd="nairolfuaebel", db="terrarium")
    cursor = db.cursor()
    cursor.execute("SELECT MIN(%s) FROM temperature" % column)
    row = cursor.fetchone()
    cursor.close()
    return row

# convert rows from database into a javascript table
def create_table(rows, x):
    chart_table=""
    for row in rows[:-1]:
        rowstr="['{0}', {1}],\n".format(str(row[0]),str(row[x]))
        chart_table+=rowstr
    row=rows[-1]
    rowstr="['{0}', {1}]\n".format(str(row[0]),str(row[x]))
    chart_table+=rowstr
    return chart_table

# google chart snippet
chart_code="""  <script type="text/javascript" 
		src="https://www.google.com/jsapi"></script>
    		<script type="text/javascript">
      			google.load("visualization", "1", {packages:["corechart", "gauge"]});
      			google.setOnLoadCallback(drawChart);
      		function drawChart() {
        	var courbe_RaspberryTemp = google.visualization.arrayToDataTable([['Time', 'Temperature'],%s]);
        	var courbe_RoomTemp = google.visualization.arrayToDataTable([['Time', 'Temperature'],%s]);
        	var courbe_LowTemp = google.visualization.arrayToDataTable([['Time', 'Temperature'], %s]);
        	var courbe_WarmTemp = google.visualization.arrayToDataTable([['Time', 'Temperature'], %s]);
        	var courbe_ColdTemp = google.visualization.arrayToDataTable([['Time', 'Temperature'], %s]);

        	var gauge_RaspberryTemp = google.visualization.arrayToDataTable([['Label', 'Value'],['Raspberry', %s]]);
        	var gauge_RoomTemp = google.visualization.arrayToDataTable([['Label', 'Value'],['Room', %s]]);
        	var gauge_LowTemp = google.visualization.arrayToDataTable([['Label', 'Value'],['Low', %s]]);
        	var gauge_WarmTemp = google.visualization.arrayToDataTable([['Label', 'Value'],['Warm', %s]]);
        	var gauge_ColdTemp = google.visualization.arrayToDataTable([['Label', 'Value'],['Cold', %s]]);

        	var gauge_options = {redFrom: 90, redTo: 100, yellowFrom:75, yellowTo: 90, minorTicks: 5};

        	var courbe_chart_RaspberryTemp = new google.visualization.LineChart(document.getElementById('courbe_chart_div_RaspberryTemp'));
        	option_RaspberryTemp = {title: 'Raspberry', colors: ['black'], backgroundColor: '#EEC277', hAxis: {title: 'Time'}, vAxis: {title: 'Temperature'}}
        	courbe_chart_RaspberryTemp.draw(courbe_RaspberryTemp, option_RaspberryTemp);

        	var courbe_chart_RoomTemp = new google.visualization.LineChart(document.getElementById('courbe_chart_div_RoomTemp'));
        	option_RoomTemp = {title: 'Room', colors: ['black'], backgroundColor: '#EEC277', hAxis: {title: 'Time'}, vAxis: {title: 'Temperature'}}
        	courbe_chart_RoomTemp.draw(courbe_RoomTemp, option_RoomTemp);

        	var courbe_chart_LowTemp = new google.visualization.LineChart(document.getElementById('courbe_chart_div_LowTemp'));
        	option_LowTemp = {title: 'Low', colors: ['black'], backgroundColor: '#EEC277', hAxis: {title: 'Time'}, vAxis: {title: 'Temperature'}}
        	courbe_chart_LowTemp.draw(courbe_LowTemp, option_LowTemp);

        	var courbe_chart_WarmTemp = new google.visualization.LineChart(document.getElementById('courbe_chart_div_WarmTemp'));
        	option_WarmTemp = {title: 'Warm', colors: ['black'], backgroundColor: '#EEC277', hAxis: {title: 'Time'}, vAxis: {title: 'Temperature'}}
        	courbe_chart_WarmTemp.draw(courbe_WarmTemp, option_WarmTemp);

        	var courbe_chart_ColdTemp = new google.visualization.LineChart(document.getElementById('courbe_chart_div_ColdTemp'));
        	option_ColdTemp = {title: 'Cold', colors: ['black'], backgroundColor: '#EEC277', hAxis: {title: 'Time'}, vAxis: {title: 'Temperature'}}
        	courbe_chart_ColdTemp.draw(courbe_ColdTemp, option_ColdTemp);

        	var gauge_chart_RaspberryTemp = new google.visualization.Gauge(document.getElementById('gauge_chart_div_RaspberryTemp'));
        	gauge_chart_RaspberryTemp.draw(gauge_RaspberryTemp, gauge_options);

        	var gauge_chart_RoomTemp = new google.visualization.Gauge(document.getElementById('gauge_chart_div_RoomTemp'));
        	gauge_chart_RoomTemp.draw(gauge_RoomTemp, gauge_options);

        	var gauge_chart_LowTemp = new google.visualization.Gauge(document.getElementById('gauge_chart_div_LowTemp'));
        	gauge_chart_LowTemp.draw(gauge_LowTemp, gauge_options);

        	var gauge_chart_WarmTemp = new google.visualization.Gauge(document.getElementById('gauge_chart_div_WarmTemp'));
        	gauge_chart_WarmTemp.draw(gauge_WarmTemp, gauge_options);

        	var gauge_chart_ColdTemp = new google.visualization.Gauge(document.getElementById('gauge_chart_div_ColdTemp'));
        	gauge_chart_ColdTemp.draw(gauge_ColdTemp, gauge_options);
      		}
    		</script>"""
## MAIN ##
cgitb.enable() 
# enable debugging 
max_RaspberryTemp = get_max('RaspberryTemp') 
max_RoomTemp = get_max('RoomTemp') 
max_TerraLowTemp = get_max('TerraLowTemp')
max_TerraWarmTemp = get_max('TerraWarmTemp')
max_TerraColdTemp = get_max('TerraColdTemp')

min_RaspberryTemp = get_min('Raspberrytemp') 
min_RoomTemp = get_min('RoomTemp') 
min_TerraLowTemp = get_min('TerraLowTemp')
min_TerraWarmTemp = get_min('TerraWarmTemp')
min_TerraColdTemp = get_min('TerraColdTemp')

data = get_data() 
last_RaspberryTemp = [x[5] for x in data][-1]
last_RoomTemp = [x[4] for x in data][-1]
last_TerraLowTemp = [x[1] for x in data][-1]
last_TerraColdTemp = [x[2] for x in data][-1]
last_TerraWarmTemp = [x[3] for x in data][-1] 
if len(data) != 0:
    table=create_table(data,1) 
else:
    print "No data found" 

print "Content-type: text/html\n\n" 
print "<html>" 
print "<head>" 
print "<title>Raspberry</title>" 
print """<link type="text/css" rel="stylesheet" href="css/stylesheet1.css"/>""" 
print "<body>" 
print """<h1>Raspberry Monitoring</h1>
         <p> Voici la page d'accueil du raspberry</p>""" 
print chart_code % (create_table(data,5), create_table(data,4), create_table(data,1), create_table(data,3), create_table(data,2), last_RaspberryTemp, last_RoomTemp, last_TerraLowTemp, last_TerraWarmTemp, last_TerraColdTemp)
#print """<div id="courbe_chart_div_RaspberryTemp" style="width: 200px; 
#height: 200px;"></div>"""
print """<div id="courbe_chart_div_RaspberryTemp" class="curves"></div>""" 
print """<div id="courbe_chart_div_RoomTemp" class="curves"></div>""" 
print """<div id="courbe_chart_div_LowTemp" class="curves"></div>""" 
print """<div id="courbe_chart_div_WarmTemp" class="curves"></div>""" 
print """<div id="courbe_chart_div_ColdTemp" class="curves"></div>""" 

print """<div id="gauge_chart_div_RaspberryTemp" class="thermometer"></div>""" 
print """<div class="thermometer">
             Min = %s<br/>
             Max = %s
         </div>""" % (str(get_min('RaspberryTemp')),get_max('RaspberryTemp'))
#print """<div class="thermometer">Max = %s</div>""" % 
#get_max('RaspberryTemp')
print """<div id="gauge_chart_div_RoomTemp" class="thermometer"></div>""" 
print "<p>Min = %s</p>" % get_min('RoomTemp') 
print "<p>Max = %s</p>" % get_max('RoomTemp') 
print """<div id="gauge_chart_div_LowTemp" class="thermometer"></div>"""
print "<p>Min = %s</p>" % get_min('TerraLowTemp') 
print "<p>Max = %s</p>" % get_max('TerraLowTemp')
print """<div id="gauge_chart_div_WarmTemp" class="thermometer"></div>"""
print "<p>Min = %s</p>" % get_min('TerraWarmTemp') 
print "<p>Max = %s</p>" % get_max('TerraWarmTemp')
print """<div id="gauge_chart_div_ColdTemp" class="thermometer"></div>"""
print "<p>Min = %s</p>" % get_min('TerraColdTemp') 
print "<p>Max = %s</p>" % get_max('TerraColdTemp')
print "</body>" 
print "</head>" 
print "</html>"
