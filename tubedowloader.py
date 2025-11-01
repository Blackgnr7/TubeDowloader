#!/usr/bin/env python3  
import os
import requests
import os
import sys
import shutil   
import pathlib
from mutagen.mp4 import MP4,MP4Cover
import eyed3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytubefix import YouTube
from pytubefix import Search
from pydub import AudioSegment


def main():
    if len(sys.argv) > 2:
        url = str(sys.argv[1])
        ttipo = str(sys.argv[2]).lower()
        if ttipo != "mp3" and ttipo != "mp4":
            print("Tipo de arquivo inválido. Use 'mp3' ou 'mp4'.")
            print(ttipo)
            return
        diretorio_destino = os.path.expanduser("~/Downloads")
        if not os.path.exists(diretorio_destino):
            print(f"estranho voçê não tem o diretório: {diretorio_destino}, no seu path ou a pasta no seu sistema")
            return
        if ttipo == "mp3":
            if "youtu" in url:
                yt = YouTube(url)
                thumbnail_peagr = yt.thumbnail_url
                codigo = thumbnail_peagr.split("/")[-2].split("/")[-1]
                thumbnail = "https://i.ytimg.com/vi_webp/" + codigo + "/maxresdefault.webp"
                print(thumbnail)
                artist = yt.author
                titulo = yt.title
                titulo_novo1 = titulo.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
                yt.streams.get_audio_only().download(output_path=diretorio_destino)
                res = requests.get(thumbnail, stream=True)
                with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                    shutil.copyfileobj(res.raw, out_file)
                caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.m4a"
                with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                    img_data = img_file.read()
                sound = AudioSegment.from_file(caminho_arquivo, format="m4a")
                sound.export(f"{diretorio_destino}/{titulo_novo1}.mp3", format="mp3")
                audiofile = eyed3.load(f"{diretorio_destino}/{titulo_novo1}.mp3")
                if not audiofile.tag:
                    audiofile.initTag()
                audiofile.tag.artist = artist
                audiofile.tag.images.set(3, img_data, "image/jpeg")
                audiofile.tag.save()
                print("musica salva tanto como imagem e titulo")
                os.remove(f"{diretorio_destino}/capa.jpg")
                os.remove(f"{caminho_arquivo}")
        elif ttipo == "mp4":
            if "youtu" in url:
                yt = YouTube(url)
                thumbnail_peagr = yt.thumbnail_url
                codigo = thumbnail_peagr[23:34]
                print(codigo)
                thumbnail = "https://i.ytimg.com/vi_webp/" + codigo + "/maxresdefault.webp"
                print(thumbnail)
                artist = yt.author
                titulo = yt.title
                titulo_novo1 = titulo.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
                res = requests.get(thumbnail, stream=True)
                with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                    shutil.copyfileobj(res.raw, out_file)
                with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                    img_data = img_file.read()
                yt.streams.get_highest_resolution().download(output_path=diretorio_destino)
                caminho_arquivo = f"{diretorio_destino}/{titulo_novo1}.mp4"
                video = MP4(caminho_arquivo)
                video["\xa9ART"] = artist
                video["covr"] = [MP4Cover(img_data, imageformat=MP4Cover.FORMAT_JPEG)]
                video.save()
                os.remove(f"{diretorio_destino}/capa.jpg")
        os.system("pause")

    else:
        if sys.argv[1] == "config":
            diretoriodoarquivo = pathlib.Path(__file__).parent.resolve()
            print(f"abrindo o vscode na pasta: {diretoriodoarquivo}")
            os.system(f"code {diretoriodoarquivo}")
        else:
            if "spotify" in sys.argv[1]:    
                url = str(sys.argv[1])
                diretorio_destino = os.path.expanduser("~/Downloads")
                client_id = "you client_id"
                client_secret = "you client_secret"
                sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
                track_id = url.split("/")[-1].split("?")[-2]
                track_info = sp.track(track_id)
                print(track_info["name"])
                titulo_spotify = str(track_info["name"])
                titulo_spotify1 = titulo_spotify.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
                res = requests.get(track_info["album"]["images"][0]["url"], stream=True)
                with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                    shutil.copyfileobj(res.raw, out_file)
                with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                    img_data = img_file.read()
                    print("deu certo")
                results = Search(f"{track_info["name"]}, {track_info["album"]["artists"][0]["name"]}")
                if results.videos:
                    titulo = results.videos[0].title
                    print(titulo)
                    results.videos[0].streams.get_audio_only().download(output_path=diretorio_destino)
                    titulo_novo1 = titulo.replace("/", "").replace("|", "").replace("?", "").replace("*", "").replace("<", "").replace(">", "").replace(":", "").replace("\\", "")
                    sound = AudioSegment.from_file(f"{diretorio_destino}/{titulo_novo1}.m4a", format="m4a")
                    sound.export(f"{diretorio_destino}/{titulo_spotify1}.mp3", format="mp3")
                    audiofile = eyed3.load(f"{diretorio_destino}/{titulo_spotify1}.mp3")
                    if not audiofile.tag:
                        audiofile.initTag()
                    audiofile.tag.artist = track_info["album"]["artists"][0]["name"]
                    audiofile.tag.images.set(3, img_data, "image/jpeg")
                    audiofile.tag.save()
                    ("musica salva tanto como imagem e titulo")
                    os.remove(f"{diretorio_destino}/capa.jpg")
                    os.remove(f"{diretorio_destino}/{titulo_novo1}.m4a")
            else:
                print("Uso: tubedowloader <url> <mp3|mp4>")

if __name__ == "__main__":
    main()
