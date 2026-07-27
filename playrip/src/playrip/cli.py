from playrip import Dowload
import sys
import os

directorio = os.path.expanduser("~/Downloads")

def main():
    url = sys.argv[1]
    if("youtu" in url):
        print("\n------Abaixando video do Youtube------")
        if(len(sys.argv) > 2):
            tipo = sys.argv[2]
            try:
                directorio = sys.argv[3]
            except IndexError:
                print("ola não tem diretorio")
            if(directorio != None and "~" in directorio):
                Dowload.Youtube(url=url, formato_do_audio=tipo, thumbnail=True, diretorio_destino=os.path.expanduser(directorio))
            else:
                if(os.path.isdir(directorio)):
                    Dowload.Youtube(url=url, formato_do_audio=tipo, thumbnail=True, diretorio_destino=directorio)
                else:
                    print("\npasta não achada")
                    return
    elif("spotify" in url):
        print("\n------Abaixando musica do spotify------")
        try:
            directorio = sys.argv[2]
        except IndexError:
            directorio = "~/Downloads"
        if("~" in directorio):
            directorio = os.path.expanduser(directorio)
            if(not os.path.exists(directorio)):
                print("pasta não achada")
                return
            else:
                Dowload.Spotify(url=url,thumbnail=True, diretorio_destino=os.path.expanduser(directorio))
        else:
            if(os.path.isdir(directorio)):
                Dowload.Spotify(url=url,thumbnail=True, diretorio_destino=directorio)
            else:
                print("pasta não achada")
                return
    else:
        print("\npf coloque um link no spotify ou youtube\n")
        return