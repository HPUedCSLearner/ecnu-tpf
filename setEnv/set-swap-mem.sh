# 设置16G 虚拟内存 用于项目编译
# 开机重启后，swap内存复原

# 创建分区路径
sudo mkdir -p /var/cache/swap/

# 设置分区的大小 64M * 64 = 4096MB=4GB
# sudo dd if=/dev/zero of=/var/cache/swap/swap0 bs=64M count=64

# 64M * 64 = 4096MB=16GB
sudo dd if=/dev/zero of=/var/cache/swap/swap0 bs=64M count=256

# 设置该目录权限 (rw-------)
sudo chmod 0600 /var/cache/swap/swap0

# 创建SWAP文件
sudo mkswap /var/cache/swap/swap0

# 激活SWAP文件
sudo swapon /var/cache/swap/swap0

# 查看SWAP信息是否正确
# sudo swapon -s

# swap0文件的路径在/var/cache/swap/下，编译完后, 如果不想要交换分区了, 可以删除。
# 删除交换分区的命令：
# sudo swapoff /var/cache/swap/swap0
# sudo rm /var/cache/swap/swap0

# 释放空间命令：
# sudo swapoff -a