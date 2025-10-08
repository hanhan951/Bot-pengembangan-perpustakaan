import discord
import random
from discord.ext import commands
from bot_logic import gen_pass
from settings import TOKEN
import os
import requests

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command()
async def min(ctx, left: int, right: int):
    await ctx.send(left - right)

@bot.command()
async def times(ctx, left: int, right: int):
    await ctx.send(left * right)

@bot.command()
async def divide(ctx, left: int, right: int):
    await ctx.send(left / right)

@bot.command()
async def exp(ctx, left: int, right: int):
    await ctx.send(left ** right)

@bot.command()
async def meme(ctx):
    """Mengirim meme acak dari folder images"""
    memes = os.listdir('images')
    meme_name = random.choice(memes)
    with open(f'images/{meme_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('dog')
async def dog(ctx):
    image_url = get_dog_image_url()
    await ctx.send(image_url)

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

def get_fox_image_url():
    url = 'https://randomfox.ca/floof/'
    res = requests.get(url)
    data = res.json()
    return data['image']

@bot.command('fox')
async def fox(ctx):
    image_url = get_fox_image_url()
    await ctx.send(image_url)

@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        t.write(my_string)

@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        t.write("\n" + my_string)

@bot.command()
async def baca(ctx):
    with open('kalimat.txt', 'r', encoding='utf-8') as t:
        document = t.read()
    await ctx.send(document)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def pw(ctx):
    await ctx.send(f'Kata sandi yang dihasilkan: {gen_pass(10)}')

@bot.command()
async def passgen(ctx, length: int = 10):
    password = gen_pass(length)
    await ctx.send(f"🔑 Your generated password: `{password}`")

@bot.command(name="pass")
async def pass_command(ctx, length: int = 10):
    password = gen_pass(length)
    await ctx.send(f"🔐 Generated password: `{password}`")

@bot.command()
async def bye(ctx):
    await ctx.send("😀")

@bot.command()
async def coinflip(ctx):
    num = random.randint(1, 2)
    if num == 1:
        await ctx.send("It's Head! 🪙")
    else:
        await ctx.send("It's Tail! 🪙")

@bot.command()
async def dice(ctx):
    nums = random.randint(1, 6)
    await ctx.send(f'It is {nums}! 🎲')


@bot.command()
async def joined(ctx, member: discord.Member):
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.command()
async def local_drive(ctx):
    try:
        folder_path = "./files"
        files = os.listdir(folder_path)
        file_list = "\n".join(files)
        await ctx.send(f"Files in the files folder:\n{file_list}")
    except FileNotFoundError:
        await ctx.send("Folder not found.")

@bot.command()
async def showfile(ctx, filename):
    folder_path = "./files/"
    file_path = os.path.join(folder_path, filename)
    try:
        await ctx.send(file=discord.File(file_path))
    except FileNotFoundError:
        await ctx.send(f"File '{filename}' not found.")

@bot.command()
async def simpan(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            await attachment.save(f"./files/{file_name}")
            await ctx.send(f"Menyimpan {file_name}")
    else:
        await ctx.send("Anda lupa mengunggah :(")

@bot.command()
async def helpme(ctx):
    commands_list = """
**🧮 Math Commands**
$add x y — Tambah dua angka
$min x y — Kurangi dua angka
$times x y — Kali dua angka
$divide x y — Bagi dua angka
$exp x y — Pangkatkan dua angka

**🎮 Fun & Games**
$coinflip — Lempar koin
$dice — Lempar dadu
$bye — Balas emoji 😀

**🖼️ Images**
$meme — Kirim gambar meme acak
$dog — Gambar anjing acak
$duck — Gambar bebek acak
$fox — Gambar rubah acak

**🔐 Password**
$pass — Password acak
$passgen [panjang] — Password sesuai panjang

**📄 File Handling**
$tulis — Buat file teks baru
$tambahkan — Tambah teks ke file
$baca — Tampilkan isi file
$simpan — Simpan file yang diunggah
$showfile [nama_file] — Kirim file dari folder ./files
$local_drive — Lihat semua file

Ketik `$helpme` untuk melihat daftar ini lagi.
"""
    await ctx.send(commands_list)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Perintah tidak dikenal! Ketik `$helpme` untuk melihat semua perintah.")
    else:
        await ctx.send(f"⚠️ Terjadi kesalahan: {error}")
