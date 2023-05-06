#!/usr/bin/python
import asyncio
import twitchio
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import commands
from twitchio.ext import routines

############
# SPOTIFY
############
spot_id= open('creds/spot_cid.cred','r').read()  # Spotify client ID
spot_sec= open('creds/spot_cs.cred','r').read()  # Spotify client secret
redirect_uri= open('creds/redirect_uri.cred','r').read() # redirect_uri used for Oauth token
scope= "user-library-read user-library-modify user-modify-playback-state user-read-playback-state user-read-currently-playing playlist-modify-public" # Spotify client auth scope


#############
# TWITCH
#############
channel_name = "TwitchUsernameHere" # Channel that should be joined
twch_id= open('creds/twitch_cid.cred','r').read()  # Twitch Client ID
twch_token= open('creds/twitch_token.cred','r').read()  # Twitch OAuth Token

#############
# LOCKS
#############
godonly = False # only god_name can run command
modsonly = False # only mods can run command
god_name = channel_name # channel owner
lastlock = "" # last mod to set lock
autolock_time = 15 # Seconds until autolock routine is ran

##############
# LOCK BLOCKS
##############
# Each command should have the lock block in front of it to check for 
# conditions that could prevent a user from running the command.
# This should only be a temporary solution.
# If it still exist during actual release, then I'm lazy. Sorry.
##############

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token= twch_token,client_id= twch_id, prefix= '!', initial_channels= [channel_name], nick= "LittleSpotBot")


    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        chan = bot.get_channel(channel_name)
        loop = asyncio.get_event_loop()
        loop.create_task(chan.send("SingsNote SpotBot is online! SingsNote"))


    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console.
        print(f"{message.author.name}: {message.content}")

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)


    @commands.command(name=  "bingbong")
    async def bingbong_command(self, ctx: commands.Context):
        # LOCK BLOCK
        if godonly and ctx.author.display_name != god_name:
            print(f"[{ctx.author.display_name}][-] God locked by {god_name}")
            await ctx.send(f"VoteNay God locked by {god_name}")
            return

        if modsonly and not ctx.author.badges['moderator']:
            print(f"[-] Mod locked by {lastlock}.")
            await ctx.send(f"VoteNay Mod locked by {lastlock}")

        else:

            await ctx.send(f"@{ctx.author.display_name} BingBong")
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= spot_id, client_secret= spot_sec, redirect_uri= redirect_uri, scope= scope))
            sp.add_to_queue("1wujqDb6M7WGONFoxroSey") #BingBongSong


    @commands.command(name= "search", aliases=["s"])
    async def search_command(self, ctx:commands.Context):

        # LOCK BLOCK
        if godonly and ctx.author.display_name != god_name:
            print(f"[{ctx.author.display_name}][-] God locked by {god_name}")
            await ctx.send(f"VoteNay God locked by {god_name}")
            return

        if modsonly and not ctx.author.badges['moderator']:
            print(f"[-] Mod locked by {lastlock}.")
            await ctx.send(f"VoteNay Mod locked by {lastlock}")

        else:

            max_limit=1
            sp = spotipy.Spotify(auth_manager= SpotifyOAuth(client_id= spot_id, client_secret= spot_sec, redirect_uri= redirect_uri, scope= scope))
            s = str(ctx.message.content)
            search_str = s.replace("!search", "").strip()
            search_str = search_str.replace("!s", "").strip()
            result = sp.search(search_str,limit=max_limit, type='track')


            for i in range(max_limit):
                tname = result['tracks']['items'][i]['name']
                artist = result['tracks']['items'][i]['album']['artists'][0]['name']
                uri = result['tracks']['items'][i]['album']['artists'][0]['uri']
                release_date = result['tracks']['items'][i]['album']['release_date']
                song_id = result['tracks']['items'][i]['id']
                #full_song = f"{str(i+1)}) {tname} - {artist} ({release_date}) [{song_id}]"
                full_song = f"[search] {tname} by {artist} [ID: {song_id}]"
                await ctx.send(full_song)  



    @commands.command(name= "playing", aliases=['p'])
    async def currentsong_command(self, ctx:commands.Context):

        # LOCK BLOCK
        if godonly and ctx.author.display_name != god_name:
            print(f"[{ctx.author.display_name}][-] God locked by {god_name}")
            await ctx.send(f"VoteNay God locked by {god_name}")
            return

        if modsonly and not ctx.author.badges['moderator']:
            print(f"[-] Mod locked by {lastlock}.")
            await ctx.send(f"VoteNay Mod locked by {lastlock}")

        else:

            sp = spotipy.Spotify(auth_manager= SpotifyOAuth(client_id= spot_id, client_secret= spot_sec, redirect_uri= redirect_uri, scope= scope))
            current = sp.currently_playing()
            title = current['item']['name']
            artist = current['item']['artists'][0]['name']
            await ctx.send(f"@{ctx.author.display_name} SingsNote {title} by {artist} SingsNote")



    @commands.command(name= "queue",aliases=['q'])
    async def add2queue_command(self, ctx:commands.Context):

        # LOCK BLOCK
        if godonly and ctx.author.display_name != god_name:
            print(f"[{ctx.author.display_name}][-] God locked by {god_name}")
            await ctx.send(f"VoteNay God locked by {god_name}")
            return

        if modsonly and not ctx.author.badges['moderator']:
            print(f"[-] Mod locked by {lastlock}.")
            await ctx.send(f"VoteNay Mod locked by {lastlock}")

        else:

            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= spot_id, client_secret= spot_sec, redirect_uri= redirect_uri, scope= scope))
            s = str(ctx.message.content)

            # strip command from message and get rid of whitespace
            song_id = s.replace("!queue", "").strip()
            song_id = song_id.replace("!q", "").strip()


            sp.add_to_queue(song_id)
            track = sp.track(song_id)
            print(f"[+] Added '{track['name']}' by {track['album']['artists'][0]['name']}")
            await ctx.send(f"SingsMic Added '{track['name']}' by {track['album']['artists'][0]['name']} SingsMic")



    @commands.command(name= "debug") #debug
    async def debug_command(self, ctx:commands.Context): 
        """
        Quick command to print whatever to console or chat.
        """
        # Some BS deadcode below.
        print(type(ctx.author.badges))
        print(ctx.author.badges['moderator'])
        print(ctx.author.display_name)
        print(await bot.fetch_streams(user_logins= channel_name))



    @commands.command(name= "godlock")
    async def godlock_command(self, ctx:commands.Context, status: str):
        """
        Enable or disable must be passed as status string.
        """
        # make configurable
        global godonly
        status = status.lower()

        if ctx.author.display_name == god_name:
            # If enabled, change to not enabled
            if status == "disable":
                godonly= False
                print("[-] Godlock disabled")
                await ctx.send("FBtouchdown Godlock disabled")
                return

            # If not enabled, change to enabled    
            if status == "enable":
                godonly= True
                print("FBtouchdown Godlock enabled")
                await ctx.send("FBtouchdown Godlock enabled")
                return
            else:
                await ctx.send(f"@{ctx.author.display_name} Please use 'enable' or 'disable'.")
                
        else:
            await ctx.send(f"VoteNay {god_name} only. No Custers.")


    @commands.command(name= "modlock")
    async def modlock_command(self, ctx:commands.Context, status: str):
        """
        User must past enable or disable for boolean to be flipped.
        If no string is passed, a raised exception will occur and pass.
        """
        # make configurable
        global modsonly
        global lastlock
        status = status.lower()
        print(f"status:{status}")

        if not status.strip():
            return await ctx.send(f"@{ctx.author.display_name} Please use 'enable' or 'disable'.")

        if ctx.author.badges['moderator']:
            # If enabled, change to not enabled
            if status == 'disable':
                modsonly = False
                print("[-] Modlock disabled")
                await ctx.send("FBtouchdown Modlock disabled")
                return

            # If not enabled, change to enabled
            if status == 'enable':
                modsonly = True
                print("[+] Modlock enabled")
                await ctx.send("FBtouchdown Modlock enabled")
                lastlock = ctx.author.display_name
                return
            else:
                await ctx.send(f"@{ctx.author.display_name} Please use 'enable' or 'disable'.")
                
        else:
            await ctx.send(f"VoteNay Mods only. No Custers.")


    @commands.command(name= "isonline") #debug
    async def isonline_command(self, ctx:commands.Context):
        """
        Debug command to check if user is online
        """
        print(ctx.chatters) #debug
        print(type(ctx.chatters))
        
        for each in ctx.chatters:
            print(each.display_name)
            if each.display_name == god_name:
                print(f"[+] {god_name} ONLINE")
                await ctx.send(f"[+] {god_name} ONLINE")
                return
            else:
                print(f"[-] {god_name} OFFLINE")
                await ctx.send(f"[-] {god_name} OFFLINE")
                return       

@routines.routine(seconds= autolock_time)
async def autolock():

    global godonly
    streamerOnline = await bot.fetch_streams(user_logins= [god_name])

    if not streamerOnline:
        godonly = True



bot = Bot()
autolock.start()
bot.run()
