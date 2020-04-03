import bs4
import requests
from slugify import slugify

campus_abrev = {
    'apodi': 'Apodi',
    'caico': 'Caicó',
    'canguaretama': 'Canguaretama',
    'curraisnovos': 'Currais Novos',
    'educacaoadistancia': 'Educacão a distância',
    'ipanguacu': 'Ipanguaçu',
    'joaocamara': 'João Câmara',
    'macau': 'Macau',
    'mossoro': 'Mossoró',
    'natalcentral': 'Natal-Central',
    'natalzonanorte': 'Natal-Zona Norte',
    'novacruz': 'Nova Cruz',
    'parnamirim': 'Parnamirim',
    'paudosferros': 'Pau dos Ferros',
    'santacruz': 'Santa cruz',
    'saogoncalo': 'São Gonçalo do Amarante',
    }

class Professor:
    def __init__(self, titulo, site, abr_campus):
        self.titulo = titulo
        self.site = site
        uri = site.rsplit('/', maxsplit=1)[-1]
        nome,sobrenome = titulo.lower().split()
        slug_nome = uri[slice(len(nome))]
        slug_sobrenome = uri[slice(len(nome), len(uri))]
        self.id = f'{slug_nome}.{slug_sobrenome}'
        self.email = f'{self.id}@ifrn.edu.br'
        self.campus = campus_abrev.get(abr_campus, 'Desconhecido')

    def __str__(self):
        return f'{self.titulo} <{self.email}>'

    def __repr__(self):
        return f'{self.titulo} <{self.email}>'


URL = 'http://docentes.ifrn.edu.br/'

def principal():
    req = requests.get(URL)
    sopa = bs4.BeautifulSoup(req.text, 'html.parser')
    global resultados
    resultados = sopa.find_all('li', {'class': 'redesdecomputadores'})
    global professores
    professores = {}
    for res in resultados:
        abr_campus = res.attrs['class'][1]
        enlace = res.find_all('a')[0]
        novo_professor = Professor(titulo=enlace['title'],
                                   site=enlace['href'],
                                   abr_campus=abr_campus)
        professores[novo_professor.id] = novo_professor

if __name__ == "__main__":
    principal()
