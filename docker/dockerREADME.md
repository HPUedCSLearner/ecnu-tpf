
#### docker 常用官方网站:
* https://hub.docker.com/
* https://docs.docker.com/
* https://download.docker.com/linux/

#### Docker快速入门:
* https://docker.easydoc.net

#### docker 离线安装：


#### docker windows 更改镜像安装位置：
* C:\Users\王枫\AppData\Local\Docker\wsl


```bash
PS C:\Users\王枫> wsl -l -v
  NAME                   STATE           VERSION
* docker-desktop-data    Running         2
  docker-desktop         Running         2
PS C:\Users\王枫> wsl --shutdown
PS C:\Users\王枫> wsl --export docker-desktop-data D:\docker\dockerAppImages\docker-desktop-data.tar
PS C:\Users\王枫> wsl --export  docker-desktop  D:\docker\dockerAppImages\docker-desktop.tar
PS C:\Users\王枫> wsl --unregister docker-desktop-data
正在注销...
PS C:\Users\王枫> wsl --unregister docker-desktop
正在注销...
PS C:\Users\王枫> wsl --import docker-desktop-data  D:\docker\dockerAppImages\image  D:\docker\dockerAppImages\docker-desktop-data.tar
PS C:\Users\王枫> wsl --import docker-desktop  D:\docker\dockerAppImages\bin  D:\docker\dockerAppImages\docker-desktop.tar
PS C:\Users\王枫> wsl -l -v
  NAME                   STATE           VERSION
* docker-desktop-data    Stopped         2
  docker-desktop         Running         2
重启docker
PS C:\Users\王枫> wsl -l -v
  NAME                   STATE           VERSION
* docker-desktop-data    Running         2
  docker-desktop         Running         2



  D:\docker\images-tars>docker load -i ubuntu-llvm.tar
fb3430f8db2e: Loading layer [==================================================>]  1.854GB/1.854GB
1122f5e490c2: Loading layer [==================================================>]  1.978GB/1.978GB
bc01da0580e9: Loading layer [==================================================>]  3.744GB/3.744GB
ae6b7a61f1fa: Loading layer [==================================================>]  1.495MB/1.495MB
Loaded image: ubuntu-llvm15:1.4
  

  D:\docker\images-tars>docker images -a
REPOSITORY      TAG       IMAGE ID       CREATED         SIZE
ubuntu-llvm15   1.4       00fbde1a1973   4 days ago      7.59GB
python          3.7       3e36461b4ff4   12 days ago     907MB
ubuntu          latest    a8780b506fa4   3 weeks ago     77.8MB
redis           latest    c2342258f8ca   4 weeks ago     117MB
centos          latest    5d0da3dc9764   14 months ago   231MB
  ```


#### docker windows安装, 更换镜像安装路径：
* 

#### docker离线安装并导入镜像:
* https://www.jianshu.com/p/1dd72a6b5ae9
```bash
docker save [images:tags] -o *.tar
docker load -i *.tar
docker save ubuntu-llvm15:1.4 -o ubuntu-llvm.tar #将ubuntu-llvm15:1.4的镜像导出成tar文件
docker load -i ubuntu-llvm.tar #将tar文件导入为ubuntu-llvm15:1.4的镜像
```
#### others
* vim /etc/apt/sources.list
* apt update / apt-get update
* apt install openssh-server vim gcc g++ cmake ninja(seems no)
* service ssh restart
* vim /ect/ssh/sshd_config -> PermitRootLogin yes
* ssh root@127.0.0.1 -p 8022

* ssh-keygen -t rsa -C 'cjdspace-learn' (其他的公钥git clone generate errors)
* git config --global alias.ci commit
* git config --global alias.co checkout
* git config --global alias.br branch
* git config --global alias.st status


* git clone -depth 1 git@github.com:llvm/llvm-project.git
* 发现使用ssh比hppts带宽大，并且push的时候，也不会出问题

#### docker cmd
```bash
docker ps
docker images
docker port [containerID/containName] # 查看容器端口情况

docker run [images][:Tag]
docker run -d -it -p 8022:22 --name myUbuntu ubuntu-sshd:1.1
docker run -d -it -p 8022:22 -v D:\docker\windowsDocument:/app ubuntu-gitpush:1.2
docker run -it -d -p 8025:22  --privileged=true ubuntu-llvm15:1.4  /sbin/init

docker commit -m -a [containerID] newImageName:[Tag]
docker commit -m="add sshd" -a="feng" e5624a341ed7 ubuntu-sshd:1.1
```
#### 在docker中使用systemctl:

* 参考链接:[docker中无法使用systemctl](https://aoyouer.com/posts/docker-systemctl/)
```bash
apt install init
docker run -it -d -p 8025:22  --privileged=true ubuntu-llvm15:1.4  /sbin/init
systemctl status ssh
```

##### 配置docker过程中一些重要的心得：
* 首先，用vscode链接Linux的时候，可以用 ssh root@127.0.0.1 -p 8022测试
* 可以用vscode链接后，需要可以从gethub克隆代码：有点坑的是，使用public key的时候，用使用这种方法生成的 ssh-keygen -t rsa -C，后者无法下载代码
* 可以克隆之后，发现无法push， 首先，使用ssh克隆网速快，其次，push的时候，不要使用https等克隆的仓库
* 另外，clone push的时候，使用代理网络，可能会导致失败；

