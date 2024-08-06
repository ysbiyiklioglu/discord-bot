import discord
from discord.ext import commands
from discord import app_commands

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command()
    async def kullanıcı(self,interaction: discord.Integration, member: discord.Member):
        if "bot" in [role.name for role in member.roles]:
                is_bot = "evet"

        else:
                is_bot= "hayır"
            
            
        emb = discord.Embed(color=0xff0080)
        emb.add_field(name="ad",value=member.display_name)    
        emb.add_field(name="durum",value=member.status)  
        emb.add_field(name="rol",value=member.top_role)  
        emb.add_field(name="id",value=member.id)  
        emb.add_field(name="bot mu",value=is_bot)
        emb.add_field(name="hesabı ne zaman kuruldu",value=member.created_at)
        emb.add_field(name="sunucuya ilk giriş",value=member.joined_at) 
        emb.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=emb)
    @app_commands.command()
    async def rol(self,interaction: discord.Integration, member:discord.Member):
        try:
            emb=discord.Embed(color=0xff0080)
            emb.add_field(name="/>",value="**"+ member.display_name+"** adlı kullanıcın rolü: **{}**".format(member.top_role))
            emb.set_thumbnail(url=member.avatar)
            await interaction.response.send_message(embed=emb)
        except ImportError as e:
            print(e)     
async def setup(bot):
    
    await bot.add_cog(User(bot))