# Focusee Company Limited — Portable Air Comfort Website

静态站（纯 HTML/CSS/JS，无依赖），内容参考 unitedgreenac.com 的产品线重建，品牌为 FOCUSEE。

## 结构

```
focusee-ac/
├── index.html            首页
├── products.html         产品总览（53 个型号，3 大分类，可筛选）
├── about.html            关于我们 / 可持续发展
├── contact.html          联系我们（Carol Luo / Robert Luo）
├── product-<型号>.html   53 个产品详情页（规格表 + 功能表 + 图库）
├── assets/
│   ├── css/style.css     全站样式（含响应式）
│   ├── js/site.js        移动菜单、分类筛选、产品图切换
│   ├── img/              产品图 + LOGO
│   └── products.json     产品数据（供二次开发/搜索用）
├── data/products.json    生成器的源数据
└── build.py              站点生成器（改数据后重新跑即可）
```

## 关键信息

- 公司名：Focusee Company Limited
- 地址：Factory House B, Changmingshui Industrial Park, Changyi Road, Wuguishan, Zhongshan City, Guangdong Province, China 528458
- Carol Luo — General Manager — carol.luo@focuseetech.com — WhatsApp +86 133 7848 2598
- Robert Luo — Marketing Manager — Marketing@focuseetech.com — WhatsApp +86 134 2565 1968

## 内容修改

改文案直接编辑对应 HTML；批量改（新增型号、改联系方式）用生成器：

```bash
# 编辑 data/products.json 后
python build.py
```

`build.py` 会重新生成全部 57 个页面。联系方式、公司名、地址集中在 build.py 顶部的 `COMPANY` / `ADDRESS` / `PEOPLE` 常量里。

## 部署

**线上地址：https://q522658267-pixel.github.io/focusee-ac/**
仓库：https://github.com/q522658267-pixel/focusee-ac

已部署到 GitHub Pages（main 分支根目录）。更新流程：

```bash
cd focusee-ac
python build.py          # 如改了 data/products.json 或 build.py
git add -A
git commit -m "update"
git push                 # 推完约 1 分钟自动重新发布
```

本地预览：

```bash
python -m http.server 8899
# 打开 http://127.0.0.1:8899/index.html
```

> 注意：本机 `HOME` 是 POSIX 风格路径，gh CLI 写配置会失败。用 gh 命令时前面加 `HOME='C:\Users\ASUS'`。

## 备注

- 产品图片来自参考站点，均为干净的产品棚拍图，无第三方品牌水印。
- 原站的品牌文案（GREEN MASTER / Zhongshan Lianchang / 原邮箱）已全部剔除并改写为 FOCUSEE 口径。
- 认证表述（CE/GS、Energy Star options、MEPS ready、RoHS）沿用参考站的原口径，正式对外发布前建议由业务确认当前有效状态。
