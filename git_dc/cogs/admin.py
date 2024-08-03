import discord
import time
from discord.ext import commands

class Admin(commands.Cog):
    
    
    def __init__(self, bot):
        self.bot = bot
    @commands.command(hidden=True)
    async def yenile(self, ctx, value:str) :
        
        dizin= "cogs."
        
        try:
            if(ctx.author.guild_permissions.administrator):
                    await self.bot.unload_extension(dizin + value)
                    await self.bot.load_extension(dizin + value)
                    await ctx.send(value+ " dosyası yenilendi")

            else:
                await ctx.send("bu komut için yetkiniz yok")       
        except ImportError as e:
            print(e)
    
        
    @commands.command(aliases=["clear"])        
    async def clean(self,ctx,num:int):
        
        min=0
        max=100

        if(ctx.author.guild_permissions.administrator):
            if(num > min and num<=max):
                Channel = ctx.channel
                message = [msg async for msg in Channel.history(limit=num)]


                
                message_2 = await ctx.send("{} adet mesaj bulnuyor".format(num))
                time.sleep(1)
                await message_2.edit(content="{} adet mesaj siliniyor".format(num))
                time.sleep(0.5)
                await Channel.delete_messages(message)
                await message_2.edit(content="{} adet mesaj silindi...".format(num))
                time.sleep(0.5)
                message = [msg async for msg in Channel.history(limit=1)]
                await Channel.delete_messages(message)
            else:
                await ctx.send("en fazla {} mesaj silebilirim".format(max))    
        else:
            await ctx.send("bu komut için yetkiniz yok")
          
  
    @commands.command()
    async def kick(self,ctx, member: discord.Member,*,sebep=None):
     try: 
        if(ctx.author.guild_permissions.administrator): 
                if sebep:    
                    await member.kick(reason=sebep)
                    await ctx.send(f"**{member.mention}**, **{sebep}** sebebiyle sunucudan atıldı")
                else:
                    await member.kick(reason=None)
                    await ctx.send(f"**{member.mention}**,sunucudan atıldı")
        else:
            await ctx.send("bu komut için yetkiniz yok")
     except ImportError as e:
            print(e)

    @commands.command()
    async def ban(self,ctx, member: discord.Member,*,sebep=None):
       try: 
        if(ctx.author.guild_permissions.administrator): 
            if sebep:
                await member.ban(reason=sebep)
                await ctx.send(f"üye sunucudan **{member.mention}**, **{sebep}** sebebiyle yasaklandı")     
            else:
                 await member.ban(reason=None)
                 await ctx.send(f"**{member.mention}**, sunucudan yasaklandı")       
        else:
            await ctx.send("bu komut için yetkiniz yok")
       except ImportError as e:
            print(e) 
        
        
            
async def setup(bot):
    await bot.add_cog(Admin(bot))        