---
layout: post
title: archlinux上使用虚拟机
date: 2024-03-14 19:59 +0800
category: [教程]
tags: [qemu, virt-manager, archlinux, kvm]
media_subpath: "/assets/img/posts/"
---

1. 确保bios支持并已开启虚拟化

2. 确保内核支持并开启KVM

3. 安装qemu及virt-manager

    ```console
    paru qemu-full
    paru virt-manager
    ```

4. 将自己加入libvirtd组

    ```console
    sudo usermod -a -G libvirt $USER
    ```

5. 启动libvirtd服务

    ```console
    systemctl enable --now libvirtd
    ```

6. 开启虚拟网络

    ```console
    sudo virsh net-autostart default
    ```
