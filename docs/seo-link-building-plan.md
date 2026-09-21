# Focusee SEO 外链与权重建设方案

> 产出时间：2026-09-21 | 负责：Robert | 域名：focuseetech.com

## 核心判断

- **技术 SEO 已 A+**：JSON-LD / canonical / OG / sitemap / WebP 全部到位，零死链零重复
- **当前瓶颈**：域名无外链、无收录、无内容深度 → Google 不给权重
- **现实目标**：不追大词"portable air conditioner"（200 万+ 月搜，美的/格力/聚合站把持），专打**品牌/型号长尾词**（"Focusee PCX12R-22MA""Focusee OEM portable air conditioner"）——这些词收录后几乎稳拿第一，询盘质量最高

---

## 第一优先级（本周可做）

### 1. Google Search Console 收录（必须）
- 添加 `https://focuseetech.com/` → 选**HTML 标记**验证
- build.py 第 78 行 `GSC_VERIFY = ''` 留空 → 待 GSC 给 token 后填入，重跑 `python build.py` 即可
- 验证后在「站点地图」提交 `https://focuseetech.com/sitemap.xml`
- Bing Webmaster Tools 同样提交一次（覆盖 Yahoo/DuckDuckGo）
- 7–14 天后在 GSC「索引覆盖率】查看是否抓取成功

### 2. 跨站互链（fcsequip + fcsappliance → focuseetech）
- 两个站同属 Focusee，互链完全合规
- 建议在 fcsequip.com 的导航或 footer 加链接：`Focusee Portable Air Conditioners`
- 建议在 fcsappliance.com 的产品页底部加"相关品牌"区块
- 这是"站内换外链"的高价值低成本动作，1 小时内可完成

---

## 第二优先级（本月可做）

### 3. B2B 目录平台（免费基础版）
| 平台 | 重点关键词 | 是否推荐 |
|------|-----------|---------|
| Alibaba.com | "portable air conditioner OEM""OEM AC manufacturer" | ★ 强烈推荐 |
| Made-in-China.com | "portable AC supplier""OEM cooling" | ★ 推荐 |
| Europages.com | "portable air conditioning Europe""OEM AC EU" | ★★★ 法国市场重点 |
| YellowPages.ca | "portable air conditioner Canada""OEM AC supplier" | 澳新市场 |
| Kompass.com | "air conditioning equipment manufacturer" | 欧洲 B2B |
| GlobalSources.com | "portable air conditioner OEM""private label AC" | 泛亚 |
| ThomasNet.com | "portable air conditioning manufacturer USA" | 北美市场 |

**执行建议**：先上 Alibaba + Made-in-China（流量最大），Europages（法国渠道重点）。每个平台用同一套公司介绍 + 产品 PDF，统一署名 Robert + WhatsApp + 邮箱。

### 4. 内容营销：写 3 篇行业落地页
在 focuseetech.com 新增以下页面（用 `build.py` 机制，纯 HTML）：
- `/applications/tent-camping-ac.html` — 帐篷/房车用移动空调（高搜索意图）
- `/applications/server-room-cooling.html` — 服务器机房降温方案
- `/blog/oem-private-label-guide.html` — OEM 贴牌采购指南（长文，目标 1500+ 字）

**SEO 效果**：这些长尾词竞争极低，内容充实后 Google 容易给首页权重。

---

## 第三优先级（持续进行）

### 5. 客户合作换外链
- 每开发一个客户，要求对方官网挂"供应商"页面并链接到你的产品页
- 话术："We'd love to feature you as a valued partner on our website — can you also add a link to our product page on your supplier page?"
- 这类 B2B 外链权重极高（行业相关性 + .com 域名）

### 6. LinkedIn 公司页 + 帖子引流
- 建公司 LinkedIn 页（Focusee Company Limited）
- 每周发 1 篇产品/行业帖子，带链接到 focuseetech.com
- LinkedIn 帖子容易被 Google 收录，带来第二外链来源

### 7. YouTube 产品视频
- 每个主力型号做 1 分钟短视频（开箱/功能/应用场景）
- 描述区放产品页链接
- YouTube 视频在 Google 视频搜索有独立排名

---

## 时间规划

| 周次 | 任务 | 预期效果 |
|------|------|---------|
| 第 1 周 | GSC 收录 + 跨站互链 | 从 0 收录 → 被 Google 抓取 |
| 第 2–3 周 | Alibaba + Made-in-China 上架 | 外部外链 +2 |
| 第 4 周 | 3 篇行业落地页上线 | 长尾词开始有排名 |
| 第 2 月 | LinkedIn + YouTube 启动 | 外链持续积累 |
| 第 3 月 | 评估 GSC 数据，调整关键词 | 复盘 + 迭代 |

---

## 预期结果

- **3 个月内**：品牌词"Focusee portable air conditioner"进入前 3
- **6 个月内**：型号词（如"PCX12R-22MA"）稳定在首页
- **12 个月内**：部分长尾词（"OEM portable air conditioner China""camping AC ductless"）进入前 10

---

## 不做什么

- 不买外链（Fiverr/SEO 黑帽）——Google 算法会惩罚
- 不做友情链接群发——低质量外链反而有害
- 不追大词排名——B2B 询盘不需要"portable air conditioner"首页，型号词足矣
