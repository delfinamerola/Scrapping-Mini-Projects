import requests
from bs4 import BeautifulSoup
from IPython.display import Image


def getSite(url):
    p12 = requests.get(url)
    s = BeautifulSoup(p12.text, 'lxml')
    secciones = s.find('ul', attrs={'class':'hot-sections'}).find_all('li')

    links_secciones = [seccion.a.get('href') for seccion in secciones]
    titles_secciones = [seccion.a.get_text() for seccion in secciones]

    return links_secciones, titles_secciones


def get_articles(link_seccion):
    try: 
        seccion = requests.get(link_seccion)
        pagina_seccion = BeautifulSoup(seccion.text, 'lxml')        
        lista_notas = []
        featured_article = pagina_seccion.find('div', attrs = {'class':'featured-article__container'})
        if featured_article.a:
            lista_notas.append(featured_article.a.get('href'))
        articles_list = pagina_seccion.find('ul', attrs = {'class':'article-list'})
        for article in articles_list.find_all('li'):
            if article.a:
                lista_notas.append(article.a.get('href'))
        
        return lista_notas
    except: 
        print('Error while getting this section')
        return None

def get_info(url_nota):
    informacion = {}
    nota = requests.get(url_nota)
    if nota.status_code == 200:
        s_nota = BeautifulSoup(nota.text, 'lxml')
        #Extraigo titulo
        titulo = s_nota.find('h1', attrs = {'class':'article-title'})
        if titulo:
            informacion['titulo'] = titulo.text
        else:
            informacion['titulo'] = None

        #Extraer fecha
        fecha = s_nota.find('span', attrs = {'pubdate':'pubdate'}).get('datetime')
        if fecha:
            informacion['fecha'] = fecha
        else:
            informacion['fecha'] = None

        #Extraer volanta
        volanta = s_nota.find('h2', attrs = {'class':'article-prefix'})
        if volanta:
            informacion['volanta'] = volanta.text
        else:
            informacion['volanta'] = None

        #Extraer copete
        copete = s_nota.find('div', attrs = {'class':'article-summary'})
        if copete:
            informacion['copete'] = copete.text
        else:
            informacion['copete'] = None

        #Extraer imagen
        media = s_nota.find('div', attrs = {'class':'article-main-media-image'})
        if media:
            imagenes = media.find_all('img')
            if len(imagenes) == 0:
                print('No se encontraron imagenes')
            else:
                imagen = imagenes[-1]
                imagen_src = imagen.get('data-src')
                try:
                    img_req = requests.get(imagen_src)
                    if img_req.status_code == 200:
                        informacion['imagen'] = Image(img_req.content)
                    else:
                        informacion['imagen'] = None
                except:
                    print('No se pudo obtener la imagen')

        else:
            print('No se encontro media') 

        #extraer cuerpo
        cuerpo = s_nota.find('div', attrs = {'class':'article-text'})
        if cuerpo:
            informacion['cuerpo'] = cuerpo.text
        else:
            informacion['cuerpo'] = None   
    else: 
        print('No se pudo obtener informacion')
    return informacion         
    
    
def main(url):
    #traigo los links y titulos de cada seccion
    links_sec, titulos_sec = getSite(url)
    for i in range(len(links_sec)):
        print(f'Seccion: {titulos_sec[i]}')
        try:
            lista_notas = get_articles(links_sec[i])
            #imprimo los links
            print(lista_notas)
            featured_article = lista_notas[0]
            #de cada seccion traigo los datos del articulo principal
            info_featured_article = get_info(featured_article)
            print(info_featured_article)
        except Exception as e:
            print('Error')
            print(e)
            print('\n')
    
if __name__ == "__main__":
    url = 'https://www.pagina12.com.ar/'
    main(url)








        