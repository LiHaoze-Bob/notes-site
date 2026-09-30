# Steam 卡片实时接口

网站继续托管在 GitHub Pages；此 Worker 只为 Steam 卡片提供 JSON，不迁移网站。固定查询 `76561199304157766`，不接受其他 ID 或上游地址。

## 在 Cloudflare 控制台部署

1. 创建一个名为 `notes-site-steam` 的 Worker，选择 Hello World 起步。
2. 在代码编辑器中，用本目录的 `worker.mjs` 全文替换默认代码，部署。
3. 在 Worker 的 **Settings → Variables and Secrets** 新增 **Secret**，名称为 `STEAM_API_KEY`，值填入你的 [Steam Web API Key](https://steamcommunity.com/dev/apikey)。保存并部署。不要把 Key 写入源码、GitHub 变量或聊天。
4. 默认允许网站域名 `https://lihaoze-bob.github.io`。如需本地浏览器联调，添加 Text 变量 `ALLOWED_ORIGINS`，值为 `https://lihaoze-bob.github.io,http://127.0.0.1:8765`。本地验证后可恢复正式域名。
5. 打开 `https://notes-site-steam.<你的子域名>.workers.dev/steam`，确认返回 JSON；没有 Key 时返回 503，Steam 故障时返回 502。根路径 `/` 返回 404 是正常的。
6. 将完整的 `/steam` 地址填入 `site-template/_data/steam-live.json` 的 `endpoint`，构建并发布网站。留空时保持发布快照，不发起请求。

已有 Wrangler CLI 时，也可以在本目录运行 `wrangler deploy`，再用 `wrangler secret put STEAM_API_KEY` 交互输入 Key。CLI 会读取相邻的 `wrangler.toml`，无需数据库、KV 或定时任务。

## 更新与回退

- 页面可见时，首次打开立即查询，此后每 60 秒查询；后台标签页暂停，回到前台立即查询。
- 状态缓存 30 秒，资料缓存 1 小时，缓存按 Cloudflare 数据中心隔离；没有访客时不会主动查询 Steam。60 秒是查询间隔，不是端到端延迟保证。
- 状态与资料分别显示原始采集时间。资料请求失败不会阻断在线状态刷新；请求超时或失败时保留上次数据显示时间，不伪造成功时间。
- 主页转为非公开时，状态显示未公开，清除卡片中的游戏、徽章等旧资料及后端资料缓存。游戏详情的可见性遵循 Steam API 对所用 Key 的返回结果。
- 近两周时长累加 API 返回的全部游戏，再选前三款展示；不作为全库总时长。游戏数采用 API 的拥有游戏计数（包括玩过的免费游戏），可能与社区主页展示口径不同。
- `STEAM_API_KEY` 仅用于后端请求 Steam；响应与缓存只包含卡片需要的字段。CORS 限制浏览器来源，不作为鉴权或全局限流。此接口只用于展示自己的资料。
- 页面未启用 JavaScript、接口未配置或不可用时，仍有 `scripts/steam.py` 在发布时生成的静态卡片。

## 验证

在仓库根目录运行 `node --test tests/steam-worker.test.mjs` 和 `.venv/bin/python -m pytest tests/test_steam.py`。上线后验证 `/steam` 的状态码、CORS、原始时间戳，以及 About 页在更新失败时保留旧时间的行为。

接口依据：[Steam 玩家状态](https://partner.steamgames.com/doc/webapi/ISteamUser)、[Steam 玩家资料](https://partner.steamgames.com/doc/webapi/IPlayerService)、[Cloudflare Cache API](https://developers.cloudflare.com/workers/runtime-apis/cache/)、[Cloudflare Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)。
