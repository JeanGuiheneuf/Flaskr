# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import random
import os.path
import pickle


def fichierverbes():
    fin= open('Notes selectionnées.txt','r')
    cartes = fin.readlines()
    verbes = cartes[1::2]
    fout = open('Verbes.txt','w')
    for i in verbes:
        fout.write(i)

def traduire(Phraseatraduire):
    # Scrapping de deepl pour traduire les phrases d'exemples.
    urldeepl = "https://www.deepl.com/translator#fr/es/"
    #< div; id = "target-dummydiv"class ="lmt__textarea lmt__textarea_dummydiv" > Hola < / div >

    """url = ''.join([urldeepl, Phraseatraduire])
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    time.sleep(5)

    traductionbrut = soup.find(id="target-dummydiv")
    print(traductionbrut)
    print(traductionbrut.text.strip())  # Press Ctrl+F8 to toggle the breakpoint."""

    opts = Options()
    opts.set_headless()
    assert opts.headless  # Operating in headless mode
    browser = Firefox(executable_path=r'C:\Users\Jean\Downloads\geckodriver-v0.29.0-win64\geckodriver.exe', options=opts)


    browser.get('https://www.deepl.com/translator#fr/es')
    search_form = browser.find_element_by_class_name('lmt__textarea lmt__source_textarea lmt__textarea_base_style')

    #class ="lmt__textarea lmt__source_textarea lmt__textarea_base_style"
    search_form.click()
    search_form.clear()
    search_form.send_keys('Bonjour')
    search_form.submit()
    results = browser.find_elements_by_id('target-dummydiv')
    print(results)

    browser.close()
    quit()

def createcsv():
    f = open('verbitos.csv', "w")
    f.write("verbe, traduction, présent,yo,tu,ella,nosotros,vosotros,ellos")
    f.close()
def addVerbs(verbslist):
    f = open('verbitos.csv','a')
    for verb in verbslist:
        if verb not in f.readlines():
            continue

def sraping_conjugaisons(verbe):
    baseurl = "https://la-conjugaison.nouvelobs.com/espagnol/verbe/"
    url = baseurl + verbe + ".php"
    page = requests.get(url)
    print(verbe)

    soup = BeautifulSoup(page.content, "html.parser")
    #Traduction du verbe
    traductionbloc = soup.find('div', {'class': 'bloc b t22'})
    try:
        traduction = traductionbloc.a.get_text()
    except AttributeError:
        traduction = "Pas de traduction disponible"
    #print(traduction)
    #Temps de conjugaison
    try:
        verbetypebloc = soup.find('div', {'class': 'bloc'}).text
    except AttributeError:
        print("Verbe",verbe, "introuvable.")
        return
    verbetype = verbetypebloc.split()[1]
    #print(verbetype)
    tempsblocs = soup.find_all('div', {'class': 'tempstab'})

    #seulement le présent pour commencer
    #print(tempsblocs[1].text)
    present = tempsblocs[0].text
    a = present.split(")",1)
    temps = a[0]+')'
    #conjugaisons:
    conjugaisonsbrutes = a[1]
    pronombres = ['yo', 'tú','él','nosotros','vosotros','ellos']
    for i in pronombres:
        try:
            conjugaisonsbrutes = conjugaisonsbrutes.replace(i,'/',1)
        except:
            pass
    #print(conjugaisonsbrutes)
    conjugaisons = conjugaisonsbrutes.split('/')
    conjugaison = [b.replace('  ',' ').lstrip() for b in conjugaisons if b!='']
    #print(conjugaison)
    verbpackage = [temps, traduction, verbetype, conjugaison]

    dicoverbes[verbe] = verbpackage
    #print(dicoverbes)

def quizz(dicoverbes, iterations):
    liste= [*dicoverbes]
    pronoms = ['yo', 'tú', 'él/ella', 'nosotros', 'vosotros', 'ellos/ellas']
    bonneréponses = 0
    for i in range(iterations):
        verbe = random.choice(liste)
        id_conjugaison = random.choice([0,1,2,3,5]) # 0 pour yo, 2 pour él etc...
        conjugaison = dicoverbes[verbe][3][id_conjugaison]

        print('-----------------------------')
        print(str(i+1)+'/'+str(iterations),verbe," - ", dicoverbes[verbe][1])
        print(dicoverbes[verbe][0],"   ",'verbe',dicoverbes[verbe][2])
        #print(pronoms[id_conjugaison])
        input(" ".join([pronoms[id_conjugaison],"..."]))

        validation = input("--".join([conjugaison,"Avez-vous saisis la bonne réponse ? o/n"]))
        if validation=='o':
            print('bien ouej frérot')
            bonneréponses+=1
        else:
            print('Tu nous as habitué à mieux frérot')
    print(bonneréponses,"bonnes réponse sur",iterations)
    if bonneréponses>9:
        print("ça se tient")
    elif bonneréponses>5:
        print("pas mal mais un peu la lose quand même")
    else:
        print('NUL NUL NUL')
        print('NUUUUUUUUUUUUL !')




liste_temps=['pres',
             'pret_perf_comp',
             'pret_imp',
             'pret_plus',
             'pret_perf_simp',
             'pret_ant',
             'fut',
             'fut_perf',
             'cond',
             'cond_perf',
             'sub_pres',
             'sub_pret_perf',
             'sub_pret_imp1',
             'pret_plus1'
             'sub_pret_imp2',
             'pret_plus2'
             'sub_fut',
             'sub_fut_perf']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if os.path.exists('dicoverbes')==False:
        if os.path.exists('Verbes.txt')== False:
            fichierverbes()

        f = open('Verbes.txt', 'r')

        listeverbes = []
        #print(f.readlines())
        for verbe in f.readlines():
            listeverbes.append(verbe.strip())
        print(listeverbes)


        dicoverbes = {}
        #listeverbes = ["volcar","volar","construir"]
        for verbe in listeverbes:
            sraping_conjugaisons(verbe)
        d = open('dicoverbes','wb')
        pickle.dump(dicoverbes,d)
    else:
        e = open('dicoverbes','rb')
        dicoverbes = pickle.load(e)
    print(dicoverbes)
    quizz(dicoverbes,10)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
