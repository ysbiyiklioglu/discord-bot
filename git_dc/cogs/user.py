import discord
from discord.ext import commands

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def kullanıcı(self,ctx, member: discord.Member):
        if "superbot" in [role.name for role in member.roles]:
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
        await ctx.send(embed=emb)

async def setup(bot):
    
    await bot.add_cog(User(bot))