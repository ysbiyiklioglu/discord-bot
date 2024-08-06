import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

database = sqlite3.connect('kanwit.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS messages(message_content STRING, message_id INT) ")

class DB(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @app_commands.command()
    async def write(self,interaction: discord.Integration ,message:str):
        
        query = "INSERT INTO messages VALUES (?,?)"
        cursor.execute(query, (message,interaction.id))
        database.commit()
        
        await interaction.response.send_message("Message written to database")
        
        
        
    @app_commands.command()
    async def delete(self,interaction: discord.Integration ,message:str):
        
        query = "DELETE FROM messages WHERE message_content = ?"
        cursor.execute(query, (message,))
        database.commit()
        
        await interaction.response.send_message("Message deleted")
        
    @app_commands.command()
    async def search(self,interaction: discord.Integration,message:str):
        
        
        query=f"SELECT * FROM messages where message = {message}"    
        
        data= cursor.execute(query,).fetchone()
        
        
    
        if data:
               
                emb = discord.Embed(color=0xff0080)
       
                emb.add_field(name="message",value=data[0])  
                emb.add_field(name="id",value=data[1])  
          
                await interaction.response.send_message(embed=emb)
     
        
        else:
            await interaction.response.send_message("aradığınız id ye sahip bir kullanıcı bulunamamakta")
        
        
        
async def setup(bot):
    
    await bot.add_cog(DB(bot))