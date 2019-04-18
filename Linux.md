## Command

```
scp user@host:server_path ./
```

## VPS

```
yum -y install wget
wget -N --no-check-certificate https://raw.githubusercontent.com/ToyoDAdoubi/doubi/master/ssr.sh && chmod +x ssr.sh && bash ssr.sh

yum -y install wget
wget --no-check-certificate https://github.com/teddysun/across/raw/master/bbr.sh
chmod +x bbr.sh
./bbr.sh
```

## 私有PyPi

1. 安装pypiserver

```
pip install pypiserver
```

2. 创建模块存放路径

```
mkdir ~/packages
```

3. 安装所需库

```
sudo pip install passlib
sudo apt install apache2-utils -y
```

4. 生成帐号密码

```
htpasswd -sc ~/packages/.passwd.txt username
```

5. 启动服务

```
pypi-server -p 8080 -P ~/Desktop/packages/.passwd.txt --fallback-url http://pypi.douban.com/simple  ~/Desktop/packages
```

6. 配置.pypirc

```
vim ~/.pypirc

[distutils]
index-servers =
  local
[local]
repository: http://127.0.0.1:8080
username: root
password: 123abc.
```

7. 生成和上传

```
python setup.py register -r local && python setup.py sdist upload -r local
```

8. 安装包

```
pip install packagename==version --extra-index-url http://localhost:8080/
```