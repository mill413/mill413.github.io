---
layout: post
title: Archlinux+KDE美化记录
date: 2023-10-03 21:47 +0800
category: [记录,Archlinux]
tags: [archlinux,美化,kde,wayland]
img_path: /assets/img/posts/231003/
image: 
    path: preview.png
    alt: 美化后的桌面，点击查看大图
---

很简单的美化，做一个流水账式的记录

## 外观

### 主题

在`设置`-`外观`-`全局主题`中选择`Breeze微风`即可，应用后其他所有相关设置都会变成微风主题，接下来再对一些项目做单独设置

![主题](1.png)
_全局主题选择_

### 颜色

在`颜色`中，选择一个自己喜欢的颜色，并在底下选择一个喜欢的`配色方案`

![颜色选择](2.png)
_颜色选择_

### 图标

`图标`是一个很重要的美化元素，在右下角`获取新图标`中搜索并下载`Tela`

![图标](3.png)
_图标_

### 欢迎屏幕

`欢迎屏幕`是个见仁见智的东西，最开始我并不会设置它，现在我选择`Arch`用来开机后的过渡，`获取新欢迎屏幕`在右上角

![欢迎屏幕](4.png)
_欢迎屏幕_

### 登录屏幕（SDDM）

在`设置-开机与关机-登录屏幕（SDDM）`中选择`Breeze微风`，并点击右下角的`应用Plasma设置`

![登录屏幕](5.png)
_登录屏幕_

编辑`/usr/lib/systemd/system/sddm.service`文件

在`[Service]`块下添加一行

```text
Environment=LANG=zh_CN.UTF-8  
```

然后重启即可

### 桌面特效

个人不大喜欢花里胡哨的特效，仅仅设置了`最小化过渡动画（神灯）`，以及关掉了`气泡显隐渐变动画`，因为fcitx5在一些应用中会闪屏

桌面特效相关设置在`工作区行为-桌面特效`中

### 锁屏

锁屏并没有太多需要设置的，仅仅设置了锁屏的外观，具体设置如图所示

![锁屏外观](6.png)
_锁屏外观_

### 面板

我在桌面上添加了两个面板，最底下的面板用以放置`应用程序启动器`以及`图标任务管理器`挂件，充当类似Dock栏的功能

![底部面板](9.png)
_底部面板_

而顶部面板分别添加`全局菜单`、`Window Title`、`Window Buttons`、`系统托盘`、`数字时钟`、`通知`挂件

![顶部面板](10.png)
_顶部面板_

以上两个面板均设置为`居中`、`自动隐藏`、`半透明`、`浮动面板`，但是貌似透明度设置在微风主题下失效

### 壁纸

设置好以上的配置项后，选择一个好看的壁纸就大功告成了，如果你是多屏用户，KDE提供了为不同屏幕设置不同壁纸的特性（薄纱Windows

在桌面右键，进入壁纸设置

![壁纸](11.png)
_壁纸_

## 系统设置

### 24小时

QT的默认区域设置中，中国大陆的时间格式为12小时，可下载24小时制补丁包

```zsh
paru qt5-base-24hms
```

### kwin脚本

在`窗口管理-KWin脚本`中，点击右下角`获取新脚本`，搜索并下载`Hide Titles`，此脚本可在窗口最大化后隐藏标题栏，配合`全局菜单`挂件使用体验更佳

### 任务切换器

在`任务切换器`中设置`可视化`，选择`缩略图网格`

![任务切换器](7.png)
_任务切换器_

### 活动

在`工作区行为-活动`中，设置`Default`活动的图标与名称，配合`Window Title`挂件使用

![活动](8.png)
_活动_

## 其他美化

### 终端

![终端](12.png)
_终端_

首先把工具栏去除，再进行下一步

#### 配置方案

1. 将`黑底绿字`中的`背景色透明度`设置为`50%`，且开启`模糊背景`即可

2. 字体选择`JetBrains Mono NL ExtraBold`，字号设置为`10`

3. `滚动条位置`设置为`隐藏`

#### shell美化

1. 安装`oh-my-zsh`

    ```zsh
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```

    仅使用默认主题

2. 安装插件

    个人最常用的就是`zsh-autosuggestions`和`zsh-syntax-highlighting`插件

    ```zsh
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    ```

    安装完成后编辑`~/.zshrc`文件，在`plugins`配置项里写入以上两个插件的名字，我还启用了`extract`插件，在解压缩时只需要使用`x`命令即可，无需根据压缩格式选择不同的命令

    ```text
    plugins=(git zsh-syntax-highlighting zsh-autosuggestions extract)
    ```

### GRUB

我选择Tela主题

1. 下载源文件

    ```zsh
    git clone https://github.com/vinceliuice/grub2-themes.git
    ```

2. 执行安装脚本

    ```zsh
    sudo ./install.sh -b -t tela
    ```

### pacman

1. 编辑`/etc/pacman.conf`，取消`Color`注释

2. 编辑`/etc/paru.conf`，取消`BottomUp`注释
