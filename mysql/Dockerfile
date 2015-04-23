# Openhab installation file

#FROM hypriot/rpi-mysql
FROM hypriot/rpi-python
MAINTAINER Roman Grekov <roman.grekov88@gmail.com>

RUN apt-get update -y

#Install and config mysql
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -q -y mysql-server
RUN apt-get install -y mysql-client

RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf
#RUN sed -i '/bind-address*/a skip-grant-tables' /etc/mysql/my.cnf

ADD mysql_startup.sh /mysql_startup.sh

EXPOSE 3306

CMD ["/bin/bash", "/mysql_startup.sh"]
