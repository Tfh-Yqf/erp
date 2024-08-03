FROM mysql:8.0


# 创建数据库和用户
RUN service mysql start && \
    mysql -e "CREATE DATABASE erp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" && \
    mysql -e "CREATE USER 'root'@'localhost' IDENTIFIED BY 'ERPSYSTE';" && \
    mysql -e "GRANT ALL PRIVILEGES ON erp_db.* TO 'root'@'localhost';" && \
    mysql -e "FLUSH PRIVILEGES;"

# 暴露端口
EXPOSE 3306
