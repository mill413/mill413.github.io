---
layout: post
title: ArchLinux安装记录二
date: 2023-10-02 18:28 +0800
category: [记录,Archlinux]
tags: [archlinux,kde,wayland]
---

> 请注意本文时效性
{: .prompt-warning }

由于用了几个月之后太多软件在硬盘里拉屎（指config），我选择直接重装系统，并对之前写的安装步骤做一些优化，比如删去xorg,更换内核等

## 准备工作

1. 下载[ArchLinux-2023.09.01](https://archlinux.org/download/)镜像并安装进U盘制作启动盘，这里选择UEFI模式下引导的GRUB启动。
2. 重启电脑进入BIOS关闭安全启动。
3. 插入U盘并重启，选择安装有镜像的U盘启动。

## 进入archiso

以下步骤均在**archiso**里进行

### 连接互联网

有线网可忽略

### 更新系统时间

```bash
timedatectl set-ntp true
```

查看系统时间是否正确

```bash
timedatectl status
```

### 建立分区

#### 查看硬盘设备名

   ```bash
   fdisk -l
   ```

这里我的硬盘名为`/dev/nvme0n1`

#### 修改分区表

   ```bash
   cfdisk /dev/nvme0n1
   ```

   分区大小及类型参考下表

   |   设备    |   大小   |       类型       |
   | :-------: | :------: | :--------------: |
   | /dev/nvme0n1p1 |   512M   |    EFI System    |
   | /dev/nvme0n1p2 |    16G    |    Linux Swap    |
   | /dev/nvme0n1p3 | 其余全部 | Linux filesystem |

> swap分区大小视电脑内存大小而定
{: .prompt-info }

#### 格式化分区

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

#### 挂载分区

   ```bash
   mount /dev/nvme0n1p3 /mnt
   mount --mkdir /dev/nvme0n1p1 /mnt/boot
   swapon /dev/nvme0n1p2
   ```

### 安装系统

#### 安装必需的软件包

> 注意，若CPU为intel，则安装intel-ucode，若为amd，则安装amd-ucode

```bash
pacstrap -K /mnt linux-zen linux-zen-headers linux-firmware base base-devel vim amd-ucode networkmanager
```

#### 生成Fstab文件

```bash
genfstab -U /mnt >> /mnt/etc/fstab
```

#### 进入系统

```bash
arch-chroot /mnt
```

#### 设置时区

```bash
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
```

#### 本地化

1. 编辑 **/etc/locale.gen** 文件，取消 **en_US.UTF-8 UTF-8** 和 **zh_CN.UTF-8 UTF-8** 前的注释

2. 创建 **/etc/locale.conf** ，并输入

   ```text
   LANG=en_US.UTF-8
   ```

3. 执行

   ```bash
   locale-gen
   ```

#### 网络配置

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

#### 设置root密码

```bash
passwd
```

#### 安装引导程序

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

*若电脑为双系统，请先挂载另一系统引导程序所在磁盘，并执行`os-prober`后，再进行grub配置*

#### 结束安装

```bash
exit
umount -R /mnt
reboot
```

拔掉U盘，完成安装

## 系统设置

### zsh配置

我选择使用zsh替代bash作为默认shell

```bash
pacman -S zsh
```

#### 修改默认shell

```zsh
chsh -s /bin/zsh
```

### 添加非root用户

添加用户，这里的haruto为用户名

```zsh
useradd -m haruto -G wheel,users,storage,adm -s /bin/zsh
```

#### 设置用户密码

```bash
passwd haruto
```

#### 修改用户权限

我在修改权限时使用`visudo`命令出现了错误，这里选择直接修改`/etc/sudoers`文件

```bash
chmod +w /etc/sudoers
vim /etc/sudoers
chmod -w /etc/sudoers
```

查找并取消注释以下行

```text
%wheel ALL=(ALL) ALL
```

### 添加ArchlinuxCN仓库

编辑 **/etc/pacman.conf**

在末尾添加

```text
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

安装archlinuxcn-keyring

```zsh
pacman -Sy archlinuxcn-keyring
```

### 添加对32位库支持

编辑 **/etc/pacman.conf**

去掉以下两行的注释

```text
# [multilib] 
# Include = /etc/pacman.d/mirrorlist
```

执行

```zsh
pacman -Syu
```

## 安装软件包

### AUR(Arch User Repository)
  
  我选择使用较新的`paru`替代`yay`

  ```zsh
  pacman -S paru
  ```

### 显卡驱动

  > 请根据不同的显卡选择驱动安装，这里以amd核显+nvidia独显为例
  >
  > 若未开启对32位库的支持，请不要安装lib32开头的包
  >
  > 由于我使用的linux-zen内核，独显驱动仅安装`nvidia-dkms`

  ```zsh
  pacman -S mesa xf86-video-amdgpu vulkan-radeon lib32-mesa lib32-vulkan-radeon
  pacman -S nvidia-dkms
  ```

### 声音相关
  
  ```zsh
  pacman -S alsa-utils pulseaudio
  ```

### 显示服务和桌面环境

   我选择使用只有wayland下的plasma桌面环境

  ```zsh
  pacman -S plasma sddm konsole dolphin plasma-wayland-session
  systemctl enable sddm
  ```

### 字体

   ```bash
   pacman -S noto-fonts-extra noto-fonts-emoji noto-fonts-cjk ttf-jetbrains-mono
   ```

### 输入法

1. 安装fcitx5输入法及相关包

   ```zsh
   pacman -S --noconfirm fcitx5-im fcitx5-chinese-addons fcitx5-pinyin-moegirl fcitx5-pinyin-zhwiki  fcitx5-qt fcitx5-gtk
   ```

2. 编辑文件 **/etc/environment**，输入

   ```text
   GTK_IM_MODULE=fcitx
   QT_IM_MODULE=fcitx
   XMODIFIERS=@im=fcitx
   ```

### 重启

```zsh
reboot
```

## 参考

1. [ArchLinux安装记录 \| 彩虹岛](https://mill413.github.io/posts/ArchLinux%E5%AE%89%E8%A3%85%E8%AE%B0%E5%BD%95/)

2. [安装指南 - Arch Linux中文维基](https://wiki.archlinuxcn.org/wiki/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97)
