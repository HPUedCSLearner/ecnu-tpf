
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

* ssh-keygen -t rsa -C 'cjdspace-learn' (其他的公钥git clone generate errors)
* git config --global alias.ci commit
* git config --global alias.co checkout
* git config --global alias.br branch
* git config --global alias.st status


* git clone -depth 1 git@github.com:llvm/llvm-project.git
* 发现使用ssh比hppts带宽大，并且push的时候，也不会出问题

#### docker cmd
docker ps
docker images
docker port [containerID/containName] # 查看容器端口情况

docker run [images][:Tag]
docker run -d -it -p 8022:22 --name myUbuntu ubuntu-sshd:1.1

docker commit -m -a [containerID] newImageName:[Tag]
docker commit -m="add sshd" -a="feng" e5624a341ed7 ubuntu-sshd:1.1


##### 配置docker过程中一些重要的心得：
* 首先，用vscode链接Linux的时候，可以用 ssh root@127.0.0.1 -p 8022测试
* 可以用vscode链接后，需要可以从gethub克隆代码：有点坑的是，使用public key的时候，用使用这种方法生成的 ssh-keygen -t rsa -C，后者无法下载代码
* 可以克隆之后，发现无法push， 首先，使用ssh克隆网速快，其次，push的时候，不要使用https等克隆的仓库
* 另外，clone push的时候，使用代理网络，可能会导致失败；

