import discord
from discord.ext import commands
from pytube import YouTube
import re
import os
intents = discord.Intents(messages = True, guilds = True, reactions = True)
client = commands.Bot(command_prefix="yt!", intents = intents)

#-----------------help-cmd-----------
class MyHelp(commands.HelpCommand):
   # !help
    async def send_bot_help(self, mapping):
        url = f"https://discord.com/api/channels/{self.context.channel.id}/messages"
        # embed = discord.Embed(title = "Title")
        button1 = discord.ui.Button(label="INVITE ME",style = discord.ButtonStyle.link,url = "https://discord.com/api/oauth2/authorize?client_id=877101493155692555&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D877101493155692555%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D877101&scope=applications.commands%20bot")
        button2 = discord.ui.Button(label="SUPPORT SERVER",style = discord.ButtonStyle.link,url = "https://discord.gg/tTr6DvyRCH")     
        embed0 = discord.Embed(title="Help",colour = discord.Colour.red(),description = '''
Hi! I am YouTube Downloader! 
I can Download Youtube Videos for you so you don't need to go to any third party site/app to do the task!

**Youtube Downloader Works With Slash Commands**

__The Available Commands Are :-__

***ytdownload*** - Downloads Video from YouTube from the link entered by you in the slash command

***invite***  - Sends Bot Invite. Make Sure to add me to your Server :)

***support***  - Sends Support Server's Invite


**Note** - All the Commands are Slash Commands so make sure to give me access to create slash commands in this Server if I don't have.
''')
        view = discord.ui.View()
        view.add_item(button1)
        view.add_item(button2)
        await self.context.send(embed=embed0, view=view)
        return

        
client.help_command = MyHelp()
  

#------------------------------------

async def checkytlink(link):
    try:
        yt = YouTube(link)
    except:
        return "invalid"
    return yt
    
@client.event
async def on_ready():
    print("Logged In Successfully")

@client.event
async def on_interaction(interaction):
    if interaction.application_id == 877101493155692555:
        if interaction.type == discord.InteractionType.application_command:
            data = interaction.data
            
            
            if data['name'] == "invite":
                embed=discord.Embed(title='Invite Me here',description='[Click Here](https://discord.com/api/oauth2/authorize?client_id=877101493155692555&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D877101493155692555%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D877101&scope=applications.commands%20bot)',colour=discord.Colour.red())  
                button = discord.ui.Button(label="Invite Me",style = discord.ButtonStyle.link,url = "https://discord.com/api/oauth2/authorize?client_id=877101493155692555&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Fapi%2Foauth2%2Fauthorize%3Fclient_id%3D877101493155692555%26permissions%3D8%26redirect_uri%3Dhttps%253A%252F%252Fdiscord.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id%253D877101&scope=applications.commands%20bot")
                view = discord.ui.View() #this is the view object that holds all the components
                view.add_item(button)
                await interaction.response.send_message(embed = embed,view=view)
                return
            
            if data['name'] == "support":
                embed=discord.Embed(title='Join My Support Server',description='[Support Server](https://discord.gg/tTr6DvyRCH)',colour=discord.Colour.red())  
                button = discord.ui.Button(label="Support Server",style = discord.ButtonStyle.link,url = "https://discord.gg/tTr6DvyRCH")
                view = discord.ui.View() #this is the view object that holds all the components
                view.add_item(button)
                await interaction.response.send_message(embed = embed,view=view)
                return
            

            if data['name'] == 'ytdownload':
                link = data['options'][0]['value']
                checklink = await checkytlink(link)
                if checklink == "invalid":
                    await interaction.response.send_message(content = "Invalid Link Entered",ephemeral = True)
                    return 

                yt = checklink
                type2 = data['options'][1]['value']

                #----------list of resolutions banade-------------------
                if type2.lower() == 'audio':
                    audios = yt.streams.filter(mime_type="audio/mp4", type = 'audio')
                    audio = list(enumerate(audios))
                    m = []
                    for i in audio:
                        i = str(i).split()
                        m = m + re.findall(r"abr=\"([^\"]+)", i[4])
                    if len(m)==0:
                        await interaction.response.send_message(content = "No Audio Options are available for this video to be downloaded",ephemeral = True)
                        return

                    d = {}
                    for i in range(len(m)):
                        d[m[i]] = i

                    await interaction.response.send_message(content = "Choose the Audio Quality",view = YTDOWNLOADaudio(interaction,checklink,m,d))
                if type2.lower() == 'video':
                    videos = yt.streams.filter(mime_type="video/mp4",audio_codec="mp4a.40.2", type = 'video')
                    video = list(enumerate(videos))
                    m=[]
                    for i in video:
                        i = str(i).split()
                        m = m + re.findall(r"res=\"([^\"]+)", i[4])
                    if len(m)==0:
                        await interaction.response.send_message(content = "No Video Options are available for this video to be downloaded",ephemeral = True)
                        return
                    d = {}
                    for i in range(len(m)):
                        d[m[i]] = i
                    await interaction.response.send_message(content = "Choose the resolution size",view = YTDOWNLOADvideo(interaction,checklink,m,d))
    return

                
                   
                



