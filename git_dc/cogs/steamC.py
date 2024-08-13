import os
import discord
from steam_web_api import Steam
import json
from discord.ext import commands
from discord import app_commands
import datetime

class steamCon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Steam API anahtarını çevre değişkenlerinden alıyoruz.
        self.KEY = os.environ.get("STEAM_API_KEY")
        # Steam API istemcisini başlatıyoruz.
        self.steam = Steam(self.KEY)

    def date_time(self, date):
        # Bir Unix zaman damgasını insan tarafından okunabilir bir tarihe dönüştürüyoruz.
        d_time = datetime.datetime.fromtimestamp(date)
        return d_time

    @app_commands.command()
    async def s_bilgi(self, interaction: discord.Interaction, id: str):
            # `user2` için bir bayrak oluşturuyoruz, bu `search_user` fonksiyonunun kullanıldığını belirtiyor.
            u2 = False
              
            # Steam kullanıcı detaylarını ID ile alıyoruz.
            user = self.steam.users.get_user_details(id)
         
            # Kullanıcı adını veya ID'yi kullanarak kullanıcıyı arıyoruz.
            user2 = self.steam.users.search_user(id)
            player = None
            
            
            if user is None and user2 is None:
                await interaction.response.send_message("API'den geçerli bir yanıt alınamadı. Lütfen tekrar deneyin.")
                return

            
            # Eğer `user2` içinde bir oyuncu varsa, onun detaylarını alıyoruz.
            player = None
            if user2 and 'player' in user2:
                print("API Yanıtı:", json.dumps(user2, indent=2))
                player = user2['player']
                # Eğer `search_user` fonksiyonu kullanılmışsa, oyuncunun Steam ID'sini güncelliyoruz.
                id = player.get("steamid")
                u2 = True
            try:
                # Steam kullanıcı seviyesini ve yasaklamalarını alıyoruz.
                level = self.steam.users.get_user_steam_level(id)
                ban = self.steam.users.get_player_bans(id)
            except Exception as e:
                await interaction.response.send_message(f"**{id} id'sine sahip sahip Kullanıcı bilgileri bulunamadı.**")
                if e=="400 Bad Request <html><head><title>Bad Request</title></head><body><h1>Bad Request</h1>Please verify that all required parameters are being sent</body></html>":
                        (f"{id} id'sine sahip sahip Kullanıcı bilgileri bulunamadı.")
                return

            # VAC (Valve Anti-Cheat) bilgilerini almak için kontrol yapıyoruz.
            vac = None
            if ban and 'players' in ban:
                vac = ban['players'][0]

            # Eğer `user2` kullanılmamışsa (`u2 == False`), `user` içindeki oyuncu bilgilerini alıyoruz.
            if user and 'player' in user and u2 == False:
                print("API Yanıtı:", json.dumps(user, indent=2))
                player = user['player']

            # Eğer `player` bilgisi mevcutsa, kullanıcı bilgilerini çekip embed mesajı oluşturuyoruz.
            if player:
                personaname = player.get('personaname')  # Kullanıcı adı
                profileurl = player.get('profileurl')  # Profil URL'si
                avatar = player.get("avatarfull")  # Avatar URL'si
                timecreated = player.get("timecreated")  # Hesabın kurulduğu tarih
                lvl = level.get("player_level") if level else "Bilinmiyor"  # Kullanıcı seviyesi
                
                # VAC yasaklama bilgileri
                bn = vac.get("VACBanned")
                bantime = vac.get("DaysSinceLastBan")
                if bn == True:
                    bn = f"❌ {bantime} gündür"
                if bn == False:
                    bn = "✅"
                
                # Embed mesajını oluşturuyoruz ve dolduruyoruz.
                emb = discord.Embed(color=0xff0080)
                emb.set_thumbnail(url=avatar)
                emb.add_field(name="Kullanıcı Adı", value=personaname)              
                emb.add_field(name="Kullanıcı seviyesi", value=lvl)
                emb.add_field(name="Kullanıcı id", value=id)
                emb.add_field(name="VAC", value=bn)
                emb.add_field(name="Hesap Kurulma Tarihi", value=self.date_time(timecreated))
                emb.add_field(name="Profil URL", value=profileurl)
                
                # Embed mesajını yanıt olarak gönderiyoruz.
                await interaction.response.send_message(embed=emb)
            else:
                # Eğer kullanıcı bilgileri bulunamadıysa, bir hata mesajı gönderiyoruz.
                await interaction.response.send_message("Kullanıcı bilgileri bulunamadı.")
        
async def setup(bot):
    # Steam API entegrasyonunu sağlayan cog'u Discord botuna ekliyoruz.
    await bot.add_cog(steamCon(bot))
