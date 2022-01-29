# fitnessfabrik_usage_diagramm

My local gym Fitnessfabrik started offering a [visitor count](http://besucher.fitnessfabrik.de) during the Corona period in 2020. The websites only shows the current visitor count 
but it doesn't offer a history function or diagrams. So I created this small project to scrape the data from the website and create useful diagrams out of it. The diagrams offer an easy way to find less busy time spots in the gym :)

<p align="center">
  <img src="pictures/fitness_fabrik_visitor_count.png">
</p>
<p align="center">
     <em>Original website</em>
</p>

## Script

The Python 3 script uses the Beautiful Soup lib to scrape the visitor count from http://besucher.fitnessfabrik.de every minute. It writes the data to a simple .csv file 
and uses the pandas and Plotly lib to render a HTML diagram from the data.

I run the script on a Raspberry Pi 3 and has proven to be very reliable for the job.

<p align="center">
  <img src="pictures/sample_count.png">
</p>
<p align="center">
     <em>This a rendered HTML diagram by the script</em>
</p>

## Trigger
* A simple way to start the script is to just run ```python3 get_count.py```
* It's recommended to set the script up as a systemd service and trigger it via cron
  * ```50 5 * * 1-5 systemctl start gym_visitor_count``` -> Start at 5:50 GMT during the week
  * ```10 22 * * 1-5 systemctl stop gym_visitor_count``` -> Stop at 22:10 GMT during the week
  * ``` 50 8 * * 6,0 systemctl start gym_visitor_count``` -> Start at 08:50 GMT on weekends
  * ``` 10 20 * * 6,0 systemctl stop gym_visitor_count``` -> Stop at 20:10 GMT on weekends
* One could also use [systemd timers](https://wiki.archlinux.org/title/Systemd/Timers) to schedule the service

##  View the diagrams

There multiple options to view the diagrams with the visitor statistics. 

* Local workstation
  * Go to the output folder specified in the script and open the <ISO_8601_date>.html file (for example 2020-06-30.html)  
* Remote device without GUI (for example a Raspberry Pi with CLI only)
  * A Raspberry Pi runs the script perfectly fine and offers a low power consumption
  * A good way to view the HTML files is to run a webserver (like Nginx) with directory listing enabled
  * The script copies the rendered HTML files to the ```/var/www/html/``` directory which can be served via Nginx

<p align="center">
  <img src="pictures/nginx_dir_listing.png">
</p>
<p align="center">
     <em>Nginx hosting the HTML files with directory listing enabled</em>
</p>

## Disclaimer:

I am not associated with the company running the gym. This is just a small hobby project by a customer. 