#-----------------------video---------------------------------------------------------------------------
class one44p(discord.ui.Button['YTDOWNLOADvideo']):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.danger,label = "144p")


    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: YTDOWNLOADvideo = self.view
        if interaction.user != view.interaction.user:
            return
        for i in view.children:
            i.disabled = True
        await view.interaction.followup.send("Getting Video, Please Wait!, It may take some time, I'll ping you when it's done")
        videos = view.ytobject.streams.filter(mime_type="video/mp4",audio_codec="mp4a.40.2", type = 'video')
        dn_video = videos[view.d['144p']]
        outfile = f"{interaction.message.id}.mp4"
        dn_video.download(filename = outfile)
        await view.interaction.followup.send(content=f"<@{interaction.user.id}>",file = discord.File(outfile))
        os.remove(outfile)
        view.stop()

class two40p(discord.ui.Button['YTDOWNLOADvideo']):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.danger,label = "240p")


    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: YTDOWNLOADvideo = self.view
        if interaction.user != view.interaction.user:
            return
        for i in view.children:
            i.disabled = True
        await view.interaction.followup.send("Getting Video, Please Wait!, It may take some time, I'll ping you when it's done")
        videos = view.ytobject.streams.filter(mime_type="video/mp4",audio_codec="mp4a.40.2", type = 'video')
        dn_video = videos[view.d['240p']]
        outfile = f"{interaction.message.id}.mp4"
        dn_video.download(filename = outfile)
        await view.interaction.followup.send(content=f"<@{interaction.user.id}>",file = discord.File(outfile))
        os.remove(outfile)
        view.stop()

class three60p(discord.ui.Button['YTDOWNLOADvideo']):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.danger,label = "360p")


    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: YTDOWNLOADvideo = self.view
        if interaction.user != view.interaction.user:
            return
        for i in view.children:
            i.disabled = True
        await view.interaction.followup.send("Getting Video, Please Wait!, It may take some time, I'll ping you when it's done")
        videos = view.ytobject.streams.filter(mime_type="video/mp4",audio_codec="mp4a.40.2", type = 'video')
        dn_video = videos[view.d['360p']]
        outfile = f"{interaction.message.id}.mp4"
        dn_video.download(filename = outfile)
        await view.interaction.followup.send(content=f"<@{interaction.user.id}>",file = discord.File(outfile))
        os.remove(outfile)
        view.stop()

