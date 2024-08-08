import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord import app_commands


class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot        
        self.url="https://steamcommunity.com/"
        
        
    
    def find_id(self,steam_id):
        page= requests.get(self.url+"profiles/"+steam_id)
        soup = BeautifulSoup(page.text, "html.parser")
        
        if soup.findAll("div",attrs={"class":"error_ctn"}):
            page= requests.get(self.url+"id/"+steam_id)
            soup = BeautifulSoup(page.text, "html.parser")
            if soup.findAll("span", attrs={"class":"actual_persona_name" }):
                result =soup.find("span", attrs={"class":"actual_persona_name" })
                return(result.text)
            else:
                return("hatalı id girdiniz")
            
            
        else:
            result =soup.find("span", attrs={"class":"actual_persona_name" })
            return (result.text)
    
    @app_commands.command()
    async def id(self,interaction: discord.Integration,steam_id: str):
        
        
        await interaction.response.send_message(self.find_id(steam_id))


            
            
async def setup(bot):
    
    await bot.add_cog(Steam(bot))
