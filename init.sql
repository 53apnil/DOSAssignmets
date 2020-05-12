use mysql;
update user set plugin='mysql_native_password' where user='root';
flush privileges;
