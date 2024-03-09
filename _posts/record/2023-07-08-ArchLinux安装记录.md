---
title: ArchLinux安装记录
date: 2023-03-09 20:43:00 +0800
categories: [记录]
tags: [archlinux]
---

> 请注意本文时效性
{: .prompt-warning }

## 0 准备工作

1. 下载[ArchLinux-2023.03.01](https://archlinux.org/download/)镜像并安装进U盘制作启动盘，这里选择UEFI模式下引导的GRUB启动。
2. 重启电脑进入BIOS关闭安全启动。
3. 插入U盘并重启，选择安装有镜像的U盘启动。

## 1 连接互联网

有线网可忽略

## 2 更新系统时间

```bash
timedatectl set-ntp true
```

查看系统时间是否正确

```bash
timedatectl status
```

## 3 建立分区

### 3.0 查看硬盘设备名称

   ```bash
   fdisk -l
   ```

### 3.1 修改分区表

   ```bash
   cfdisk /dev/nvme0n1
   ```

   分区大小及类型参考下表

   |   设备    |   大小   |       类型       |
   | :-------: | :------: | :--------------: |
   | /dev/nvme0n1p1 |   512M   |    EFI System    |
   | /dev/nvme0n1p2 |    4G    |    Linux Swap    |
   | /dev/nvme0n1p3 | 其余全部 | Linux filesystem |

### 3.2 格式化分区

- 格式化efi分区
  
     ```bash
     mkfs.vfat /dev/nvme0n1p1
     ```

- 格式化swap分区

     ```bash
     mkswap /dev/nvme0n1p2
     ```

- 格式化根分区

     ```bash
     mkfs.ext4 /dev/nvme0n1p3
     ```

### 3.3 挂载分区

   ```bash
   mount /dev/nvme0n1p3 /mnt
   mount --mkdir /dev/nvme0n1p1 /mnt/boot
   swapon /dev/nvme0n1p2
   ```

## 4 安装

### 4.0 选择镜像

### 4.1 安装必需的软件包

> 注意，若CPU为intel，则安装intel-ucode，若为amd，则安装amd-ucode

```bash
pacstrap -K /mnt linux linux-firmware linux-headers base base-devel vim bash-completion amd-ucode networkmanager
```

## 5 配置系统

### 5.1 生成Fstab文件

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

### 5.2 进入系统

```bash
arch-chroot /mnt
```

### 5.3 设置时区

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
```

### 5.4 本地化

1. 编辑 **/etc/locale.gen** 文件，取消 **en_US.UTF-8 UTF-8** 和 **zh_CN.UTF-8 UTF-8** 前的注释

2. 创建 **locale.conf** ，并输入

   ```text
   LANG=en_US.UTF-8
   ```

3. 执行

   ```bash
   locale-gen
   ```

### 5.5 网络配置

1. 创建 **/etc/hostname** 文件，输入主机名

   ```text
   Arch9000
   ```

2. 编辑 **/etc/hosts** 文件，输入以下内容

   ```text
   127.0.0.1   localhost
   ::1         localhost
   127.0.1.1   Arch9000.localdomain Arch9000
   ```

3. 激活 NetworkManager服务，使其开机自启动

   ```bash
   systemctl enable NetworkManager
   ```

### 5.6 设置root密码

```bash
passwd
```

### 5.7 安装引导程序

这里选择GRUB作为引导程序

1. 安装相关包

   ```bash
   pacman -S grub efibootmgr os-prober
   ```

2. 配置grub

   ```bash
   grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
   grub-mkconfig -o /boot/grub/grub.cfg
   ```

## 6 结束安装

```bash
exit
umount -R /mnt
reboot
```

拔掉U盘，完成安装

## 7 基本设置

### 7.0 bash配置

```bash
cd /etc/skel
vim .bashrc
```

在alias行上面添加

```text
export EDITOR=vim
```

然后将文件复制到home目录下

```bash
cp -a . ~
```

刷新配置

```bash
source ~/.bashrc
```

### 7.1 添加非root用户

添加用户，这里的haruto为用户名

```bash
useradd -m -G wheel,users,storage,adm haruto
```

设置密码

```bash
passwd haruto
```

修改权限

```bash
visudo
```

查找并取消注释以下行

```text
%wheel ALL=(ALL) ALL
```

### 7.2 添加ArchlinuxCN仓库

编辑文件

```bash
vim /etc/pacman.conf
```

在末尾添加

```text
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

安装archlinuxcn-keyring

```bash
pacman -Sy archlinuxcn-keyring
```

### 7.3 添加对32位库支持

编辑 **/etc/pacman.conf**

去掉以下两行的注释

```text
# [multilib] 
# Include = /etc/pacman.d/mirrorlist
```

执行

```bash
pacman -Syu
```

## 8 安装软件

### 8.0 yay
  
  ```bash
  sudo pacman -S yay
  ```

### 8.1 显卡驱动

  > 请根据不同的显卡选择驱动安装，这里以amd核显+nvidia独显为例
  > 若未开启对32位库的支持，请不要安装lib32开头的包

  ```bash
  sudo pacman -S mesa xf86-video-amdgpu vulkan-radeon lib32-mesa lib32-vulkan-radeon
  sudo pacman -S nvidia nvidia-settings nvidia-utils lib32-nvidia-utils
  ```

### 8.2 声音相关
  
  ```bash
  sudo pacman -S alsa-utils pulseaudio
  ```

### 8.3 显示服务和桌面环境

  ```bash
  sudo pacman -S xorg plasma sddm konsole dolphin
  systemctl enable sddm
  ```

### 8.4 字体

   ```bash
   sudo pacman -S noto-fonts-extra noto-fonts-emoji noto-fonts-cjk adobe-source-han-sans-cn-fonts adobe-source-han-serif-cn-fonts ttf-jetbrains-mono
   ```

### 8.5 输入法

1. 安装fcitx5输入法及相关包

   ```bash
   sudo pacman -S --noconfirm fcitx5-im fcitx5-chinese-addons fcitx5-material-color fcitx5-pinyin-moegirl fcitx5-pinyin-zhwiki  fcitx5-qt fcitx5-gtk
   ```

2. 编辑文件 **/etc/environment**，输入

   ```text
   GTK_IM_MODULE=fcitx
   QT_IM_MODULE=fcitx
   XMODIFIERS=@im=fcitx
   ```

重新登录

```bash
reboot
```

### 8.6 其他软件

1. SNS

   (1) QQ

      ```bash
      yay -S linuxqq
      ```

   (2) 微信

   > 先开启32位库支持

      ```bash
      yay -S deepin-wine-wechat
      ```

2. 浏览器

   edge

      ```bash
      yay -S microsoft-edge-stable-bin
      ```

3. 影音

   (1) vlc

   ```bash
   yay -S vlc
   ```

   (2) YesPlayMusic

   ```bash
   yay -S yesplaymusic
   ```

4. 工具

   (1) vscode

      ```bash
      yay -S visual-studio-code-bin
      ```

   (2) clash for windows

      ```bash
      yay -S clash-for-windows-bin
      ```

   (3) pycharm

      ```bash
      yay -S pycharm-professional
      ```

   (4) v2raya

   1. 安装v2ray内核和v2raya

      ```bash
      yay -S v2ray v2raya
      ```

   2. 设置开机自启

      ```bash
      sudo systemctl enable v2raya
      sudo systemctl start v2raya
      ```

5. 其他

   (1) cuda

      1. 下载特定版本cuda，参考[`该网站`](https://archive.archlinux.org/packages/c/cuda/)

      2. 本地安装

         ```bash
         yay -U <package-name>
         ```

   (2) anaconda

### 8.7 美化

1. 主题设置

   (1) Layan

   (2) kvantum

2. 终端美化

   (1) zsh

   (2) oh-my-zsh

   (3) konsole配置

3. 面板挂件

   (1) window title

   (2) windows buttons

4. GRUB美化

   (1) os-prober

   (2) 主题安装

## 参考

1. [安装指南 - Arch Linux中文维基](https://wiki.archlinuxcn.org/wiki/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97)
2. [网络配置 - Arch Linux中文维基](https://wiki.archlinuxcn.org/wiki/%E7%BD%91%E7%BB%9C%E9%85%8D%E7%BD%AE)
3. [GRUB - Arch Linux中文维基](https://wiki.archlinuxcn.org/wiki/GRUB)
4. [建议阅读 - Arch Linux中文维基](https://wiki.archlinuxcn.org/wiki/%E5%BB%BA%E8%AE%AE%E9%98%85%E8%AF%BB)
5. [archlinux 显卡驱动 archlinux 简明指南](https://arch.icekylin.online/guide/rookie/graphic-driver.html)
6. [简体中文本地化 - Arch Linux中文维基](https://wiki.archlinuxcn.org/wiki/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87%E6%9C%AC%E5%9C%B0%E5%8C%96)
7. [Fcitx5 - Arch Linux中文维基](https://wiki.archlinuxcn.org/wiki/Fcitx5)
8. [Arch（KDE Plasma）中文化_arch安装中文字体_CoinSkydiver804的博客-CSDN博客](https://blog.csdn.net/qingtian805/article/details/123187337)
9. [用 fontconfig 治理 Linux 中的字体 - 双猫CC](https://catcat.cc/post/2021-03-07/)
10. [超简单的Arch Linux+Windows双启动配置教程 - 知乎](https://zhuanlan.zhihu.com/p/471374126)
11. [vinceliuice/grub2-themes: Modern Design theme for Grub2](https://github.com/vinceliuice/grub2-themes)
12. [GRUB -  Arch Linux 中文维基](https://wiki.archlinuxcn.org/wiki/GRUB#%E6%8E%A2%E6%B5%8B%E5%85%B6%E4%BB%96%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F)
13. [archLinux装微信两种方法以及问题解决办法_archlinux安装微信_蓝元风的博客-CSDN博客](https://blog.csdn.net/bluevitwind/article/details/127453816)
14. [Index of /packages/c/cuda/](https://archive.archlinux.org/packages/c/cuda/)
15. [ArchLinux忽略某个包的升级 - Jiajun的编程随想](https://jiajunhuang.com/articles/2019_12_22-archlinux_ignore_pkg.md.html)
16. [linux系统修改启动引导时间,通过Grub调整提高Linux系统启动速度的方法_就爱吃鱼的博客-CSDN博客](https://blog.csdn.net/weixin_31585653/article/details/116645496)
17. [V2RayA——新一代Linux客户端安装配置教程 \| SKY博客](https://www.sky350.com/1210.html)
