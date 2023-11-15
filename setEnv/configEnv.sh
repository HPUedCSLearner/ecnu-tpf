
#build-essential
sudo apt install ninja-build  build-essential net-tools htop



#git
sudo apt install git
git config --global alias.ci commit
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status

#git user name
git config --global user.email "yoga13s-wsl2-ubuntu22.04"
git config --global user.name "wangfeng"


#挂载磁盘
# sudo mount /dev/sdb1 /home/feng/disk/disk1
# sdb      8:16   0 931.5G  0 disk 
# ├─sdb1   8:17   0   233G  0 part /home/feng/disk/disk1
# ├─sdb2   8:18   0 509.3G  0 part 
# └─sdb3   8:19   0 188.7G  0 part
# 卸载磁盘
# sudo umount /dev/sdb1
# sudo umount /home/feng/disk/disk1
