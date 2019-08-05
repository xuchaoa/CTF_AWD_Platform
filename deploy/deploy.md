全部基于ubuntu 18 LTS版本

安装mysql、redis 并在setting.py中配置连接信息

创建虚拟环境基于python3.6

安装requirements.txt中的依赖包
	如果报下面的错误
	OSError: mysql_config not found
	sudo apt-get install mysql-server mysql-client
    然后mysql -V查看mysql是否安装成功
    sudo  apt-get install libmysqlclient-dev python3-dev
    然后
    pip install mysqlclient就不会报错找不到'mysql_config'了
    
    
### docker install mysql 8.0 

docker pull mysql  #安装mysql 8.0

docker run -it --rm --name mysql -e MYSQL_ROOT_PASSWORD=SDUTctf123. -p 3306:3306 -d mysql 

进入容器
docker exec -it mysql bash 

新建ctf数据库
create database ctf;

## docker install redis
docker pull redis

docker run -d --name myredis -p 6379:6379 redis --requirepass "SDUTctf"  
  
python manage.py makemigrations

python manage.py migrate

# 创建管理员用户
python manage.py createsuperuser

### 运行celery异步任务
celery -A celery_tasks.main  worker --loglevel=info


  