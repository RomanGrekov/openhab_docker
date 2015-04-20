# Openhab installation file

#FROM ubuntu:14.04
FROM hypriot/rpi-java
#FROM armv7/armhf-ubuntu
MAINTAINER Roman Grekov <roman.grekov88@gmail.com>

#Install openhab
RUN mkdir -p /opt/openhab
ADD openhab /opt/openhab/
#sudo chown odroid:odroid /opt/openhab
#ADD config/system/openhab /etc/init.d/
#RUN chmod a+x /etc/init.d/openhab
#RUN update-rc.d openhab defaults

#Install common packages
RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties
RUN apt-get install -y vim

#Install ntp
RUN apt-get install -y wpasupplicant
RUN apt-get install -y ntp

#Install monit
#RUN apt-get install monit
#ADD $openhab_dir/config/system/monit /etc/monit/

#Network
#sudo cp /opt/openhab/system/interfaces /etc/network/

#Install Java
#RUN apt-get install -y openjdk-7-jdk
#RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
#RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu precise main" | tee /etc/apt/sources.list.d/webupd8team-java.list
#RUN echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu precise main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886
#RUN apt-get update
#RUN apt-get install -y oracle-java8-installer
#RUN rm -rf /var/lib/apt/lists/*
#RUN rm -rf /var/cache/oracle-jdk8-installer

# Install mosquitto
#RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa -y
#RUN apt-get update
#RUN apt-get install -y mosquitto mosquitto-clients python-mosquitto

#RUN apt-get install -y make cmake libssl-dev rpm git build-essential uuid-dev xsltproc docbook-xsl libmagick-dev 
#RUN apt-get install -y wget
#RUN apt-get install -y libc-ares-dev
#RUN wget http://git.warmcat.com/cgi-bin/cgit/libwebsockets/snapshot/libwebsockets-1.3-chrome37-firefox30.tar.gz
#RUN tar -xzvf libwebsockets-1.3-chrome37-firefox30.tar.gz -C /
#WORKDIR /libwebsockets-1.3-chrome37-firefox30
#RUN mkdir build
#WORKDIR build
#RUN cmake .. -DOPENSSL_ROOT_DIR=/usr/bin/openssl
#RUN make
#RUN make install
#RUN ln -s /usr/local/lib/libwebsockets.so.4.0.0 /usr/lib/libwebsockets.so.4.0.0
#WORKDIR /
#RUN git config --global http.sslverify false
#RUN git clone https://git.eclipse.org/r/mosquitto/org.eclipse.mosquitto
#WORKDIR /org.eclipse.mosquitto
#RUN pwd
#RUN sed -i 's/WITH_WEBSOCKETS:=no/WITH_WEBSOCKETS:=yes/g' config.mk
#RUN make
##RUN make test
#RUN make install
#RUN useradd -r -m -d /var/lib/mosquitto -s /usr/sbin/nologin -g nogroup mosquitto
#
#ADD ./config/system/mosquitto /etc/init.d/
#ADD ./config/system/mosquitto.conf /etc/mosquitto/
#*********************************************************

#Install and config mysql
#RUN export DEBIAN_FRONTEND=noninteractive
#RUN apt-get install -q -y mysql-server
#RUN apt-get install -y mysql-client
#ADD ./config/mysql_startup.sh /opt/mysql_startup.sh
#RUN /opt/mysql_startup.sh

#Startup script
ADD config/startup.sh /
CMD /startup.sh

EXPOSE 8443 8080
