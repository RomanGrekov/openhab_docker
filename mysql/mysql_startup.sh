#!/bin/bash

echo "=> Initializing MySQL data."
mysql_install_db

echo "=> Starting MySQL server."
/usr/bin/mysqld_safe &

echo "=> Waiting for MySQL server."
while (true); do
    echo "     waiting for 3 s..."
    sleep 3s
    mysql -uroot -e "status" > /dev/null 2>&1 && break
done

echo "=> Creating mysql database and user."
DBNAME='openhab'
PASS='123456'
mysql -uroot -e "CREATE DATABASE $DBNAME CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -uroot -e "CREATE USER $DBNAME@localhost IDENTIFIED BY '$PASS';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON ${DBNAME}.* TO $DBNAME@localhost;"
mysql -uroot -e "FLUSH PRIVILEGES;"

echo "=> Done."




