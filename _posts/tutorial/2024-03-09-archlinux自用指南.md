---
layout: post
title: Archlinux自用指南
date: 2024-03-09 08:51 +0800
category: [教程, linux]
tags: [archlinux, kde]
img_path: "/assets/img/posts/240309/"
image: 
    path: image.jpeg
    alt: Plasma6
pin: true
---

> 本文为 *自用* 指南，仅对本人负责，若您因本文而产生了困扰，概不负责
{: .prompt-warning }

KDE6顺利发布了，借此机会写一个安装指南完全版，用以后续重装系统参考用，以后也不再写新的安装记录了，有什么改动就直接修改这篇文章

## 系统安装

这一节是整个Archlinux系统从0到1的安装过程

### 准备工作

1. 下载[最新的镜像文件](https://archlinux.org/download/)并安装进U盘制作启动盘，这里选择UEFI模式下引导的GRUB启动。
2. 重启电脑进入BIOS关闭安全启动。
3. 插入U盘并重启，选择安装有镜像的U盘启动。

### 基本安装

#### 连接互联网

有线网忽略

#### 更新系统时间

```console
timedatectl set-ntp true
```

#### 建立分区

> 请看清楚要安装的硬盘名，以免造成意外的数据丢失
{: .prompt-warning }

```console
fdisk -l
```

这里我的硬盘为`/dev/nvme1n1`

##### 创建分区

```console
cfdisk /dev/nvme0n1
```

分区大小及类型参考下表

| 设备            |大小      |       类型        |
| :-------:      | :------: | :--------------: |
| /dev/nvme1n1p1 | 512M     |    EFI System    |
| /dev/nvme1n1p2 | 16G      |    Linux Swap    |
| /dev/nvme1n1p3 | 其余全部  | Linux filesystem |

> swap分区大小视电脑内存大小而定
{: .prompt-info }

##### 格式化分区

- 格式化efi分区
  
     ```console
     mkfs.vfat /dev/nvme1n1p1
     ```

- 格式化swap分区

     ```console
     mkswap /dev/nvme1n1p2
     ```

- 格式化根分区

     ```console
     mkfs.ext4 /dev/nvme1n1p3
     ```

##### 挂载分区

```console
mount /dev/nvme1n1p3 /mnt
mount --mkdir /dev/nvme1n1p1 /mnt/boot
swapon /dev/nvme1n1p2
```

#### 安装系统

##### 安装必需的软件包

> 注意，若CPU为intel，则安装intel-ucode，若为amd，则安装amd-ucode
{: .prompt-info }

这里选择linux-zen内核

```console
pacstrap -K /mnt linux-zen linux-zen-headers linux-firmware base base-devel vim amd-ucode networkmanager
```

##### 生成Fstab文件

```console
genfstab -U /mnt >> /mnt/etc/fstab
```

### 系统配置

#### 进入系统

```console
arch-chroot /mnt
```

#### 设置时区

```console
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

   ```console
   locale-gen
   ```

#### host配置

1. 创建 **/etc/hostname** 文件，输入主机名

   ```text
   Arch9000
   ```

2. 编辑 **/etc/hosts** 文件，输入以下内容

   ```text
   127.0.0.1   localhost
   ::1         localhost
   ```

3. 激活 NetworkManager服务，使其开机自启动

   ```console
   systemctl enable NetworkManager
   ```

#### GRUB安装

这里选择GRUB作为引导程序

1. 安装相关包

   ```console
   pacman -S grub efibootmgr os-prober
   ```

2. 配置grub

   ```console
   grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB
   grub-mkconfig -o /boot/grub/grub.cfg
   ```

3. 双系统配置

    编辑`/etc/default/grub`，取消`GRUB_DISABLE_OS_PROBER=false`前的注释，再重新执行

    ```console
    grub-mkconfig -o /boot/grub/grub.cfg
    ```

#### 设置root密码

```console
passwd
```

#### 结束安装

```console
exit
umount -R /mnt
reboot
```

## 桌面环境配置

### 基本桌面环境

#### zsh

我选择使用zsh作为默认shell

```console
pacman -S zsh
```

#### 添加用户

这里的haruto为用户名

```console
useradd -m haruto -G wheel,users,storage,adm -s /bin/zsh
```

##### 设置用户密码

```console
passwd haruto
```

##### 修改用户权限

```console
export EDITOR=vim
visduo
```

查找并取消注释以下行

```text
%wheel ALL=(ALL) ALL
```

#### 添加ArchlinuxCN仓库

编辑 **/etc/pacman.conf**

在末尾添加

```text
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

安装archlinuxcn-keyring

```console
pacman -Sy archlinuxcn-keyring
```

若在安装时报以下错

```text
error: archlinuxcn-keyring: Signature from "Jiachen YANG (Arch Linux Packager Signing Key) <farseerfc@archlinux.org>" is marginal trust
```

执行以下命令

```console
sudo pacman-key --lsign-key "farseerfc@archlinux.org"
```

再重新安装archlinuxcn-keyring

#### 显卡驱动

  > 请根据不同的显卡选择驱动安装，这里以amd核显+nvidia独显为例
  >
  > 若未开启对32位库的支持，请不要安装lib32开头的包
  >
  > 由于我使用的linux-zen内核，独显驱动仅安装`nvidia-dkms`

  ```console
  pacman -S mesa xf86-video-amdgpu vulkan-radeon lib32-mesa lib32-vulkan-radeon
  pacman -S nvidia-dkms
  ```

#### 声音相关

  ```console
  pacman -S alsa-utils pulseaudio
  ```

#### 字体

   ```console
   pacman -S noto-fonts-extra noto-fonts-emoji noto-fonts-cjk ttf-jetbrains-mono
   ```

#### 桌面环境

  ```console
  pacman -S plasma sddm konsole dolphin
  systemctl enable sddm
  ```

#### 输入法

1. 安装fcitx5输入法及相关包

   ```console
   pacman -S fcitx5-im fcitx5-chinese-addons fcitx5-pinyin-moegirl fcitx5-pinyin-zhwiki
   ```

2. 编辑文件 **/etc/environment**，输入

   ```text
   GTK_IM_MODULE=fcitx
   XMODIFIERS=@im=fcitx
   ```

#### 完成安装

以上全部安装完成后，重启

   ```console
   reboot
   ```

### KDE设置

#### 输入和输出

- 鼠标和触摸板

  - 鼠标

      重新绑定额外鼠标按键

  - 鼠标和触摸板->屏幕边缘

      全部改为无操作

- 键盘->虚拟键盘

   安装了fcitx5后选择`Wayland启动器`

- 声音->配置

   选择`自动切换所有当前音频流到新输出设备`

- 显示和监视器

   修改显示器分辨率

#### 外观和视觉风格

- 颜色和主题

  - 颜色

      选择喜欢的颜色

  - 窗口装饰元素

    - 配置标题栏按钮

      保留`此窗口的更多操作`、`保持在其他窗口之上`、`最小化`、`最大化`、`关闭`

    - 编辑微风主题（假设窗口装饰是微风）

      - 常规

         选中在关闭按钮周围绘制圆圈

      - 阴影和外框

         外框亮度选择关闭

  - 图标

      下载Tela

- 文字和字体->字体

   全部改为`Noto Sans CJK SC`，等宽使用`JetBrainsMonoNL`

#### 应用和窗口

- 通知

   停留时长改为2秒

- 窗口管理

  - 窗口行为

      窗口激活策略改为`焦点跟随鼠标`

- 任务切换器->主窗口

   取消选中`显示选中窗口`

- 桌面特效

   1. 取消选中`屏幕边缘高亮`

   2. 窗口背景虚化

      虚化程度左数第三档

      噪点程度最左档

   3. 窗口透明度

      ![opacity](opacity.png)

   4. 选择最小化过渡动画（神灯）

   5. 圆角

      安装`kwin-effect-rounded-corners-git`

      ```console
      paru kwin-effect-rounded-corners-git
      ```

- 活动

   修改名称和图标

#### 工作区

- 常规行为

   取消选择鼠标悬停时显示提示信息

   > 此项设置与图标任务管理器中的`悬停在任务上时显示窗口的小型预览`冲突
   {: .prompt-warn}

- 搜索

   `文件搜索`中`要索引的数据`选择`仅文件名`

### 应用软件

#### AUR

AUR的选择目前来看有两个，yay和paru

我选择paru

```console
sudo pacman -S paru
```

#### 通讯软件

##### QQ

```console
paru linuxqq
```

如果要让qq运行在wayland下

```text
--ozone-platform-hint=auto
--enable-wayland-ime
```
{: file='~/.config/qq-flags.conf'}

但是要注意目前wayland下qq的剪贴板无法和其他程序共享

##### telegram

> 截止2024/03/11 我遇到了telegram客户端的自动夜间模式失效的情况
>
> 参考[github的issue](https://github.com/telegramdesktop/tdesktop/issues/27431)
>
> 貌似一直都是坏的，就这样吧
{: .prompt-warn}

```console
paru telegram-desktop
```

#### 音乐

##### r3playx

等待网易云音乐官方linux版，r3也不错

```console
paru r3playx-bin
```

如果要让他跑在wayland下

```text
--enable-features=WaylandWindowDecorations
--ozone-platform-hint=auto
```
{: file='~/.config/electron28-flags.conf'}

> 注意在wayland下全局菜单会失效
{: .prompt-warn}

#### 编程

##### Visual Studio Code

```console
paru visual-studio-code-bin
```

如果要使用全局菜单，请在设置中将`Title Bar Style`改为`native`

##### Datagrip

```console
paru datagrip
paru datagrip-jre
```

后者是patche

#### 浏览器

##### Chrome

```console
paru google-chrome
```

如果要跑在wayland下

```text
--ozone-platform-hint=auto
--enable-wayland-ime
```
{: file='~/.config/chrome-flags.conf'}

#### 工具

##### Ark

##### OBS

##### Gwenview

##### Spectacle

##### Okular

##### KDEConnect

##### Clash-verge

##### Kate

#### 终端使用

##### konsole

新建一个配置方案

###### 外观

- 配色方案和字体

   选择`Breeze微风`

   字体选择`JetBrainsMonoNL`

- 光标

   形状选择`|字型`

   启用`闪烁`

- 杂项

   边距调整为5像素

   取消选中`调整大小后显示终端大小提示`

###### 滚动

   滚动条位置选择`隐藏`

   取消选中`高亮显示刚刚进入视图的行`

###### 鼠标

- 文本交互

   复制选项全部选中

- 杂项

   选中文件加下划线

##### oh-my-zsh

- 安装`oh-my-zsh`

   ```console
   paru oh-my-zsh-git
   ```

   安装完成后生成`.zshrc`文件

   ```console
   cp /usr/share/oh-my-zsh/zshrc ~/.zshrc
   ```

- 安装`zsh-autosuggestions`插件

   ```console
   git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
   ```

- 安装`fast-syntax-highlighting`插件

   ```console
   git clone https://github.com/zdharma-continuum/fast-syntax-highlighting.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/fast-syntax-highlighting
  ```

- 编辑`~/.zshrc`

   找到plugins行

   ```text
   plugins=(git extract zsh-autosuggestions fast-syntax-highlighting)
   ```
   {: file='~/.zshrc'}

##### fastfetch

- 安装`fastfetch`

   ```console
   paru fastfetch
   ```

- 生成配置文件

   ```console
   fastfetch --gen-config
   ```

- 编辑`~/.config/fastfetch/config.json`，删除不需要的项
