#!/usr/bin/env python3  

import yt_dlp
import os
import eyed3
import requests
import os
import sys
import shutil
import subprocess
import pathlib
import mutagen.mp4

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
            ydl_opts = {
            'format': 'bestaudio/best',  # Baixa apenas o melhor áudio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Converte para MP3
                'preferredquality': '320', # Qualidade do áudio (ex: 320k)
            }],
            'outtmpl': f'{diretorio_destino}/oi.%(ext)s', # Nome do arquivo de saída
            'cachedir': False
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                artista = info_dict.get('uploader')
                thumbnail = info_dict.get('thumbnail')
                res = requests.get(thumbnail, stream=True)
                with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                    shutil.copyfileobj(res.raw, out_file)
                titulo = info_dict.get('title')
                titulo_novo = titulo.replace("/", ";").replace("|", "!").replace("?", "&").replace("*", "#").replace("<", "{").replace(">", "}").replace(":", ";").replace("\\", ";")
                caminho_arquivo = f"{diretorio_destino}/oi.mp3"
                with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                    img_data = img_file.read()
                music = eyed3.load(caminho_arquivo)
                music.tag.images.set(3, img_data, "image/jpeg")
                music.tag.artist = artista
                music.tag.save()    
                print("musica salva tanto como imagem e titulo")
                os.rename(f"{diretorio_destino}/oi.mp3", f"{diretorio_destino}/{titulo_novo}.mp3")
                os.remove(f"{diretorio_destino}/capa.jpg")
        elif ttipo == "mp4":
            ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Baixa o melhor vídeo e áudio mp4
            'outtmpl': f'{diretorio_destino}/oi.%(ext)s', # Nome do arquivo de saída
            'cachedir': False
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                artista = info_dict.get('uploader')
                titulo = info_dict.get('title')
                titulo_novo = titulo.replace("/", ";").replace("|", ";").replace("?", ";").replace("*", ";").replace("<", ";").replace(">", ";").replace(":", ";").replace("\\", ";")
                caminho_arquivo = f"{diretorio_destino}/oi.mp4"
                thumbnail = info_dict.get('thumbnail')
                res = requests.get(thumbnail, stream=True)
                with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                    shutil.copyfileobj(res.raw, out_file)
                with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                    img_data = img_file.read()
                video = mutagen.mp4.MP4(caminho_arquivo)
                video["\xa9ART"] = artista
                video["covr"] = [mutagen.mp4.MP4Cover(img_data, imageformat=mutagen.mp4.MP4Cover.FORMAT_JPEG)]
                video.save()
                os.rename(caminho_arquivo, f"{diretorio_destino}/{titulo_novo}.mp4")
                os.remove(f"{diretorio_destino}/capa.jpg")

    else:
        if sys.argv[1] == "config":
            diretoriodoarquivo = pathlib.Path(__file__).parent.resolve()
            print(f"abrindo o vscode na pasta: {diretoriodoarquivo}")
            os.system(f"code {diretoriodoarquivo}")
        else:
            print("Uso: tubedowloader <url> <mp3|mp4>")

if __name__ == "__main__":
    main()
