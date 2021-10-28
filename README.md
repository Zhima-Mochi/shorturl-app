# Overview
The application is used to shorten long url, and the short url is valid until the application is down or 6-digit codes generated for short url is almost exhausted (how can that be?) .
# Requirement
- Program: [Docker](https://www.docker.com/)
- Environment: Unix/Linux
# Getting started
```bash
# download the code
git clone https://github.com/Zhima-Mochi/shorturl-app.git
cd shorturl-app
# generate the passwords for database (default: password)
src/init.sh
# change the passwords for free
vim secrets/db_shorturl_password
vim secrets/db_shorturl_root_password
# build and run the application
docker-compose up
```
Now, have fun with http://localhost:56643/.
# Demo
![](/src/examples/main_page.png)
