# Google Search Console 验证步骤

## 方法 A：HTML 标记验证（推荐）

1. 打开 https://search.google.com/search-console
2. 点「新增资源」→ 选「网址前缀」→ 输入 `https://focuseetech.com/`
3. 选择「HTML 标记」验证
4. GSC 会给你一个类似 `googlexxxxxxxxxxxx.html` 的文件名 + 一个 token
5. **把 token 填入 `../build.py` 第 78 行**：
   ```python
   GSC_VERIFY = 'googlexxxxxxxxxxxx'  # 去掉 google 前缀，只留 token
   ```
6. 在根目录创建验证文件：
   ```bash
   echo '<html><head><meta name="google-site-verification" content="YOUR_TOKEN"></head><body></body></html>' > googleXXX.html
   ```
7. 重新提交 sitemap：GSC → 站点地图 → 输入 `sitemap.xml` → 提交
8. 等 24–48 小时看「索引覆盖率」

## 方法 B：DNS TXT 记录验证（更稳）

1. 选「DNS 记录」验证
2. 复制 GSC 给的 TXT 记录值
3. 去你的域名注册商（如 Cloudflare/Namecheap）添加 TXT 记录
4. 验证通过后 GSC 会显示「验证成功」

## 验证通过后

- GSC → 站点地图 → 提交 `https://focuseetech.com/sitemap.xml`
- 同时提交到 Bing Webmaster Tools：https://www.bing.com/webmasters
- 7–14 天后检查「页面索引】报告

## 注意事项

- GSC 验证文件（googleXXX.html）只需保留 30 天，验证通过后**建议删除**避免泄露
- `build.py` 的 `GSC_VERIFY` 留空即可，不影响其他功能
- 如果换了验证方法，记得清掉 `GSC_VERIFY` 的值重新 build
