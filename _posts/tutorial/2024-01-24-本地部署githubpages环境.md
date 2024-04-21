---
layout: post
title: 本地部署GithubPages环境
date: 2024-01-24 17:19 +0800
category: [教程]
tags: [jekyll,githubpage]
media_subpath: "/assets/img/posts/"
---

重装系统后，往往也需要重新安装各种环境，在此记录一下Github Page的本地搭建环境

其实也就是安装ruby和jekyll

1. 安装ruby

    根据操作系统选择安装ruby的方式，[官网](https://jekyllrb.com/docs/installation/other-linux/)有很详细的说明

    以Arch为例

    ```shell
    sudo pacman -S ruby base-devel
    ```

2. 安装jekyll

    ```shell
    echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
    echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
    echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    注意`bashrc`替换为正在使用的shell对应的文件，比如我正在用的zsh,对应`zshrc`

3. 安装bundler

    ```shell
    gem install jekyll bundler
    ```

4. 将Github上的仓库clone下来，进入目录后，安装依赖

    ```shell
    bundle install
    ```

    如果报了```Bundler::PermissionError: There was an error while trying to write to`/usr/lib/ruby/gems/3.0.0/cache`. It is likely that you need to grant write permissions for that path.```这样的错，需要修改目录所有者

    ```shell
    sudo chown -R $whoami /usr/lib/ruby/gems
    ```

    重新安装依赖即可
