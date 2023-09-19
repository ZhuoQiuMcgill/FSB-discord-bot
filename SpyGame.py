import random
import discord


class SpyGame:
    def __init__(self, game_code, nums):
        self.game_code = game_code
        self.nums = nums
        self.players_blue = []
        self.players_red  = []
        self.spy_blue = []
        self.spy_red  = []
        self.game_started = False
        
    def add_player(self, player, side):    
        if side == "blue":
            if player in self.players_blue:
                return str(player) + "已在蓝色方出现"
            if player in self.players_red:
                self.players_red.remove(player)
            self.players_blue.append(player)
            return str(player) + "已成功加入蓝色方"
        if side == "red":
            if player in self.players_red:
                return str(player) + "已在红色方出现"
            if player in self.players_blue:
                self.players_blue.remove(player)
            self.players_red.append(player)
            return str(player) + "已成功加入红色方"
        return str(player) + "未正确加入游戏"
    
    def game_info(self):
        started = "游戏未开始"
        if self.game_started:
            started = "游戏已开始"
        embed = discord.Embed(title="游戏" + self.game_code,
                              description=started + "\n" + str(self.nums) + "个间谍",
                              colour=discord.Colour.dark_gold())
        blue = ""
        red  = ""
        for player in self.players_blue:
            blue += str(player)
            if player in self.spy_blue:
                blue += " (内鬼)"
            blue += "\n"
        for player in self.players_red:
            red += str(player)
            if player in self.spy_red:
                red += " (内鬼)"
            red += "\n"
        embed.add_field(
            name="蓝色方(" + str(len(self.players_blue)) + "人)",
            value=blue,
            inline=True
        )
        embed.add_field(
            name="红色方(" + str(len(self.players_red)) + "人)",
            value=red,
            inline=True
        )
        return embed

    def game_start(self):
        if self.game_started:
            return "游戏已经开始"
        if  0 < self.nums < min(len(self.players_blue), len(self.players_red)):
            for i in range(self.nums):
                b_spy = random.choice(self.players_blue)
                r_spy = random.choice(self.players_red)
                while b_spy in self.spy_blue:
                    b_spy = random.choice(self.players_blue)
                while r_spy in self.spy_red:
                    r_spy = random.choice(self.players_red)
                self.spy_blue.append(b_spy)
                self.spy_red.append(r_spy)
            self.game_started = True
            return "内鬼已确定"
        return "内鬼数量错误"
