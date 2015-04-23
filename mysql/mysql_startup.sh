#!/bin/bash

USER='openhab'
PASS='123456'
DBNAME='openhab'

if [ ! -f /var/lib/mysql/ibdata1 ]; then
    echo "=> Initializing MySQL data."
    mysql_install_db

fi
    echo "=> Starting MySQL server."
    /usr/bin/mysqld_safe &
    sleep 5s

    echo "=> Creating mysql database and user."
    mysql -uroot -e "CREATE DATABASE $DBNAME CHARACTER SET utf8 COLLATE utf8_general_ci;"
    mysql -uroot -e "CREATE USER '$USER'@'%' IDENTIFIED BY '$PASS';"
    mysql -uroot -e "GRANT ALL PRIVILEGES ON ${DBNAME}.* TO '$USER'@'%' IDENTIFIED BY '$PASS' WITH GRANT OPTION;"
    mysql -uroot -e "FLUSH PRIVILEGES;"

    echo "=> Done."

    killall mysqld
    sleep 5s

/usr/bin/mysqld_safe



