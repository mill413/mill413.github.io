---
layout: post
title: 让sddm跑在wayland下
date: 2023-11-23 16:26 +0800
category: [教程, KDE]
tags: [archlinux,sddm,wayland,kde]
media_subpath: "/assets/img/posts/"
---

## 开端

在我将kde全部纳入wayland后发现xorg依然存在于我的电脑里，直到我在群里发现大家讨论sddm跑在wayland下。

于是我决定让我的sddm也跑在wayland下，此举也一并解决了困扰我很久的问题，为什么sddm的缩放没有跟kde走

## 配置

创建文件`/etc/sddm.conf.d/10-wayland.conf`并写入

```text
[General]
DisplayServer=wayland
```

这样就为sddm启用了wayland,但是此时的sddm是用wetson做混成器的，我是kde用户自然不想多装一个wetson

继续写入

```text
GreeterEnvironment=QT_WAYLAND_SHELL_INTEGRATION=layer-shell
[Wayland]
CompositorCommand=kwin_wayland --drm --no-lockscreen --no-global-shortcuts --locale1
```

完成

记得在设置里让sddm应用plasma设置

## 参考

1.[SDDM - ArchWiki](https://wiki.archlinux.org/title/SDDM#KDE_/_KWin)
