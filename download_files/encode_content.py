import os
from os import listdir
from os.path import isfile, join

class ENCODE_FILE:
    def __init__(self):
        self.nomes_arquivos = {}

    def execute_encode(self, file_name, tipo: str):
        if tipo == 'mega':
            os.system(r"D:\Documentos\StaxRip-v2.10.0-x64\StaxRip_x64_1.3.4.0_stable\StaxRip.exe -template:ENCODER D:\Documentos\megacmd\01\{} -encode -exit".format(file_name))
            print("Encoder Mega")
        elif tipo == 'panda':
            os.system(r"D:\Documentos\StaxRip-v2.10.0-x64\StaxRip_x64_1.3.4.0_stable\StaxRip.exe -template:ENCODER D:\Documentos\pandas\{} -encode -exit".format(file_name))
            print("Encoder Panda")
    def verificar_pasta(self):
        onlyfiles = [f for f in listdir(r'D:\Documentos\megacmd\01') if isfile(join(r'D:\Documentos\megacmd\01', f))]
        return onlyfiles


    def format_folder(self, link, tipo):
        resolucao = ''
        dados_link_baixado = []
        arquivos = self.verificar_pasta()
        for l in arquivos:
            for name in l.split('.'):
                if 'S' in str(name) and 'E' in str(name):
                    dados_link_baixado.append(name)
                if '720p' in str(name):
                    dados_link_baixado.append('720p')
                if 'LEG' in str(name):
                    dados_link_baixado.append('LEGENDADO')
                if 'DUB' in str(name):
                    dados_link_baixado.append('DUBLADO')
            if '720p' not in str(l):
                dados_link_baixado.append('480p')
                resolucao = '.480p'

            self.execute_encode(l, tipo)

        self.nomes_arquivos[link+resolucao] = dados_link_baixado


#app.execute_encode('20211223185538.mp4')