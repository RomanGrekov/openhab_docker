#!/bin/bash

#DO NOT FORGET TO CHANGE IP IN monitrc

sudo update-rc.d -f apache2 remove

sudo mkdir -p /opt/openhab
sudo chown linaro:linaro /opt/openhab
scp -r romang@10.51.110.161:/home/romang/Projects/openhab/openhab_git/* /opt/openhab/
sudo cp /opt/openhab/system/openhab /etc/init.d/

sudo chmod a+x /etc/init.d/openhab
sudo update-rc.d openhab defaults

sudo mount /dev/nanda /mnt
sudo cp /opt/openhab/system/script.fex /mnt/
sudo fex2bin /mnt/script.fex /mnt/script.bin
sudo umount /mnt

sudo cp /opt/openhab/system/interfaces /etc/network/

sudo apt-get install vim
#sudo apt-get install openjdk-7-jre

sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer

sudo apt-get install wpasupplicant
sudo apt-get install ntp
sudo apt-get install mysql-server
sudo apt-get install mysql-client


echo 'create database openhab' | mysql -u root 
echo "create user openhab@localhost identified by '123456';" | mysql -u root
echo "grant all privileges on openhab.* to openhab@localhost;" | mysql -u root
echo "flush privileges;" | mysql -u root

sudo dpkg-reconfigure tzdata #(will ask to choose timezone)

sudo apt-get install monit
sudo scp -r romang@10.51.110.161:/home/romang/Projects/openhab/openhab_git/system/monit/* /etc/monit/
