import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @app_commands.command()
    async def yardım(self, interaction: discord.Integration , reason: str):
            if(reason =="komut"):
                
                emb=discord.Embed(description="""!yardım komut => komut bilgileri
                                                 !yardım admin => admin komutları
                                                 !yardım user  => kullanıcı ile alakalı komutlar""")

                emb.set_author(name="superbot - yardım komutları",)
                await interaction.response.send_message(embed=emb)
            elif(reason =="admin"):
                emb=discord.Embed(description="""!yenile => dosyaları günceller
                                                 !clean "sayı" => sayı değerinde mesajları siler
                                                 !kick  "sebep"=> sebep belirterek ya da belirtmeden kullanıcıyı atmaya yarar
                                                 !ban  "sebep"=> sebep belirterek ya da belirtmeden kullanıcıyı yasaklamaya yarar""")

                emb.set_author(name="superbot - yardım komutları",)
                await interaction.response.send_message(embed=emb)
                
            elif(reason =="user"):    
                emb=discord.Embed(description="""!rol => kullanıcının rolünü gösterir
                                                 !kullanıcı "sayı" => kullanıcı hakkında bilgileri gösterir""")
                emb.set_author(name="superbot - yardım komutları",)
                await interaction.response.send_message(embed=emb)
            
            else:
                await interaction.response.send_message("eksik ya da hatalı komut girdiniz. lütfen tekrar deneyin.")
            
async def setup(bot):
    
    await bot.add_cog(Help(bot))