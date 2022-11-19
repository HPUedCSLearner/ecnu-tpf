
#### docker 常用官方网站:
* https://hub.docker.com/
* https://docs.docker.com/
* https://download.docker.com/linux/

#### Docker快速入门:
* https://docker.easydoc.net

#### docker 离线安装：


#### docker离线安装并导入镜像:
* https://www.jianshu.com/p/1dd72a6b5ae9

#### others
* vim /etc/apt/sources.list
* apt update / apt-get update
* apt install openssh-server vim gcc g++ cmake ninja(seems no)
* service ssh restart
* vim /ect/ssh/sshd_config -> PermitRootLogin yes
* ssh root@127.0.0.1 -p 8022

* git config --global alias.ci commit
* git config --global alias.co checkout
* git config --global alias.br branch
* git config --global alias.st status

#### docker cmd
docker ps
docker images
docker port [containerID/containName] # 查看容器端口情况

docker run [images][:Tag]
docker run -d -it -p 8022:22 --name myUbuntu ubuntu-sshd:1.1

docker commit -m -a [containerID] newImageName:[Tag]
docker commit -m="add sshd" -a="feng" e5624a341ed7 ubuntu-sshd:1.1

