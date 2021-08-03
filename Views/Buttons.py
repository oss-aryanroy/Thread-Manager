import discord
import config

class InviteButtons(discord.ui.View):
    def __init__(self, url):
        super().__init__()
        self.value = 0
        if config.ARROW_EMOTE is None:
            self.arrow = "\N{Black Rightwards Arrow}"
        else:
            self.arrow = config.ARROW_EMOTE
        self.add_item(discord.ui.Button(label="Invite me!", emoji=self.arrow, url=url))

    
