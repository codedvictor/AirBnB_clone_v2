#!/usr/bin/env bash
# Script to set up wen servers for the deploymen tof web_static
sudo apt-get -y update
sudo apt-get -y install nginx
sudo service nginx start

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

index="
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"

echo "$index" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/

serv_conf='38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n'
sed -i "$serv_conf" /etc/nginx/sites-enabled/default
sudo service nginx restart
exit 0
