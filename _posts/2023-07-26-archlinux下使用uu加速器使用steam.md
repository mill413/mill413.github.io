---
layout: post
title: ArchLinux下UU加速器使用Steam
date: 2023-07-26 11:11 +0800
categories: [教程]
tags: [archlinux, uu加速器]
---

## 0 下载Steam

```shell
yay -S steam
```

## 1 下载UU加速器插件

```shell
curl -s uudeck.com | sudo sh
```

出现`Installation succeeded!`即为安装成功

## 2 绑定设备

1. 手机与电脑连接至同一WiFi下

2. 打开UU加速器主机版App，选择`用硬件加速`-`安装Steam Deck插件`

3. 等待搜索设备成功后绑定即可

4. 绑定成功后即可加速steam游戏

## 3 Trouble Shooting

1. 搜索不到设备
    检查防火墙设置，或直接禁用防火墙

## 参考

[Steam Deck插件安装步骤 Q&A](https://router.uu.163.com/app/html/online/baike_share.html?baike_id=63ec9d92b2d9f77dc9a8dde6)