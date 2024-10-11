---
layout: post
title: 利用Pacman Hooks解决WPS无法使用输入法的问题
date: 2024-10-11 16:45 +0800
category: [教程, Archlinux]
tags: [pacman, hooks, wps, fcitx]
img_path: "/assets/img/posts/"
---

AUR里的WPS更新到12.1后fcitx输入法无法正常使用，参考[这篇博客](https://wszqkzqk.github.io/2024/03/09/WPS-Fcitx5/)，评论区有人提到可以使用Pacman Hooks自动化patch，但是他给出的命令有一点小问题，sed会找不到.desktop文件，初步排查后猜测原因可能是执行时文件还未生成，于是加上了2秒的延迟

```text
[Trigger]
Operation = Upgrade
Operation = Install
Type = Package
Target = wps-office-cn
[Action]
Description = Fix fcitx not working in WPS
When = PostTransaction
Exec = /bin/sh -c 'sleep 2; /usr/bin/sed -i -E -e "s/Exec ?= ?/Exec=env XMODIFIERS=\"@im=fcitx\" GTK_IM_MODULE=\"fcitx\" QT_IM_MODULE=\"fcitx\" SDL_IM_MODULE=fcitx /g" /usr/share/applications/wps-office*.desktop'
```
{: file="/etc/pacman.d/hooks/fcitx-patch-for-wps.hook"}
