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

**线上地址：https://focuseetech.com/**（www 也可访问）
备用地址：https://q522658267-pixel.github.io/focusee-ac/（会自动 301 跳到主域名）
仓库：https://github.com/q522658267-pixel/focusee-ac

托管：**GitHub Pages**（main 分支根目录），自定义域名 focuseetech.com，HTTPS 已开启（证书有效期至 2026-12-19，到期前 GitHub 会自动续）。

DNS（在域名商处配置，保持不变即可）：

| 类型 | 主机记录 | 记录值 |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | q522658267-pixel.github.io |

仓库根目录有 `CNAME` 文件（内容 `focuseetech.com`），**不要删除**，删了域名会解绑。

更新流程：

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

## SEO

全站已做的技术 SEO（改 build.py 后自动重新生成，无需手工维护）：

| 项目 | 说明 |
|---|---|
| canonical | 每页唯一绝对地址，指向 `https://focuseetech.com/...`，自动消 www / github.io 的重复内容 |
| title / description | 每页独立，产品页自动带型号 + 品类 + 关键规格；不含 HTML 实体泄漏 |
| Open Graph / Twitter Card | `og:title/description/url/image/type`，分享卡片用 `assets/img/og-cover.jpg`（1200×630，产品页自动换该产品主图） |
| 结构化数据 | 首页 `Organization` + `WebSite` + `FAQPage`；products `ItemList`；52+ 产品页 `Product`（含 sku/品牌/类目/图片/供货范围）；全站 `BreadcrumbList`；contact `ContactPage` |
| robots | `index,follow,max-image-preview:large` |
| sitemap.xml | 57 条 URL，带 priority 与 changefreq，`build.py` 每次重新生成 |
| robots.txt | 放行全站并声明 sitemap |
| 404.html | GitHub Pages 会自动用根目录 404.html 作为自定义错误页 |
| 语义化 | 每页唯一 `h1`，面包屑用真实链接（非 JS），产品页有 prev/next 与相关型号内链 |
| 图片 | `alt` 为「型号 + 品类 + 视角」自然描述；全部带 `width/height` 防布局抖动；首屏图 `fetchpriority="high"`，其余 `loading="lazy"` |
| 速度 | 191 张图全部自动转 WebP（30MB → 3.6MB，省 88%），HTML 用 `<picture>` 保留原图回退，老浏览器不受影响 |

**待办（需要人工操作，需账号权限）**

1. Google Search Console 验证 `focuseetech.com` → 提交 `https://focuseetech.com/sitemap.xml`
2. Bing Webmaster Tools 同样提交一次
3. 建议给 www 也做 301 到主域（GitHub Pages 不会自动跳），可选

## 备注

- 产品图片来自参考站点，均为干净的产品棚拍图，无第三方品牌水印。
- 原站的品牌文案（GREEN MASTER / Zhongshan Lianchang / 原邮箱）已全部剔除并改写为 FOCUSEE 口径。
- 认证表述（CE/GS、Energy Star options、MEPS ready、RoHS）沿用参考站的原口径，正式对外发布前建议由业务确认当前有效状态。
