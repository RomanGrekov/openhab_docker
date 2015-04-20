# Openhab installation file

FROM hypriot/rpi-java
MAINTAINER Roman Grekov <roman.grekov88@gmail.com>

RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties
RUN apt-get install -y vim

# Install mosquitto
#RUN apt-add-repository ppa:mosquitto-dev/mosquitto-ppa -y
#RUN apt-get update
#RUN apt-get install -y mosquitto mosquitto-clients python-mosquitto

RUN apt-get install -y make cmake libssl-dev rpm git build-essential uuid-dev xsltproc docbook-xsl libmagick-dev 
RUN apt-get install -y wget
RUN apt-get install -y libc-ares-dev
RUN wget http://git.warmcat.com/cgi-bin/cgit/libwebsockets/snapshot/libwebsockets-1.3-chrome37-firefox30.tar.gz
RUN tar -xzvf libwebsockets-1.3-chrome37-firefox30.tar.gz -C /
WORKDIR /libwebsockets-1.3-chrome37-firefox30
RUN mkdir build
WORKDIR build
RUN cmake .. -DOPENSSL_ROOT_DIR=/usr/bin/openssl
RUN make
RUN make install
RUN ln -s /usr/local/lib/libwebsockets.so.4.0.0 /usr/lib/libwebsockets.so.4.0.0
WORKDIR /
RUN git config --global http.sslverify false
RUN git clone https://git.eclipse.org/r/mosquitto/org.eclipse.mosquitto
WORKDIR /org.eclipse.mosquitto
RUN pwd
RUN sed -i 's/WITH_WEBSOCKETS:=no/WITH_WEBSOCKETS:=yes/g' config.mk
RUN make
#RUN make test
RUN make install
RUN useradd -r -m -d /var/lib/mosquitto -s /usr/sbin/nologin -g nogroup mosquitto

ADD ./mosquitto /etc/init.d/
ADD ./mosquitto.conf /etc/mosquitto/
#*********************************************************

#Startup script
CMD /etc/init.d/mosquitto start

EXPOSE 1883 1888 1889
