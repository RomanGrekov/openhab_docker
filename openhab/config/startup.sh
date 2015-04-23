#!/bin/bash

#/etc/init.d/openhab start
#/etc/init.d/monit start

sed -i -- "s/mysql\:url=.*/mysql\:url=jdbc\:mysql\:\/\/$MYSQL_PORT_3306_TCP_ADDR\/openhab/g" /opt/openhab/configurations/openhab.cfg
sed -i -- "s/mqtt\:mqtt_broker.*/mqtt\:mqtt_broker\.url=tcp\:\/\/$MOSQUITTO_PORT_1883_TCP_ADDR\:1883/g" /opt/openhab/configurations/openhab.cfg
cd /opt/openhab/ && ./start_debug.sh

