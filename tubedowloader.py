#!/usr/bin/env python3

import yt_dlp
import os
import eyed3
import requests
import sys
import shutil

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        diretorio_destino = "/home/isaac/Downloads"
        ydl_opts = {
            'format': 'bestaudio/best',  # Baixa apenas o melhor áudio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Converte para MP3
                'preferredquality': '320', # Qualidade do áudio (ex: 192k)
            }],
            'outtmpl': f'{diretorio_destino}/oi.%(ext)s', # Nome do arquivo de saída
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            artista = info_dict.get('uploader')
            thumbnail = info_dict.get('thumbnail')
            res = requests.get(thumbnail, stream=True)
            with open(f"{diretorio_destino}/capa.jpg", 'wb') as out_file:
                shutil.copyfileobj(res.raw, out_file)
            titulo = info_dict.get('title')
            caminho_arquivo = f"{diretorio_destino}/oi.mp3"
            with open(f"{diretorio_destino}/capa.jpg", 'rb') as img_file:
                img_data = img_file.read()
            music = eyed3.load(caminho_arquivo)
            music.tag.images.set(3, img_data, "image/jpeg", u"cover")
            music.tag.artist = artista
            music.tag.save()
            os.rename(caminho_arquivo, f"{diretorio_destino}/{titulo}.mp3")
            os.remove(f"{diretorio_destino}/capa.jpg")
            print(f"Artista: {artista} e titulo: {titulo}")
    else:
        print("Uso: python tubedowloader.py <URL do YouTube>")

if __name__ == "__main__":
    main()