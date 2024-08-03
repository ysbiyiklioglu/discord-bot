import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command()
    async def yardım(self, ctx , string):
            if(string =="komut"):
                
                emb=discord.Embed(description="""!yardım komut => komut bilgileri
                                                 !yardım admin => admin komutları
                                                 !yardım user  => kullanıcı ile alakalı komutlar""")

                emb.set_author(name="superbot - yardım komutları",)
                await ctx.send(embed=emb)
            if(string =="admin"):
                emb=discord.Embed(description="""!yenile => dosyaları günceller
                                                 !clean "sayı" => sayı değerinde mesajları siler
                                                 !kick  "sebep"=> sebep belirterek ya da belirtmeden kullanıcıyı atmaya yarar
                                                 !ban  "sebep"=> sebep belirterek ya da belirtmeden kullanıcıyı yasaklamaya yarar""")

                emb.set_author(name="superbot - yardım komutları",)
                await ctx.send(embed=emb)
                
            if(string =="user"):    
                emb=discord.Embed(description="""!rol => kullanıcının rolünü gösterir
                                                 !kullanıcı "sayı" => kullanıcı hakkında bilgileri gösterir""")
                emb.set_author(name="superbot - yardım komutları",)
                await ctx.send(embed=emb)
            
async def setup(bot):
    
    await bot.add_cog(Help(bot))