class seven20p(discord.ui.Button['YTDOWNLOADvideo']):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.danger,label = "720p")


    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: YTDOWNLOADvideo = self.view
        if interaction.user != view.interaction.user:
            return
        for i in view.children:
            i.disabled = True
        await view.interaction.followup.send("Getting Video, Please Wait!, It may take some time, I'll ping you when it's done")
        videos = view.ytobject.streams.filter(mime_type="video/mp4",audio_codec="mp4a.40.2", type = 'video')
        dn_video = videos[view.d['720p']]
        outfile = f"{interaction.message.id}.mp4"
        dn_video.download(filename = outfile)
        await view.interaction.followup.send(content=f"<@{interaction.user.id}>",file = discord.File(outfile))
        os.remove(outfile)
        view.stop()

class YTDOWNLOADvideo(discord.ui.View):
    def __init__(self,interaction,ytobject,m,d):
        super().__init__()
        self.interaction = interaction
        self.ytobject = ytobject
        self.m = m 
        self.d = d
        if '144p' in self.m:
            self.add_item(one44p())
        if '240p' in self.m:
            self.add_item(two40p())
        if '360p' in self.m:
            self.add_item(three60p())
        if '720p' in self.m:
            self.add_item(seven20p())
#-----audio-----------------------------------

class four8kbps(discord.ui.Button['YTDOWNLOADaudio']):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.danger,label = "48kbps")


    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: YTDOWNLOADaudio = self.view
        if interaction.user != view.interaction.user:
            return
        for i in view.children:
            i.disabled = True
        await view.interaction.followup.send("Getting Audio, Please Wait!, It may take some time, I'll ping you when it's done")
        audios = view.ytobject.streams.filter(mime_type="audio/mp4", type = 'audio')
        dn_audio = audios[view.d['48kbps']]
        outfile = f"{interaction.message.id}.mp3"
        dn_audio.download(filename = outfile)
        await view.interaction.followup.send(content=f"<@{interaction.user.id}>",file = discord.File(outfile))
        os.remove(outfile)
        view.stop()

class one28kbps(discord.ui.Button['YTDOWNLOADaudio']):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.danger,label = "128kbps")


    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: YTDOWNLOADaudio = self.view
        if interaction.user != view.interaction.user:
            return
        for i in view.children:
            i.disabled = True
        await view.interaction.followup.send("Getting Audio, Please Wait!, It may take some time, I'll ping you when it's done")
        audios = view.ytobject.streams.filter(mime_type="audio/mp4", type = 'audio')
        dn_audio = audios[view.d['128kbps']]
        outfile = f"{interaction.message.id}.mp3"
        dn_audio.download(filename = outfile)
        await view.interaction.followup.send(content=f"<@{interaction.user.id}>",file = discord.File(outfile))
        os.remove(outfile)
        view.stop()

class two56kbps(discord.ui.Button['YTDOWNLOADaudio']):
    def __init__(self):
        super().__init__(style = discord.ButtonStyle.danger,label = "256kbps")


    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: YTDOWNLOADaudio = self.view
        if interaction.user != view.interaction.user:
            return
        for i in view.children:
            i.disabled = True
        await view.interaction.followup.send("Getting Audio, Please Wait!, It may take some time, I'll ping you when it's done")
        audios = view.ytobject.streams.filter(mime_type="audio/mp4", type = 'audio')
        dn_audio = audios[view.d['256kbps']]
        outfile = f"{interaction.message.id}.mp3"
        dn_audio.download(filename = outfile)
        await view.interaction.followup.send(content=f"<@{interaction.user.id}>",file = discord.File(outfile))
        os.remove(outfile)
        view.stop()

class YTDOWNLOADaudio(discord.ui.View):
    def __init__(self,interaction,ytobject,m,d):
        super().__init__()
        self.interaction = interaction
        self.ytobject = ytobject
        self.m = m 
        self.d = d
        if '48kbps' in self.m:
            self.add_item(four8kbps())
        if '128kbps' in self.m:
            self.add_item(one28kbps())
        if '256kbps' in self.m:
            self.add_item(two56kbps())


client.run("BOT_TOKEN")
