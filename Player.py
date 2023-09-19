import discord


class Detail_info:
    def __init__(self, info, author, date):
        self.info = info
        self.author = author
        self.date = date

    def __str__(self):
        return self.info + "\n\n" + self.author + "于" + self.date + "编辑\n"


class Player:
    def __init__(self, PID, GID, brief_info, detail_info):
        self.PID = PID
        self.GID = GID
        self.brief_info = brief_info
        self.detail_info = detail_info

    def get_brief_info(self):
        return self.GID + "\t" + self.brief_info

    def get_detail_info(self):
        embed = discord.Embed(title=self.GID, description=self.brief_info, color=discord.Colour.green())
        embed.add_field(
            name="op.gg",
            value="op.gg:\thttps://na.op.gg/summoners/na/" + self.GID,
            inline=False)
        for n in range(len(self.detail_info)):
            detail = self.detail_info[n]
            embed.add_field(
                name="评论" + str(n + 1),
                value=str(detail),
                inline=False)
        return embed
