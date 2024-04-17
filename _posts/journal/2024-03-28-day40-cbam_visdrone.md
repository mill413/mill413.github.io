---
layout: post
title: Day40 - Backbone中C3/C2f后添加一层CBAM在VisDrone上的表现
date: 2024-03-28 15:42 +0800
category: [读研日记]
tags: []
img_path: "/assets/img/posts/"
---

yolov5n/s/m和yolov8n/s仅在backbone的C3/C2f模块后添加一层CBAM,在VisDrone2019上训练200epochs

- Yolov5n-cbam

    Parameters: 2.742M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|     0.422|     0.326|     0.321|     0.183|
    |           pedestrian|      0.41|     0.358|     0.343|     0.147|
    |               people|     0.504|     0.234|     0.276|    0.0985|
    |              bicycle|     0.195|    0.0995|    0.0705|    0.0266|
    |                  car|     0.638|     0.747|     0.754|     0.515|
    |                  van|     0.438|     0.371|      0.37|     0.253|
    |                truck|     0.418|     0.281|      0.27|     0.172|
    |             tricycle|     0.391|      0.23|     0.208|     0.111|
    |      awning-tricycle|     0.244|     0.141|     0.105|    0.0669|
    |                  bus|     0.507|     0.434|     0.452|     0.294|
    |                motor|     0.474|     0.362|      0.36|     0.149|

- Yolov5s-cbam

    Parameters: 9.502M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|     0.492|     0.373|     0.378|     0.224|
    |           pedestrian|      0.53|     0.376|     0.408|     0.182|
    |               people|     0.556|     0.253|     0.317|     0.121|
    |              bicycle|     0.269|     0.176|     0.129|     0.053|
    |                  car|     0.721|     0.765|     0.791|     0.561|
    |                  van|     0.529|     0.425|     0.438|     0.306|
    |                truck|     0.482|     0.332|     0.338|     0.216|
    |             tricycle|      0.41|     0.291|     0.268|     0.147|
    |      awning-tricycle|     0.309|      0.18|     0.152|    0.0983|
    |                  bus|     0.589|      0.51|      0.51|     0.363|
    |                motor|      0.52|     0.424|     0.428|     0.188|

- Yolov5m-cbam

    Parameters: 25.896M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|     0.535|     0.401|     0.419|     0.254|
    |           pedestrian|     0.572|     0.395|      0.44|     0.208|
    |               people|      0.59|      0.29|     0.346|     0.137|
    |              bicycle|     0.285|     0.185|      0.15|     0.063|
    |                  car|      0.76|     0.775|     0.807|     0.587|
    |                  van|     0.555|     0.457|     0.481|      0.34|
    |                truck|     0.568|     0.389|      0.41|     0.271|
    |             tricycle|     0.432|     0.316|     0.304|     0.171|
    |      awning-tricycle|     0.322|     0.199|     0.179|      0.11|
    |                  bus|     0.726|     0.534|     0.603|     0.442|
    |                motor|     0.544|     0.466|     0.468|     0.214|

- Yolov8n-cbam

    Parameters: 3.245M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|      0.45|     0.327|     0.328|      0.19|
    |           pedestrian|     0.459|     0.329|      0.34|     0.147|
    |               people|     0.518|     0.224|      0.27|    0.0979|
    |              bicycle|      0.21|     0.105|    0.0753|    0.0288|
    |                  car|     0.674|     0.736|     0.754|      0.52|
    |                  van|     0.488|     0.382|     0.385|     0.265|
    |                truck|     0.477|     0.301|     0.295|     0.187|
    |             tricycle|     0.387|     0.238|       0.2|     0.108|
    |      awning-tricycle|     0.243|     0.145|      0.13|    0.0809|
    |                  bus|     0.547|      0.45|     0.473|     0.314|
    |                motor|     0.497|     0.356|     0.363|     0.153|

- Yolov8s-cbam

    Parameters: 11.516M

    |                Class| Precision|    Recall|     mAP50|  mAP50-95|
    |                 ---:|      ---:|      ---:|      ---:|      ---:|
    |                  all|     0.507|     0.373|     0.387|      0.23|
    |           pedestrian|      0.55|     0.374|     0.412|     0.187|
    |               people|     0.573|      0.27|     0.328|     0.127|
    |              bicycle|     0.256|     0.143|     0.115|    0.0485|
    |                  car|      0.74|     0.759|     0.791|     0.566|
    |                  van|     0.527|     0.433|     0.443|     0.313|
    |                truck|     0.492|      0.35|     0.361|     0.236|
    |             tricycle|     0.414|       0.3|      0.28|     0.152|
    |      awning-tricycle|     0.309|      0.18|     0.155|    0.0959|
    |                  bus|     0.682|     0.494|     0.545|      0.38|
    |                motor|     0.529|     0.431|     0.434|     0.192|