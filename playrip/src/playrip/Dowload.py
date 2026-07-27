import os
from mutagen.mp4 import MP4, MP4Cover
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import eyed3
from playrip import get
from pytubefix import YouTube
from bs4 import BeautifulSoup
import requests

def Youtube(url:str, formato_do_audio:str="mp3", thumbnail:bool=True,diretorio_destino:str=os.path.expanduser("~/Downloads")):
    if formato_do_audio.lower() == "mp3":
        yt = YouTube(url)
        artist = yt.author
        titulo = yt.title
        print(f"titulo do video do Youtube: {titulo}")
        print(f"diretorio escolhido foi: {diretorio_destino}\n")
        titulo_novo1 = (
            titulo.replace("/", "")
            .replace("|", "")
            .replace("?", "")
            .replace("*", "")
            .replace("<", "")
            .replace(">", "")
            .replace(":", "")
            .replace("\\", "")
        )
        caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.m4a"
        get.audio(url=url, diretorio_destino=diretorio_destino)
        audiofile = eyed3.load(f"{diretorio_destino}/{titulo_novo1}.mp3")
        if not audiofile.tag:
            audiofile.initTag()
        audiofile.tag.artist = artist
        if thumbnail:
            get.thumbnail(url=url, diretorio_destino=diretorio_destino)
            with open(f"{diretorio_destino}/capa.jpg", "rb") as img_file:
                img_data = img_file.read()
            audiofile.tag.images.set(3, img_data, "image/jpeg")
        audiofile.tag.save()
        os.remove(f"{diretorio_destino}/capa.jpg")
    if formato_do_audio.lower() == "mp4":
        yt = YouTube(url)
        artist = yt.author
        titulo = yt.title
        print(f"titulo do video do Youtube: {titulo}")
        print(f"diretorio escolhido foi: {diretorio_destino}\n")
        titulo_novo1 = (
            titulo.replace("/", "")
            .replace("|", "")
            .replace("?", "")
            .replace("*", "")
            .replace("<", "")
            .replace(">", "")
            .replace(":", "")
            .replace("\\", "")
        )
        get.video(url=url, diretorio_destino=diretorio_destino)
        caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.mp4"
        video = MP4(caminho_arquivo)
        video["\xa9ART"] = artist
        if thumbnail:
            get.thumbnail(url=url, diretorio_destino=diretorio_destino)
            with open(f"{diretorio_destino}/capa.jpg", "rb") as img_file:
                img_data = img_file.read()
            video["covr"] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]
        video.save()
        os.remove(f"{diretorio_destino}/capa.jpg")


def Spotify(url:str, thumbnail:str, diretorio_destino=os.path.expanduser("~/Downloads")):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    thumb = soup.find("meta", property="og:image")["content"]
    titulo_spotify = soup.find("meta", property="og:title")["content"]
    artista = soup.find("meta", property="og:description")["content"].split(" · ")[0]
    if ", " in artista:
        artista = artista.split(", ")[0]
    Novo_titulo_spotify = (
        titulo_spotify.replace("/", "")
        .replace("|", "")
        .replace("?", "")
        .replace("*", "")
        .replace("<", "")
        .replace(">", "")
        .replace(":", "")
        .replace("\\", "")
    )
    if f" - Single by {artista}  Spotify" in Novo_titulo_spotify:
        Novo_titulo_spotify = Novo_titulo_spotify.replace(f" - Single by {artista}  Spotify", "")
    print(f"titulo da musica do spotify: {titulo_spotify}")
    print(f"diretorio escolhido foi: {diretorio_destino}\n")
    get.audio(artista=artista, titulo_da_musica=Novo_titulo_spotify, diretorio_destino=diretorio_destino, url=None)
    audiofile = eyed3.load(f"{diretorio_destino}/{Novo_titulo_spotify}.mp3")
    if audiofile is None:
        print("Arquivo inválido")
        return
    if not audiofile.tag:
        audiofile.initTag()
    if thumbnail:
        get.thumbnail(url=thumb, diretorio_destino=diretorio_destino)
        with open(f"{diretorio_destino}/capa.jpg", "rb") as img_file:
            img_data = img_file.read()
        audiofile.tag.images.set(3, img_data, "image/jpeg")
    audiofile.tag.artist = artista
    audiofile.tag.save()
    os.remove(f"{diretorio_destino}/capa.jpg")
