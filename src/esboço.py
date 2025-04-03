import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile, ZIP_DEFLATED

response = requests.get('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos')

#fazer condicional para verificar se a url é valida
#print(response.status_code)

site = BeautifulSoup(response.content, 'html.parser')

paragrafo = site.find('div', attrs = {'class':'cover-richtext-tile tile-content'})
lista = paragrafo.find_all('ol')
itens = lista[0].find_all('li')
anexoUm = itens[0].find('a')
anexoDois = itens[1].find('a')
#print(anexoDois['href'])

#lembrar de verificar retorno == 200 
pdfUm = requests.get(anexoUm['href'])
pdfDois = requests.get(anexoDois['href'])

pdf = open("anexoUm"+".pdf", 'wb')
pdf.write(pdfUm.content)
pdf.close()

pdf = open("anexoDois"+".pdf", 'wb')
pdf.write(pdfDois.content)
pdf.close()


arqZip = ZipFile("./anexos.zip", "w", compression = ZIP_DEFLATED)

arqZip.write("anexoUm.pdf")
arqZip.write("anexoDois.pdf")
arqZip.close()
