---
layout: post
title: 同步Fork的Github仓库
date: 2024-01-02 21:49 +0800
category: [教程,Git]
tags: []
media_subpath: "/assets/img/posts/"
---

最近发现`Github Pages`的`sync fork`老是提示冲突，每次要合并都得手动处理，记录一下这几个命令

首先在终端里`cd`到本地仓库

获取上游仓库的commit

```shell
git fetch upstream
```

签出本地默认分支

```shell
git checkout master
```

合并上游的更改

```shell
git merge upstream/master
```

一般这个时候会提示文件冲突，手动解决冲突后再次运行一遍合并即可
