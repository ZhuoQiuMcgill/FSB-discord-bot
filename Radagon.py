import discord
import os
import datetime
import random
import openai
from   discord     import app_commands
from discord.app_commands import CommandInvokeError

from   DB_Manager  import DB_Manager
from   SpyGame     import *


guild_ids = [934888633633222686, 608826511965028353, 564629259935678482]


class My_Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Logged in as {self.user}")


db = DB_Manager("FSB.db")
bot_token = open("discord_key.txt", "r").readline().strip()
OPENAI_API_KEY = open("openAI_key.txt", "r").readline().strip()
openai.api_key = OPENAI_API_KEY
client = My_Client()
tree = app_commands.CommandTree(client)
ALL_GAME = {}

population = "上榜人数： " + str(db.count_player()) + "\n"
fsb_description_list = [("查看列表", "/list"),
                        ("按创建日期查看列表", "/list d"),
                        ("按详细信息数量查看列表", "/list n"),
                        ("查看详细信息", "/detail ID"),
                        ("录入简易信息", "/new_player ID 简略信息"),
                        ("录入详细信息", "/add_comment ID 详细信息"),
                        ("开始抓内鬼游戏", "/new_game 内鬼数量"),
                        ("加入队伍", "/join game_code blue/red"),
                        ("查看游戏信息", "/game_info game_code"),
                        ("安排内鬼", "/game_start game_code"),
                        ("消息接收测试", "/msg_test game_code")]
fsb_description_msg = """
使用说明：先用/new_player在系统中添加简要信息，再使用/add_comment在系统中添加详细信息
注意：输入时只打<>内的内容，不要打<>，录入详细信息前请确认此ID已存在于数据库中
"""

# error msg
detail_error          = "格式错误: -detail空格<ID>"
new_player_error      = "格式错误: -new_player空格<ID>空格<简略信息>\n如果ID带有空格请将空格改为下划线，例子Trolling Yasuo改为Trolling_Yasuo"
add_comment_error     = "格式错误: -add_comment空格<ID>空格<详细信息>\n如果ID带有空格请将空格改为下划线，例子Trolling Yasuo改为Trolling_Yasuo"
player_exists_error   = "此人已经存在于数据库中，请为其添加详细信息"
not_exists_error      = "此人不在数据库中，请先录入简易信息"
not_int_error         = "输入出错，请输入-new_game空格<int>开始新游戏"
game_not_exists_error = "此游戏不存在，请检查game_code是否正确"


def text_format(all_text, index):
    result = ""
    for text in all_text:
        result += str(text[index]) + "\n"
    return result


def sort_list(my_dict, sort_type):
    # my_dict = {GID : (Binfo, count, date)}
    # return [(GID, Binfo, [option]count/date)]
    result = []
    if sort_type == "a":
        sorted_list = sorted(my_dict.items(), key=lambda x: x[0])
    elif sort_type == "n":
        sorted_list = sorted(my_dict.items(), key=lambda x: x[1][1])
    elif sort_type == "d":
        sorted_list = sorted(my_dict.items(), key=lambda x: x[1][2])
    else:
        for gid in my_dict:
            result.append((gid, my_dict[gid][0]))
        return result

    for (gid, (binfo, count, date)) in sorted_list:
        if sort_type == "a":
            result.append((gid, binfo, None))
        elif sort_type == "n":
            result.append((gid, binfo, count))
        elif sort_type == "d":
            result.append((gid, binfo, date))
    return result


async def chat_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"You are a helpful assistant.\nUser: {prompt}\nAssistant:",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message


@tree.command(name="help", description="this is a help message")
async def help(interaction : discord.Interaction):
    population = "上榜人数： " + str(db.count_player()) + "\n"
    embed = discord.Embed(title="Bot Commands", description=population, color=discord.Colour.dark_green())
    embed.add_field(
        name="指令介绍",
        value=text_format(fsb_description_list, 0),
        inline=True)
    embed.add_field(
        name="指令内容",
        value=text_format(fsb_description_list, 1),
        inline=True)
    embed.add_field(
        name="注意事项",
        value=fsb_description_msg,
        inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name="list", description="check list")
async def list_default(interaction : discord.Interaction):
    my_dict = db.list_info()
    embed = discord.Embed(title="封神榜", description=population, color=discord.Colour.dark_red())
    fsb = sort_list(my_dict, "a")
    embed.add_field(
        name="游戏ID",
        value=text_format(fsb, 0),
        inline=True)

    embed.add_field(
        name="简要信息",
        value=text_format(fsb, 1),
        inline=True)
    await interaction.response.send_message(embed=embed)


@tree.command(name="list_sort", description="check list with a sort type")
async def list_sort(interaction : discord.Interaction, sort_type : str):
    my_dict = db.list_info()
    embed = discord.Embed(title="封神榜", description=population, color=discord.Colour.dark_red())
    if sort_type == "n":
        fsb = sort_list(my_dict, "n")
        embed.add_field(
            name="游戏ID",
            value=text_format(fsb, 0),
            inline=True)

        embed.add_field(
            name="简要信息",
            value=text_format(fsb, 1),
            inline=True)

        embed.add_field(
            name="评论数量",
            value=text_format(fsb, 2),
            inline=True)

    elif sort_type == "d":
        fsb = sort_list(my_dict, "d")
        embed.add_field(
            name="游戏ID",
            value=text_format(fsb, 0),
            inline=True)

        embed.add_field(
            name="简要信息",
            value=text_format(fsb, 1),
            inline=True)

        embed.add_field(
            name="评论日期",
            value=text_format(fsb, 2),
            inline=True)
    else:
        fsb = sort_list(my_dict, "")
        embed.add_field(
            name="游戏ID",
            value=text_format(fsb, 0),
            inline=True)

        embed.add_field(
            name="简要信息",
            value=text_format(fsb, 1),
            inline=True)
    await interaction.response.send_message(embed=embed)


