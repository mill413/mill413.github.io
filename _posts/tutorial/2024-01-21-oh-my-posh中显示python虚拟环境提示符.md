---
layout: post
title: Oh-My-Posh中显示Python虚拟环境提示符
date: 2024-01-21 18:53 +0800
category: [教程]
tags: [ohmyposh]
img_path: "/assets/img/posts/"
render_with_liquid: false
---

我的ohmyposh主题一直用的robbyrussell主题，但是他在python的虚拟环境中无法显示虚拟环境提示符，原因是他压根没写python的segment，我就自己写了一个加进去

```json
{
          "type": "python",
          "style": "plain",
          "properties": {
            "display_mode": "environment",
            "fetch_virtual_env": true,
            "home_enabled": true
          },
          "foreground": "#ffffff",
          "template": "({{ if .Error }}{{ .Error }}{{ else }}{{ if .Venv }}{{ .Venv }}{{ end }}{{ end }}) "
}
```
