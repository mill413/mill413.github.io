---
layout: post
title: Day29 - Baseline在VsiDrone上的表现
date: 2024-03-11 23:33 +0800
category: [读研日记]
tags: []
media_subpath: "/assets/img/posts/"
---

以yolov5n/s/m和yolov8n/s作为baseline,在VisDrone2019上训练200epochs

- Yolov5n

    Parameters: 2.655M

    |                 Class|   Precision|      Recall|       mAP50|    mAP50-95|
    |---:                  |---:        |---:        |---:        |---:        |
    |                   all|       0.432|       0.318|        0.32|       0.184|
    |            pedestrian|       0.452|       0.336|       0.343|       0.146|
    |                people|       0.513|       0.218|       0.268|      0.0968|
    |               bicycle|       0.231|      0.0831|      0.0771|      0.0281|
    |                   car|       0.644|       0.743|       0.753|       0.515|
    |                   van|       0.471|       0.374|       0.382|       0.262|
    |                 truck|       0.418|       0.273|       0.267|        0.17|
    |              tricycle|       0.363|       0.211|       0.201|        0.11|
    |       awning-tricycle|       0.237|       0.143|       0.114|       0.072|
    |                   bus|       0.541|       0.422|       0.436|       0.289|
    |                 motor|       0.451|       0.378|       0.358|       0.149|

- Yolov5s

    Parameters: 9.153M

    |                 Class|   Precision|      Recall|       mAP50|    mAP50-95|
    |---:                  |---:        |---:        |---:        |---:        |
    |                   all|       0.492|        0.37|       0.382|       0.228|
    |            pedestrian|       0.511|       0.385|       0.411|       0.187|
    |                people|       0.539|       0.262|       0.316|       0.121|
    |               bicycle|       0.278|       0.149|       0.118|      0.0468|
    |                   car|       0.711|       0.769|        0.79|       0.561|
    |                   van|       0.519|       0.421|        0.44|       0.307|
    |                 truck|        0.52|       0.362|       0.367|       0.239|
    |              tricycle|       0.406|       0.279|       0.271|       0.148|
    |       awning-tricycle|       0.308|       0.165|       0.155|      0.0996|
    |                   bus|       0.622|        0.47|       0.522|       0.386|
    |                 motor|       0.512|       0.438|       0.433|       0.188|

- Yolov5m

    Parameters: 25.111M

    |                 Class|   Precision|      Recall|       mAP50|    mAP50-95|
    |---:                  |---:        |---:        |---:        |---:        |
    |                   all|       0.517|       0.405|       0.414|       0.251|
    |            pedestrian|       0.546|       0.398|       0.433|       0.203|
    |                people|       0.576|       0.289|       0.345|       0.135|
    |               bicycle|       0.278|       0.183|       0.149|      0.0622|
    |                   car|       0.757|       0.775|       0.806|       0.584|
    |                   van|       0.546|       0.468|       0.479|       0.338|
    |                 truck|       0.509|       0.411|       0.407|       0.267|
    |              tricycle|       0.412|       0.331|       0.303|       0.167|
    |       awning-tricycle|       0.312|        0.19|       0.169|       0.108|
    |                   bus|       0.702|       0.546|       0.587|       0.435|
    |                 motor|        0.53|       0.459|       0.464|        0.21|

- Yolov8n

    Parameters: 3.157M

    |                 Class|   Precision|      Recall|       mAP50|    mAP50-95|
    |---:                  |---:        |---:        |---:        |---:        |
    |                   all|       0.439|        0.33|       0.325|       0.187|
    |            pedestrian|       0.444|       0.335|       0.341|       0.145|
    |                people|       0.511|       0.232|       0.278|      0.0981|
    |               bicycle|       0.196|       0.117|      0.0834|      0.0314|
    |                   car|       0.659|       0.742|       0.755|        0.52|
    |                   van|       0.469|        0.39|       0.376|        0.26|
    |                 truck|       0.446|       0.297|       0.285|       0.177|
    |              tricycle|       0.364|       0.249|       0.212|       0.114|
    |       awning-tricycle|       0.237|       0.148|       0.117|      0.0733|
    |                   bus|       0.581|       0.418|       0.443|       0.301|
    |                 motor|       0.484|       0.367|       0.365|       0.151|

- Yolov8s

    Parameters: 11.167M

    |                 Class|   Precision|      Recall|       mAP50|    mAP50-95|
    |---:                  |---:        |---:        |---:        |---:        |
    |                   all|         0.5|        0.38|       0.385|        0.23|
    |            pedestrian|       0.541|        0.38|       0.415|       0.188|
    |                people|       0.565|       0.269|       0.321|       0.122|
    |               bicycle|       0.247|       0.174|       0.124|      0.0504|
    |                   car|        0.73|       0.765|       0.791|       0.565|
    |                   van|       0.519|       0.434|       0.442|       0.314|
    |                 truck|        0.51|       0.341|        0.36|       0.239|
    |              tricycle|       0.385|       0.307|       0.257|       0.142|
    |       awning-tricycle|       0.324|       0.188|       0.157|      0.0969|
    |                   bus|       0.677|       0.498|       0.542|       0.388|
    |                 motor|       0.503|       0.445|       0.439|       0.194|