@tree.command(name="detail", description="get detail information")
async def detail(interaction : discord.Interaction, gid : str):
    try:
        await interaction.response.send_message(embed=db.get_player_by_GID(gid).get_detail_info())
    except ValueError:
        embed = discord.Embed(title="Error", description=not_exists_error, color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)


@tree.command(name="new_player", description="add a new player")
async def new_player(interaction : discord.Interaction, gid : str, brief_info : str):
    try:
        db.register_player(gid, brief_info)
        embed = discord.Embed(title="success", description="已成功将" + gid + "添加至数据库", color=discord.Colour.green())
        await interaction.response.send_message(embed=embed)
    except ValueError:
        embed = discord.Embed(title="Error", description=player_exists_error, color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)


@tree.command(name="add_comment", description="add comments to a player")
async def add_comment(interaction : discord.Interaction, gid : str, comment : str):
    uid = str(interaction.user)
    try:
        db.rate_player(gid, uid, comment, str(datetime.datetime.now())[:10])
        await interaction.response.send_message(embed=db.get_player_by_GID(gid).get_detail_info())
    except ValueError:
        embed = discord.Embed(title="Error", description=not_exists_error, color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)


@tree.command(name="new_game", description="create a new game")
async def new_game(interaction : discord.Interaction, number_of_spy : int):
    def random_code(n):
        result = ""
        for i in range(n):
            result += str(random.randint(0, 9))
        return result
    game_code = random_code(6)
    while game_code in ALL_GAME:
        game_code = random_code(6)
    ALL_GAME[game_code] = SpyGame(game_code, number_of_spy)
    title = "游戏" + game_code + "已创建(" + str(number_of_spy) + "个内鬼)"
    description = "输入:\n/join " + game_code + " blue\n/join " + game_code + " red\n来加入游戏"
    embed = discord.Embed(title=title, description=description, color=discord.Colour.dark_gold())
    await interaction.response.send_message(embed=embed)


@tree.command(name="join", description="join spy game")
async def join(interaction : discord.Interaction, game_code : str, side : str):
    player = interaction.user
    if game_code not in ALL_GAME:
        embed = discord.Embed(title="Error", description=game_not_exists_error, color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)
    else:
        game = ALL_GAME[game_code]
        msg  = game.add_player(player, side)
        if "未正确加入游戏" in msg:
            embed = discord.Embed(title="Error", description=msg, color=discord.Colour.red())
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="success", description=msg, color=discord.Colour.green())
            await interaction.response.send_message(embed=embed)


@tree.command(name="start_game", description="start spy game")
async def start_game(interaction : discord.Interaction, game_code : str):
    if game_code not in ALL_GAME:
        embed = discord.Embed(title="Error", description=game_not_exists_error, color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)
    else:
        game = ALL_GAME[game_code]
        msg  = game.game_start()
        if "内鬼已确定" in msg:
            embed = discord.Embed(title="success", description=msg, color=discord.Colour.green())
            for spy in game.spy_blue:
                await spy.send("你是蓝色方内鬼")
            for spy in game.spy_red:
                await spy.send("你是红色方内鬼")
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=msg, color=discord.Colour.red())
            await interaction.response.send_message(embed=embed)


@tree.command(name="game_info", description="check game information")
async def game_info(interaction : discord.Interaction, game_code : str):
    if game_code not in ALL_GAME:
        embed = discord.Embed(title="Error", description=game_not_exists_error, color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)
    else:
        game = ALL_GAME[game_code]
        await interaction.response.send_message(embed=game.game_info())


@tree.command(name="msg_test", description="send a test message to all player")
async def msg_test(interaction : discord.Interaction, game_code : str):
    if game_code not in ALL_GAME:
        embed = discord.Embed(title="Error", description=game_not_exists_error, color=discord.Colour.red())
        await interaction.response.send_message(embed=embed)
    else:
        game = ALL_GAME[game_code]
        for player in game.players_blue:
            await player.send("这是一条测试消息，测试您是否能正常接收到机器人的消息")
        for player in game.players_red:
            await player.send("这是一条测试消息，测试您是否能正常接收到机器人的消息")
        embed = discord.Embed(title="success", description="已发送测试消息", color=discord.Colour.green())
        await interaction.response.send_message(embed=embed)


@tree.command(name="gpt", description="Chat with GPT")
async def chat(interaction: discord.Interaction, *, message: str):
    # 发送用户的问题
    await interaction.response.send_message(f"User: {message}")

    # 生成GPT回复

    prompt = f"User: {message}\nAI:"
    response = await chat_gpt(prompt)

    # 发送GPT回复
    await interaction.channel.send(f"GPT-3: {response}")



client.run(bot_token)
