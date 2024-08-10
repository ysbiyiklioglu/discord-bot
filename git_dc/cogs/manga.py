import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands, tasks
import sqlite3
import re


class Manga1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot        
        self.url = 'https://mangaokutr.com/'
        self.database = sqlite3.connect('mangaoku.db')
        self.cursor = self.database.cursor()

        # Başlangıçta tabloları kontrol et
        self.create_table()

        self.check_for_new_manga.start()

    def create_table(self):
        # Manga tablosunu oluştur (varsa, tekrar oluşturmaz)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS manga (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT UNIQUE,
                bölüm INTEGER
            )
        ''')
        self.database.commit()

    def extract_episode_number(self, text):
        # Bölüm numarasını metinden ayıklamak için düzenli ifade kullan
        match = re.search(r'Bölüm (\d+)', text)
        if match:
            return int(match.group(1))  # İlk grup, bölüm numarasını içerir
        return None

    @tasks.loop(minutes=5)  # Her 5 dakikada bir çalışacak şekilde ayarla
    async def check_for_new_manga(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Mangaların listesini çek (sınıf adını doğrulayın)
        manga_list = soup.find_all('div', class_='bs styletere stylefiv stylesix')

        for manga in manga_list:
            manga_title = manga.find('a')['title']
            manga_url = manga.find('a')['href']
            manga_Chapter = manga.find('ul', attrs={"class": "chfiv"})
            manga_episode_text = manga_Chapter.find('a').text

            manga_episode = self.extract_episode_number(manga_episode_text)
            if manga_episode is None:
                manga_episode = 0  # Bölüm bulunamazsa 0 yap

            # Veritabanında manga başlığı olup olmadığını kontrol et
            self.cursor.execute("SELECT bölüm FROM manga WHERE isim = ?", (manga_title,))
            data = self.cursor.fetchone()

            if data:
                current_episode = int(data[0])  # `fetchone()` tuple döndürür, bunu `int`'e dönüştürün

                if current_episode < manga_episode:
                    # Mevcut bölümden daha yüksek olan her yeni bölüm için güncelleme ve bildirim gönder
                    for new_episode in range(current_episode + 1, manga_episode + 1):
                        self.cursor.execute("UPDATE manga SET bölüm = ? WHERE isim = ?", (new_episode, manga_title))
                        self.database.commit()

                        for guild in self.bot.guilds:
                            channel = discord.utils.get(guild.text_channels, name="manga-bilgi")
                            if channel:
                                await channel.send(f"Yeni bölüm yüklendi: {manga_title} - Bölüm {new_episode} ({manga_url})")

            else:
                # Manga yeni ise, veritabanına ekle
                self.cursor.execute("INSERT INTO manga (isim, bölüm) VALUES (?, ?)", (manga_title, manga_episode))
                self.database.commit()
                
                # Yeni manga bulunduğunu bildirim olarak gönder
                for guild in self.bot.guilds:
                    channel = discord.utils.get(guild.text_channels, name="manga-bilgi")
                    if channel:
                        await channel.send(f"Yeni manga bulundu: {manga_title} - Bölüm {manga_episode} ({manga_url})")

    @check_for_new_manga.before_loop
    async def before_check_for_new_manga(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.database.close()

async def setup(bot):
    await bot.add_cog(Manga1(bot))

