docker run -d --rm --name mysql  -v  /D/mysql:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root  mysql

docker run -d --rm --name phpmyadmin -p 8080:80 --link mysql:db phpmyadmin/phpmyadmin

docker run -itd -p 8050:8050 --rm scrapinghub/splash


