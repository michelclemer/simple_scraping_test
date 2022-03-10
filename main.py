import time

from pegar_link.Link import PEGARLINK
from download_files.encode_content import ENCODE_FILE

class CONTROL_ENCODE_FILE:
    def __init__(self, link):
        self.link = link
        self.tipo_atual = []
        self.pegar_link = PEGARLINK()
        self.encode_file = ENCODE_FILE()

    def get_all_link(self):
        self.pegar_link.list_all_links(self.link)
        self.pegar_link.list_links_url()


    def run_get_links(self):

        for link in self.pegar_link.lista_url:
            print("Link: ", link)
            link_ofc = str(link)
            try:
                self.pegar_link.download_video(link_ofc)
            except:
                print("Error link -> ", link)
                pass
            print("Executando encode")
        print(self.pegar_link.todos_links_mega_panda)
            #self.encode_file.format_folder(link, self.pegar_link.tipo_link)
    def run_encode_videos(self):
        for chave, valor in  self.pegar_link.todos_links_mega_panda['mega'].items():
            for i in valor:
                if "http" in str(i):
                    self.pegar_link.download_mega_video(i)
                    print("[+] Mega Baixado!")

                    print("Executando Encode..")
                    self.encode_file.format_folder(i, 'mega')
                    time.sleep(10)






app = CONTROL_ENCODE_FILE("https://baixarseriesmp4.club/baixar-firebite-1a-temporada-mp4-legendado/")
app.get_all_link()
app.run_get_links()
app.run_encode_videos()

