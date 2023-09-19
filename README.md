# FSB (封神榜) Discord Bot

## 简介

FSB (封神榜) 是一个Discord机器人，旨在为Discord用户提供一个发泄平台。这个榜单型软件允许用户记录他们在生活或游戏中遇到的不喜欢的人，包括他们的游戏ID、行为和个人评价。


## 功能

### 帮助指令

- 使用 `/help` 指令可以查看所有可用的机器人指令。

### 所有指令内容

- 指令介绍与对应指令
  - 查看列表：`/list`
  - 按创建日期查看列表：`/list d`
  - 按详细信息数量查看列表：`/list n`
  - 查看详细信息：`/detail ID`
  - 录入简易信息：`/new_player ID 简略信息`
  - 录入详细信息：`/add_comment ID 详细信息`
  - 开始抓内鬼游戏：`/new_game 内鬼数量`
  - 加入队伍：`/join game_code blue/red`
  - 查看游戏信息：`/game_info game_code`
  - 安排内鬼：`/game_start game_code`
  - 消息接收测试：`/msg_test game_code`

### 抓内鬼游戏

- 使用 `/new_game num` 指令可以创建一个新的有num个内鬼的游戏。
- 在创建游戏后，用户可以使用 `/join gamecode side` 指令加入游戏。
- 为了确保通知能正常接收，建议在游戏开始前使用 `/msg_test gamecode` 来进行测试
- 游戏开始后，程序会随机选定指定数量的内鬼，并通过Discord消息通知他们。

## 注意事项

- 使用说明：先用 `/new_player` 在系统中添加简要信息，再使用 `/add_comment` 在系统中添加详细信息。
- 录入详细信息前请确认此ID已存在于数据库中。

## 开始使用

1. 访问 [Discord Developer Portal](https://discord.com/developers/applications) 并创建一个新的应用来获取您的Discord机器人密钥。
2. 将机器人添加到您的Discord服务器。
3. 创建两个文本文件：`discord_key.txt` 和 `openAI_key.txt`，分别存储Discord机器人的key和OpenAI账号的key。
4. 使用 `/help` 指令查看所有可用的指令。
5. 开始使用各种功能！


### 配置API密钥

- 在项目根目录下创建两个文本文件：`discord_key.txt` 和 `openAI_key.txt`。
- 在 `discord_key.txt` 中输入您的Discord机器人密钥。
- 在 `openAI_key.txt` 中输入您的OpenAI账号密钥。
- 注意：这两个文件不应上传到GitHub。

## 贡献

如果您有任何问题或建议，请随时提出。


 
