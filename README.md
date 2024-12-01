## SubTurn-Bot
---
- 一个订阅转换 telegram bot，把订阅连接转换成 clash meta 格式
- 你也可以自己修改配置文件 `config.yaml` 预设想要的分流规则
- 自建 `bot` 修改 `token.txt` 中的 `BOT_TOKEN`
- 运行 `bot：` `python bot.py`
- 在 `docker` 中使用，执行命令：
- /dockerapp/SubTurn-Bot 可自行替换成想映射的本地目录

`git clone https://github.com/sskaykat/SubTurn-Bot.git`

`cd SubTurn-Bot`

```
docker run -d \
  --name sub2clashbot \
  -v /dockerapp/SubTurn-Bot:/sub2clashbot \
  taohuajiu/sub2clash:latest
```

- 使用 `docker-compose` 部署，创建 `docker-compose.yaml`文件(如下)
- 运行 `docker-compose up -d`

```
version: '3'
services:
  onebot:
    image: taohuajiu/sub2clash:latest
    container_name: sub2clashbot
    volumes:
      - /dockerapp/SubTurn-Bot:/sub2clashbot
```

- 默认规则预览：
- 配置文件中 `Warp` 用来实现链式代理

<div style="display: flex; justify-content: space-between;">
  <img src="https://bed.ssmao.eu.org/file/1733044171403_clash-verge_HfWDXWWf10.png" alt="图片1" style="width: 45%;"/>
  <img src="https://bed.ssmao.eu.org/file/1733044175814_clash-verge_o9mLT8YgWR.png" alt="图片2" style="width: 45%;"/>
</div>




