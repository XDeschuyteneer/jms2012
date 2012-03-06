#!/usr/bin/env python
# coding: utf-8

from HTMLParser import HTMLParser
from xml.dom.minidom import Document
import sys, glob

html_rep = r'../html/*'

in_out = {}
pr = 0
entrant = 1
sortant = 2

class Parser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attr):
        if tag == 'a':
            if (len(attr) == 1 
                and len(attr[0]) == 2 
                and attr[0][0] == "href"):

                link = attr[0][1]
                self.links.append(link)

class XMLCreator:

    def __init__(self):
        self.doc = Document()
        self.root = self.doc.createElement("pr")
        self.doc.appendChild(self.root)
    
    def add_site(self, nom_v, pr_v):
        site = self.doc.createElement("site")
        nom = self.doc.createElement("nom")
        pr = self.doc.createElement("page_rank")
        
        nom_value = self.doc.createTextNode(str(nom_v))
        pr_value = self.doc.createTextNode(str(pr_v))
        
        nom.appendChild(nom_value)
        pr.appendChild(pr_value)
        
        site.appendChild(nom)
        site.appendChild(pr)
        self.root.appendChild(site)

    def __str__(self):
        return self.doc.toprettyxml(indent="  ")
                
def path_to_nom(path):
    path = path.split('/')
    return path[len(path) - 1]

def parse(pages):
    nbr_pages = len(pages)
    for page in pages:
        nom = path_to_nom(page)
        in_out[nom] = [1. / nbr_pages, [], 0]
    for page in pages:
        nom = path_to_nom(page)
        file = open(page)
        parser = Parser()
        for ligne in file:
            parser.feed(ligne)
        for link in parser.links:
            in_out[nom][sortant] += 1
            in_out[link][entrant].append(nom)

def calcul_pr(default, entrant, s):
    page_rank = 0
    for site in entrant:
        s = in_out[site]
        s_pr = s[pr]
        s_l = s[sortant]
        page_rank += float(s_pr) / float(s_l)
    return page_rank

def afficher(mat):
    for ligne in mat:
        for elem in ligne:
            print elem,
        print

def prank():
    d = 0.85
    n = len(in_out)
    somme = (1. - d) / n

    sites = []
    for elem in in_out.keys():
        tmp = elem.split(".")
        if tmp[0] not in ("rank", "page_rank") and tmp[1] == "html":
            sites.append(elem)
    sites.sort()
    mat = [1] * len(sites)
    for i, elem in enumerate(mat):
        mat[i] = [i] * len(sites)
    for i, ligne in enumerate(mat):
        for j, elem in enumerate(ligne):
            input = in_out[sites[i]]
            output = in_out[sites[j]]
            a = 0.
            for k in output[1]:
                if k == sites[i]:
                    a += 1.
            b = 1. * len(output[1])
            mat[i][j] = a / b
    afficher(mat)



if __name__ == "__main__":
    args = []
    if len(sys.argv) >= 2:
        args = sys.argv[1:]
    else:
        args = glob.glob(html_rep)
    parse(args)
    xml = XMLCreator()
    for site in in_out:
        links = in_out[site]
        page_rank = calcul_pr(links[pr], links[entrant], links[sortant])
        xml.add_site(site, "pr: %.3f"%page_rank)
    to_add = '<?xml version="1.0" ?>\n<?xml-stylesheet href="rank.xsl" type="text/xsl"?>'
    out = "../../../../../html/rank.xml"
    fichier_out = open(out, "w")
    lines = str(xml).split("\n")
    fichier_out.write(to_add)
    fichier_out.write('\n'.join(lines[1:]))
    fichier_out.close()
    prank()
    
