---
layout: post
title: Archlinux自用指南
date: 2024-03-09 08:51 +0800
category: [教程, Archlinux]
tags: [archlinux, kde, wayland]
media_subpath: "/assets/img/posts/240309/"
image: 
    path: image.jpeg
    alt: Plasma6
pin: true
---

> 本文为 *自用* 指南，仅对本人负责，若您因本文而产生了困扰，概不负责
{: .prompt-warning }

KDE6顺利发布了，借此机会写一个安装指南完全版，用以后续重装系统参考用，以后也不再写新的安装记录了，有什么改动就直接修改这篇文章

## 1 系统安装

这一节是整个Archlinux系统从0到1的安装过程

### 1.1 准备工作

1. 下载[最新的镜像文件](https://archlinux.org/download/)并安装进U盘制作启动盘，这里选择UEFI模式下引导的GRUB启动。
2. 重启电脑进入BIOS关闭安全启动。
3. 插入U盘并重启，选择安装有镜像的U盘启动。

### 1.2 基本安装

#### 1.2.1 连接互联网

有线网忽略

#### 1.2.2 更新系统时间

```console
timedatectl set-ntp true
```

#### 1.2.3 建立分区

> 请看清楚要安装的硬盘名，以免造成意外的数据丢失
{: .prompt-warning }

```console
fdisk -l
```

这里我的硬盘为`/dev/nvme1n1`

##### 1.2.3.1 创建分区

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

##### 1.2.3.2 格式化分区

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

##### 1.2.3.3 挂载分区

```console
mount /dev/nvme1n1p3 /mnt
mount --mkdir /dev/nvme1n1p1 /mnt/boot
swapon /dev/nvme1n1p2
```

#### 1.2.4 安装系统

##### 1.2.4.1 安装必需的软件包

> 注意，若CPU为intel，则安装intel-ucode，若为amd，则安装amd-ucode
{: .prompt-info }

这里选择linux-zen内核

```console
pacstrap -K /mnt linux-zen linux-zen-headers linux-firmware base base-devel vim amd-ucode networkmanager
```

##### 1.2.4.2 生成Fstab文件

```console
genfstab -U /mnt >> /mnt/etc/fstab
```

### 1.3 系统配置

#### 1.3.1 进入系统

```console
arch-chroot /mnt
```

#### 1.3.2 设置时区

```console
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
hwclock --systohc
```

#### 1.3.3 本地化

   1. 编辑 **/etc/locale.gen** 文件，取消 **en_US.UTF-8 UTF-8** 和 **zh_CN.UTF-8 UTF-8** 前的注释

   2. 创建 **/etc/locale.conf** ，并输入

      ```plaintext
      LANG=en_US.UTF-8
      ```

   3. 执行

      ```console
      locale-gen
      ```

#### 1.3.4 host配置

   1. 创建 **/etc/hostname** 文件，输入主机名

      ```plaintext
      Arch9000
      ```

   2. 编辑 **/etc/hosts** 文件，输入以下内容

      ```plaintext
      127.0.0.1   localhost
      ::1         localhost
      ```

   3. 激活 NetworkManager服务，使其开机自启动

      ```console
      systemctl enable NetworkManager
      ```

#### 1.3.5 GRUB安装

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

#### 1.3.6 设置root密码

```console
passwd
```

#### 1.3.7 结束安装

```console
exit
umount -R /mnt
reboot
```

## 2 桌面环境配置

### 2.1 基本桌面环境

#### 2.1.1 zsh

我选择使用zsh作为默认shell

```console
pacman -S zsh
```

#### 2.1.2 添加用户

这里的haruto为用户名

```console
useradd -m haruto -G wheel,users,storage,adm -s /bin/zsh
```

##### 2.1.2.1 设置用户密码

```console
passwd haruto
```

##### 2.1.2.2 修改用户权限

```console
export EDITOR=vim
visduo
```

查找并取消注释以下行

```plaintext
%wheel ALL=(ALL) ALL
```

#### 2.1.3 添加ArchlinuxCN仓库

编辑 **/etc/pacman.conf**

在末尾添加

```plaintext
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

安装archlinuxcn-keyring

```console
pacman -Sy archlinuxcn-keyring
```

若在安装时报以下错

```plaintext
error: archlinuxcn-keyring: Signature from "Jiachen YANG (Arch Linux Packager Signing Key) <farseerfc@archlinux.org>" is marginal trust
```

执行以下命令

```console
sudo pacman-key --lsign-key "farseerfc@archlinux.org"
```

再重新安装archlinuxcn-keyring

#### 2.1.4 显卡驱动

> 请根据不同的显卡选择驱动安装，这里以amd核显+nvidia独显为例
>
> 若未开启对32位库的支持，请不要安装lib32开头的包
>
> ~~由于我使用的linux-zen内核，独显驱动仅安装`nvidia-dkms`~~
> 对于Turing架构及之后的显卡，请使用`nvidia-open`或其他相关的显卡驱动

```console
pacman -S mesa xf86-video-amdgpu vulkan-radeon lib32-mesa lib32-vulkan-radeon
pacman -S nvidia-open
```

#### 2.1.5 声音相关

```console
pacman -S alsa-utils pulseaudio
```

#### 2.1.6 字体

```console
pacman -S noto-fonts-extra noto-fonts-emoji noto-fonts-cjk ttf-jetbrains-mono
```

> 由于打包变化，字体可能会fallback到非预期的字形上，请安装`noto-fonts-cjk-conf`
{: .prompt-info}

#### 2.1.7 桌面环境

```console
pacman -S plasma sddm konsole dolphin
systemctl enable sddm
```

#### 2.1.8 输入法

1. 安装fcitx5输入法及相关包

   ```console
   pacman -S fcitx5-im fcitx5-chinese-addons fcitx5-pinyin-moegirl fcitx5-pinyin-zhwiki
   ```

2. 编辑文件 **/etc/environment**，输入

   ```plaintext
   GTK_IM_MODULE=fcitx
   XMODIFIERS=@im=fcitx
   ```

#### 2.1.9 完成安装

以上全部安装完成后，重启

```console
reboot
```

### 2.2 KDE设置

#### 2.2.1 输入和输出

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

#### 2.2.2 外观和视觉风格

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

#### 2.2.3 应用和窗口

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

- 全屏隐藏标题栏

   编辑`~/.config/kwinrc`，在`[Windows]`下添加
   ```text
   BorderlessMaximizedWindows=true
   ```

#### 2.2.4 工作区

- 常规行为

   取消选择`鼠标悬停时显示提示信息`

   > 此项设置与图标任务管理器中的`悬停在任务上时显示窗口的小型预览`冲突
   {: .prompt-warning }

- 搜索

   `文件搜索`中`要索引的数据`选择`仅文件名`

#### 2.2.5 面板挂件

- 窗口标题和窗口按钮

  ```console
  paru plasma-applet-window-buttons
  paru plasma6-applets-window-title
  ```

- 面板美化

   ```console
   paru plasma6-applets-panel-colorizer
   ```

### 2.3 应用软件

#### 2.3.1 AUR

AUR的选择目前来看有两个，yay和paru

我选择paru

```console
sudo pacman -S paru
```

#### 2.3.2 通讯软件

- QQ

  ```console
  paru linuxqq
  ```

  如果要让qq运行在wayland下

  ```plaintext
  --ozone-platform-hint=auto
  --enable-wayland-ime
  ```
  {: file='~/.config/qq-flags.conf'}

   但是要注意目前wayland下qq点击截屏会闪退~~，且不论是否跑在Wayland下均无法拖拽文件~~

- telegram

  > 截止2024/03/11 我遇到了telegram客户端的自动夜间模式失效的情况
  >
  > 参考[github的issue](https://github.com/telegramdesktop/tdesktop/issues/27431)
  >
  > 貌似一直都是坏的，就这样吧
  {: .prompt-warning }

  ```console
  paru telegram-desktop
  ```

- 微信

  ```console
  paru wechat-uos-bwrap
  ```

#### 2.3.3 音乐

- r3playx

  等待网易云音乐官方linux版，r3也不错

  ```console
  paru r3playx-bin
  ```

  如果要让他跑在wayland下，编辑配置文件

  ```plaintext
  --enable-features=WaylandWindowDecorations
  --ozone-platform-hint=auto
  ```
  {: file='~/.config/electron28-flags.conf'}

  > 注意在wayland下全局菜单会失效
   {: .prompt-warning }

#### 2.3.4 编程

- Visual Studio Code

  ```console
  paru visual-studio-code-bin
  ```

  如果要使用全局菜单，请在设置中将`Title Bar Style`改为`native`

  > Title Bar Style修改为native后，如果此时主侧栏在右侧，点击右下角的管理按钮，弹出菜单不会在正确的位置
  {: .prompt-warning}

- Datagrip

  ```console
  paru datagrip
  paru datagrip-jre
  ```

  后者是patch

#### 2.3.5 浏览器

- Chrome

  ```console
  paru google-chrome
  ```

  如果要跑在wayland下

  ```plaintext
  --ozone-platform-hint=auto
  --enable-wayland-ime
  ```
  {: file='~/.config/chrome-flags.conf'}

  或chrome地址栏里输入`chrome://flags`，开启以下选项

  ![chrome-flags](flags.png)

  ~~目前遇到了Chrome在Wayland下拖入文件后鼠标失效以及右键菜单位置错误的问题~~

- FireFox

  ```console
  paru firefox
  ```

  > 如果遇到中英文混杂的问题，请安装`firefox-i18n-zh-cn`，并将`设置-扩展和主题-语言`中的中文语言包移除，若移除后仍然存在问题，继续移除至无法再移除。
  {: .prompt-info}

#### 2.3.6 工具

- Ark

   压缩和解压缩工具

- OBS

   直播和录制工具

- Gwenview

   图片查看器

- Spectacle

   截图工具

- Okular

   PDF文档查看器

- KDEConnect

- Clash-verge

- Kate

   文本编辑器

- Filelight

- htop

#### 2.3.7 终端使用

- konsole

   新建一个配置方案

   1. 外观

      - 配色方案和字体

         选择`Breeze微风`

         字体选择`JetBrainsMonoNL`

      - 光标

         形状选择`|字型`

         启用`闪烁`

      - 杂项

         边距调整为5像素

         取消选中`调整大小后显示终端大小提示`

   2. 滚动

      滚动条位置选择`隐藏`

      取消选中`高亮显示刚刚进入视图的行`

   3. 鼠标

      - 文本交互

         复制选项全部选中

      - 杂项

         选中文件加下划线

- oh-my-zsh

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

    ```plaintext
    plugins=(git extract zsh-autosuggestions fast-syntax-highlighting)
    ```
    {: file='~/.zshrc'}

- fastfetch

  - 安装`fastfetch`

    ```console
    paru fastfetch
    ```

  - 生成配置文件

    ```console
    fastfetch --gen-config
    ```

  - 编辑`~/.config/fastfetch/config.json`，删除不需要的项

#### 2.3.8 Steam

1. 确保已安装32位显卡驱动

2. 安装steam

   ```console
   paru steam
   ```

3. 若出现缩放问题，请在KDE设置`显示与监视器`选中`由系统进行缩放`

   > 由于该设置与JetBrains系软件冲突，更建议在.desktop文件里添加参数`-forcedesktopscaling 1.5`
   {: .prompt-info}

4. steam设置里需启用参与客户端测试以正常使用输入法

## 3 其他设置  

### 3.1 GRUB美化

我选择Tela主题

1. 下载源文件

   ```console
   git clone https://github.com/vinceliuice/grub2-themes.git
   cd grub2-themes
   ```

2. 执行安装脚本

   ```console
   sudo ./install.sh -b -t tela
   ```

### 3.2 pacman和paru美化

1. 编辑`/etc/pacman.conf`，取消`Color`注释

2. 编辑`/etc/paru.conf`，取消`BottomUp`注释

### 3.3 sudo时显示密码

在`/etc/sudoers`文件中写入`Defaults pwfeedback`

### 3.4 kwallet

如果遇到kwallet请求密码

1. 安装kwalletmanager

   ```console
   paru kwalletmanager
   ```

2. 修改密码时留空即可

### 3.5 部分应用没有阴影

1. 设置里`外观和视觉风格`->`颜色和主题`->`窗口装饰元素`->`编辑Breeze微风主题`->`特定窗口优先规则`，右侧添加，选中`隐藏窗口标题栏`

2. `窗口管理`->`窗口规则`，新增一条，添加`无标题栏和边框`选择`否`

## 4 目前的痛点

- [ ] VSCode、Chrome和Firefox在Wayland下全局菜单失效

- [x] chromium系在Wayland下`drag and drop`失效以及右键菜单位置错误

- [ ] VSCode在Wayland下任务管理器图标异常

- [x] VSCode将`Title Bar Style`修改为`native`后，弹出菜单位置错误

- [x] linuxqq没有音视频通话、屏幕共享功能

- [ ] linuxqq没有远程协助功能

- [ ] linuxqq在KDE下截图失效

- [ ] linuxqq通知提示音失效

- [x] 微信官方没有linux包

- [ ] 微信消息通知没有弹窗

- [ ] 网易云音乐没有linux包

- [x] telegram自动夜间模式失效

- [ ] MS Office无原生linux方案

- [ ] n卡睡眠失效
