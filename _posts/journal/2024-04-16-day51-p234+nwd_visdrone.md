---
layout: post
title: Day51 - P234+NWD改进在VisDrone上的表现
date: 2024-04-16 23:18 +0800
category: [读研日记]
tags: []
media_subpath: "/assets/img/posts/"
---

yolov5s/m和yolov8s删除P5检测头+添加P2检测头,使用NWD损失函数,在VisDrone上训练200epochs

- Yolov5s-p234-nwd

    Parameters: 6.273M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|     0.538|     0.414|     0.434|     0.257|
    |           pedestrian|     0.584|     0.472|     0.511|      0.24|
    |               people|     0.588|     0.366|     0.412|     0.167|
    |              bicycle|     0.308|     0.193|      0.17|    0.0737|
    |                  car|     0.728|     0.816|     0.834|     0.592|
    |                  van|     0.551|     0.462|     0.472|     0.334|
    |                truck|     0.502|     0.336|     0.362|     0.236|
    |             tricycle|     0.478|     0.316|     0.314|     0.173|
    |      awning-tricycle|     0.335|      0.18|     0.165|     0.105|
    |                  bus|     0.732|     0.499|     0.583|     0.413|
    |                motor|      0.57|       0.5|     0.514|     0.236|

- Yolov5m-p234-nwd

    Parameters: 17.162M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|     0.564|     0.445|     0.466|     0.282|
    |           pedestrian|     0.633|     0.493|     0.551|     0.265|
    |               people|       0.6|     0.399|     0.436|      0.18|
    |              bicycle|     0.326|      0.23|     0.204|    0.0933|
    |                  car|     0.768|     0.821|     0.843|      0.61|
    |                  van|     0.569|     0.476|     0.495|     0.353|
    |                truck|      0.59|      0.38|     0.412|     0.272|
    |             tricycle|     0.483|     0.355|     0.341|     0.192|
    |      awning-tricycle|     0.351|     0.201|      0.18|     0.111|
    |                  bus|     0.716|      0.57|     0.649|     0.482|
    |                motor|     0.603|     0.527|     0.544|     0.259|

- Yolov8s-p234-nwd

    Parameters: 7.781M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|     0.525|     0.425|     0.438|     0.261|
    |           pedestrian|      0.58|     0.478|     0.519|     0.246|
    |               people|     0.569|     0.373|     0.413|     0.169|
    |              bicycle|     0.296|     0.207|     0.178|    0.0786|
    |                  car|     0.738|     0.819|     0.837|     0.598|
    |                  van|     0.548|     0.466|      0.48|      0.34|
    |                truck|     0.519|     0.343|     0.361|      0.23|
    |             tricycle|     0.423|     0.303|     0.298|     0.166|
    |      awning-tricycle|     0.326|     0.186|     0.168|     0.109|
    |                  bus|     0.691|     0.543|     0.597|     0.431|
    |                motor|     0.559|     0.529|     0.525|     0.242|
