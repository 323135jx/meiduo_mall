
from pymysql import install_as_MySQLdb

# 适配调整，作用：把所有使用mysqlclient，改为使用pymysql
install_as_MySQLdb()