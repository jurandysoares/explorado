#!/usr/bin/env python3
# profredes.py
# This file is part of Explorado
#
# Copyright (C) 2020 - Jurandy Soares
#
# Explorado is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Explorado is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Explorado. If not, see <http://www.gnu.org/licenses/>.
#

import bs4
import requests

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
        self.nome,self.sobrenome = titulo.lower().split()
        self.email = self._get_email()
        self._id = self.email.split('@')[0]
        self.campus = campus_abrev.get(abr_campus, 'Desconhecido')

    def __str__(self):
        return f'{self.titulo} <{self.email}>'

    def __repr__(self):
        return f'{self.titulo} <{self.email}>'

    def _get_email(self) -> str:
        pag_prof = requests.get(self.site).content
        anal_pag = bs4.BeautifulSoup(pag_prof, 'html.parser')
        res_buscas = anal_pag.find_all('li', {'class': 'info-email'})
        return res_buscas[0].a.text.strip()


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
        professores[novo_professor._id] = novo_professor

if __name__ == "__main__":
    principal()
