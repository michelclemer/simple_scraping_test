from os import walk

import requests
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import base64


class LINKWEB:
    def __init__(self, driver):

        # self.driver = driver
        self.driver = driver
        # driver = webdriver.Firefox()

        print("")

    def find_elem(self, locator, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(visibility_of_element_located(locator))
        return elem

    def run_find_click(self, locator):
        c = self.find_elem(locator)
        c.click()

    def run_find_write(self, locator, keys):
        self.find_elem(locator).clear()
        self.find_elem(locator).send_keys(keys)

    def get_value(self, locator):
        return self.find_elem(locator).get_attribute('href')

    def clear_field(self, locator):
        self.find_elem(locator).clear()

    def validar_url(self, url):
        if self.driver.current_url == url:
            return 1
        else:
            return 0


class PEGARLINK(LINKWEB):
    def __init__(self):
        self.logado = False
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": 'D:\Documentos\pandas',
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }, )
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', True)
        self.driver = webdriver.Chrome(executable_path=r"D:\Documentos\chrome\chromedriver.exe", options=chrome_options,
                                       desired_capabilities=capabilities)
        self.driver.maximize_window()
        super().__init__(self.driver)
        self.url = ''
        self.lista_url = []
        self.url_oficial = []
        self.link_baixado = {}
        self.dados_link_baixado = []
        self.links_mega = {}
        self.links_panda = {}
        self.todos_links_mega_panda = {}
        self.tipo_link = ''

    def link_download(self, url):
        response = requests.get(url)
        if response.history:

            for resp in response.history:
                if 'full' in str(resp.url):
                    return resp.url


        return 0

    def format_link(self,chave, url_page, tipo):

        if tipo == 'panda':
            for c, v in self.todos_links_mega_panda['panda'].items():
                nome = str(url_page).split(".")

                for n in nome:
                    if 'S' in str(n) and 'E' in str(n):
                        v.append(n)
                        return
        elif tipo == 'mega':
            for c, v in self.todos_links_mega_panda['mega'].items():
                if chave == c:
                    self.driver.get(url_page)
                    l = self.driver.current_url
                    v.append(l)
                    ep_t = self.format_links_mega(url_page)
                    print("EPS = ",ep_t)
                    if ep_t:
                        for i in ep_t:
                            v.append(i)


    """ Acessa a página e coleta todos os links codificados e adiciona em um dicionario """

    def list_all_links(self, url: str):
        """ Acessa pagina
        params: url = link para da página com os links do mega e panda
        return: None
        """
        self.driver.get(url)
        id = self.find_elem((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]')).get_attribute("id")
        div_content = self.find_elem((By.XPATH, f'//*[@id="{id}"]/div/div[2]')).get_attribute("outerHTML")
        soup = BeautifulSoup(div_content, 'lxml')
        count_p = 2
        for tag_p in soup.find_all('p'):
            if "MP4" in str(tag_p) and "DOWNLOAD" in str(tag_p):
                titulo = tag_p.span.text


                try:
                    p_body = self.find_elem(
                        (By.XPATH, f'//*[@id="{id}"]/div/div[2]/p[3]/span[{count_p}]')).get_attribute("outerHTML")
                    count_p += 1
                    parent = BeautifulSoup(p_body)
                    for a in parent.find_all('a'):
                        if '>PandaFiles<' in str(a):
                            pandas_string = []
                            if 'DUBLADO' in str(titulo):
                                pandas_string.append('DUBLADO')
                            if 'LEGENDADO' in str(titulo):
                                pandas_string.append('LEGENDADO')
                            if '480p' in str(titulo):
                                pandas_string.append('480p')
                            if '720p' in str(titulo):
                                pandas_string.append('780p')
                            self.links_panda[a['href']] = pandas_string

                        if '>Mega<' in str(a):
                            mega_string = []
                            if 'DUBLADO' in str(titulo):
                                mega_string.append('DUBLADO')
                            if 'LEGENDADO' in str(titulo):
                                mega_string.append('LEGENDADO')
                            if '480p' in str(titulo):
                                mega_string.append('480p')
                            if '720p' in str(titulo):
                                mega_string.append('780p')
                            self.links_mega[a['href']] = mega_string


                except:
                    print("Error titulo = ", titulo)
                    pass

        self.todos_links_mega_panda['panda'] = self.links_panda
        self.todos_links_mega_panda['mega'] = self.links_mega
        print("Dict = ", self.todos_links_mega_panda)


    """" Acessa cada link e decodifica em base64 para mostrar o verdadeiro link """

    def list_links_url(self):
        """" Acressenta dados ao dicionario de links
        params: None
        return:  None
        """
        if self.todos_links_mega_panda['panda']:
            for chave, valor in self.todos_links_mega_panda['panda'].items():
                link = self.link_download(chave)
                if link:
                    url = link.split("&")[1]
                    link_oficial = base64.b64decode(url[4:]).decode('utf-8')
                    print("Link-panda = ", link_oficial)
                    valor.append(link_oficial)
                    continue
        if self.todos_links_mega_panda['mega']:
            for chave, valor in self.todos_links_mega_panda['mega'].items():
                link = self.link_download(chave)
                if link:
                    url = link.split("&")[1]
                    link_oficial = base64.b64decode(url[4:]).decode('utf-8')
                    print("Link-mega ", link_oficial)
                    self.format_link(chave, link_oficial, 'mega')

                    continue



    "Alterar usuario e senha aqui"
    def get_info_ep_temp(self, link):
        for c, v in self.todos_links_mega_panda['panda'].items():
            if str(link) == str(v[2]):
                if self.logado == False:
                    self.driver.delete_all_cookies()
                    self.driver.get("https://pandafiles.com/login.html")
                    print("Fazedo login PandaFiles!")
                    self.run_find_write((By.XPATH, '//*[@id="loginpage"]/div[2]/form/div[1]/input'), 'usuario')
                    self.run_find_write((By.XPATH, '//*[@id="loginpage"]/div[2]/form/div[2]/input'), 'senha')
                    self.run_find_click((By.XPATH, '//*[@id="loginpage"]/div[2]/form/div[3]/input'))
                    self.logado = True
                self.driver.get(link)
                self.lista_url.append(self.driver.current_url)
                try:
                    self.find_elem((By.XPATH, '//*[@id="xfiles"]'))
                    table = self.find_elem((By.XPATH, '//*[@id="xfiles"]')).get_attribute("outerHTML")
                    soup = BeautifulSoup(table, 'lxml')
                    for item in soup.find_all('tr'):

                        if '.mp4' in str(item):
                            link_url = item.td.a['href']

                            l = str(link_url).replace('\r', '')
                            nome = str(l).split(".")

                            for n in nome:
                                if 'S' in str(n) and 'E' in str(n):
                                    v.append(n)

                                    break
                except:
                    titulo = self.find_elem((By.XPATH, '//*[@id="wrapper"]/div/div/div/div[1]')).text
                    print("Titulo ", titulo)
                    nome = str(titulo).split(".")

                    for n in nome:
                        if 'S' in str(n) and 'E' in str(n):
                            v.append(n)

                            break




    def download_video(self, link):
        if 'pandafiles' in str(link):
            self.get_info_ep_temp(link)
            #self.driver.get(link)
            # self.encode_panda()
        else:

            pass

    def download_pandas(self, link):
        self.run_find_click((By.XPATH, '//*[@id="downloadbtn"]'))
        self.run_find_click((By.XPATH, '//*[@id="direct_link"]/a'))
        self.format_link(link)

        self.link_baixado[link + self.resolucao] = list(dict.fromkeys(self.dados_link_baixado))
        self.resolucao = ''
        return

    "Alterar usuario e senha aqui"
    def pandaFiles(self, link):
        if self.logado == False:
            self.driver.delete_all_cookies()
            self.driver.get("https://pandafiles.com/login.html")
            print("Fazedo login PandaFiles!")
            self.run_find_write((By.XPATH, '//*[@id="loginpage"]/div[2]/form/div[1]/input'), 'usuario')
            self.run_find_write((By.XPATH, '//*[@id="loginpage"]/div[2]/form/div[2]/input'), 'senha')
            self.run_find_click((By.XPATH, '//*[@id="loginpage"]/div[2]/form/div[3]/input'))
            self.logado = True
        self.driver.get(link)
        if not self.count_ep():
            self.format_link(link, 'panda')

        else:
            table = self.find_elem((By.XPATH, '//*[@id="xfiles"]')).get_attribute("outerHTML")
            soup = BeautifulSoup(table, 'lxml')
            for item in soup.find_all('tr'):
                if '.mp4' in str(item):
                    l = item.td.a['href']
                    print("Link = ", l)
                    self.driver.get(l)
                    self.format_link(l)
                    self.download_pandas(l)

    def count_ep(self):
        try:
            self.find_elem((By.XPATH, '//*[@id="xfiles"]'))
        except:
            print("Tabela não encontrada!")
            print("Seguindo para download!")
            return 0
        table = self.find_elem((By.XPATH, '//*[@id="xfiles"]')).get_attribute("outerHTML")
        soup = BeautifulSoup(table, 'lxml')
        for item in soup.find_all('tr'):
            if '.mp4' in str(item):
                l = item.td.a['href']
                print("Link = ", l)
                self.driver.get(l)
                self.format_link(l)
                self.download_pandas(l)
        return 1

    def encode_panda(self):
        import os
        filenames = next(walk(r'D:\Documentos\pandas'), (None, None, []))[2]

        if filenames:
            for f in filenames:
                os.remove("D:\Documentos\pandas" + '\{}'.format(f))

        print("Arquivos removidos")

    # MEGA

    def format_links_mega(self, link):
        self.driver.get(link)
        time.sleep(5)
        content = self.find_elem((By.XPATH, '/html')).get_attribute('outerHTML')
        time.sleep(5)
        soup = BeautifulSoup(content, 'lxml')
        self.lista_url.append(self.driver.current_url)
        eps = []
        spans = soup.find_all('span')
        for span in spans:

            if '.Club' in str(span.text):

                nome = str(span.text).split(".")
                for n in nome:
                    if 'S' in str(n) and 'E' in str(n):
                        eps.append(n)

        return eps


    def download_mega(self, link):
        self.driver.get(link)
        eps = self.find_elem((By.XPATH, '//*[@id="fmholder"]/div[4]/div[1]/div[5]/div[30]/div[1]/div')).get_attribute(
            'outerHTML')
        soup = BeautifulSoup(eps, 'lxml')
        quantidade_arquivos = 0
        for a in soup.find_all('a'):
            print("Mega ", a.text)
            quantidade_arquivos += 1
        self.quatidade_links_mega = quantidade_arquivos

    def download_mega_video(self, name_link):
        print("Baixando videos MEGA = ", name_link)

        import os
        filenames = next(walk(r'D:\Documentos\megacmd'), (None, None, []))[2]
        print(filenames)
        if filenames:
            for f in filenames:
                os.remove("D:\Documentos\megacmd" + '\{}'.format(f))

        print("Arquivos removidos")
        os.system(fr"C:\Users\itall\AppData\Local\MEGAcmd\MEGAclient.exe get {name_link} D:\Documentos\megacmd --ignore-quota-warn")

