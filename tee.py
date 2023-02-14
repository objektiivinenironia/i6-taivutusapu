# coding=utf-8
import xml.etree.ElementTree as ET
import sys 
import argparse
import re # haetaan nro syötteestä
import difflib

tree = ET.parse('kotus-sanalista_lyh.xml')
root = tree.getroot()

# argparse: args.monikko True = monikko (m=5) / False == yksikkö 
# monikko ja yks (esim. "nakit ja muusi") ei toimi samassa nimessä (puklu)
# syöte täytyy antaa yksikössä anyway "nakki ja muusi"
# paras olisi jos voisi antaa "nakit ja muusi" ja tämä osaisi etsiä "nakki"
# ja tehdä siitä monikon. "nak/it ja muusi/" 
# annetaan -m kun halutaan monikko
# - input pienillä kirjaimilla?

parser = argparse.ArgumentParser(description='tulosta jotain')
parser.add_argument('-m', required = False, action='store_true',
                    dest = 'monikko',
                    help='tulosta monikko')

parser.add_argument('-r', required = False, action='store_true',
                    dest = 'rajoita',
                    help='rajoita syötettä')


parser.add_argument('-d', required = False, action='store_true',
                    dest = 'debug',
                    help='*debug*')

parser.add_argument('-n', required = False, action='store_true',
                    dest = 'nee',
                    help='tulosta vain taivutukset, ei koodia')

parser.add_argument('-e', required = False, action='store_true',
                    dest = 'eidiff',
                    help='ei difflib close match')

parser.add_argument('text', action='store', type=str)

args = parser.parse_args()
#print(args.monikko)
#print(args.text)


vokaalit = 'a', 'e', 'i', 'o', 'å', 'u', 'y', 'ä', 'ö'

def debug(tulosta):
        if args.debug == True:
                print(tulosta)

# syöte 
def _main_():
        
        #input_value = _input_()
        input_value = args.text        
        # pienet kirjaimet?
        # ei välttämättä! Esim: AIDS
        #input_value = input_value.lower()
        lst = input_to_lst(input_value)

        n_sanat = len(lst)
        # laskuri t        
        t = 0

        # nominatiivilista (plus jakaja "/" at offset?)
        # monikko nom tehdään yks genetiivistä
        nom_lst = []
        #sanojen alku ennen av 
        # ts taipumaton osa
        alku_lst = []
        
        gen_lst = []
        par_lst = []
        ess_lst = []
        ill_lst = []
        # vain monikko
        ine_lst = []

        # info-tulostusta... varten: tulosta_nayte()
        tn_lst = []
        av_lst = []
        sanak_lst = []
        
        # monikko?
        if args.monikko == True:
                m = 5
        else:
                m = 0
        
        while n_sanat > t:

                sana = lst[t]
                # "perse48" ei tule tänne (E: lst out of range)
                # "perse48 perse" tulee tänne ja sanoo:
                #   sana = lst[t]? n: 48 , t: 1 , len: 2
                #print("sana = lst[t]? n:",n_sanat,", t:",t,", len:", len(lst))
                #onko syötteessä annettu taivutustietoja? tn av esim "kissa11a"
                #jos on, re_ palauttaa luvun (tn) ja kirjaimen nro:n jälkeen (av?)
                #poistaa nrot ja merkit nro:n jälkeen ja palauttaa muokatun sanan
                annettu = [0,0]
                #annettu = []
                # onko sanassa numeroita?
                if True in [char.isdigit() for char in sana]:
                        #print("JOO!")
                        annettu = re_(sana)
                        sana = poista_nro_ja_loppu(sana)
                        
                #else:
                        #print("EI!")
                #print("ANNETTU:", annettu, "len:",len(annettu))
                #print(annettu[0], annettu[1])
                n = annettu[0]
                a = annettu[1]        
                
                #if len(sana_tn_av) > 1:
                #        sana = sana_tn_av[0] 
                #        tn = sana_tn_av[1]
                #        av = sana_tn_av[2]
                #        print("SYÖTTEESSÄ T-TIETOJA:", sana, tn, av)

                taivutuslistat = []

                # jos ei annettu syötteessä n, se on 0

                # tn on taivutusnro!
                taivutuslistat = tee_taivutuslistat(sana,n,a)

                t_lista = taivutuslistat[0] # t lista
                a_lista = taivutuslistat[1] # a lista
                # tn on taivutusnro!
                tn = taivutuslistat[2]

                # info-tulostus tulosta_nayte
                av = taivutuslistat[3]

                # info-tulostus av ja sanak tulosta_nayte varten
                tn_lst.append(tn)
                if av == 0:
                        av_lst.append("-")
                else:
                        av_lst.append(av)
                        
                sanak_lst.append (taivutuslistat[4])  

                #t_lista = muokkaa_lista(sana, t_lista, a_lista, tn)
                # muokkaa_lista
                
                t_lista = muokkaa_lista(sana, a_lista, tn)          
          


                
                offset = t_lista[m]
                #print("OFFSET", offset)
                
                # tarvitaan myös (taipumattoman) alkuosan pituus
                # monikossa
                #print("offset:", offset)
             
                if len(a_lista) > 0:
                        gen_lst.append(a_lista[m+1]+t_lista[m+1])
                        par_lst.append(a_lista[m+2]+t_lista[m+2])
                        ess_lst.append(a_lista[m+3]+t_lista[m+3])
                        ill_lst.append(a_lista[m+4]+t_lista[m+4])
                        ine_lst.append(a_lista[m+5]+t_lista[m+5])
                else:
                        gen_lst.append(t_lista[m+1])
                        par_lst.append(t_lista[m+2])
                        ess_lst.append(t_lista[m+3])
                        ill_lst.append(t_lista[m+4])
                        ine_lst.append(t_lista[m+5])
                        
                #print("a_lista:", a_lista)
                #print("t_lista:", t_lista)

                # tehdään positiivinen offset
                offset = len(sana)+offset
                
                # alku_lst[]: kaappi = kaap, perse = perse
                alku_lst.append(sana[:offset])
 
                # monikko? -- nominatiivi
                # ...jos tulee samaan listaan yks ja mon,
                # tämä ehkä toimii?
                if m > 0:

                        # mon nom on yks. gen.
                        # onko ao ehto turha?
                        if a_lista:
                                #temp_offset = len(sana)+a_lista[0]
                                # 0 on yksikkö
                                temp_offset = len(sana)+t_lista[0] 
                                temp_gen_mjono = a_lista[1]+t_lista[1]
                        else:
                                temp_offset = len(sana)+t_lista[0]
                                temp_gen_mjono = t_lista[1]
                                
                        temp_gen_mjono = sana[:temp_offset]+temp_gen_mjono
                        temp_alku = temp_gen_mjono[:offset]
                        temp_loppu = temp_gen_mjono[offset:]

                        mjono = temp_alku+"/"+temp_loppu[:-1]+"t"
                                                 
                        
                        nom_lst.append(mjono)
                        
                        #END monikko
                else:
                        nom_lst.append(sana[:offset]+"/"+sana[offset:])
                               
                t+=1 
        
        tulosta_nayte(m, lst, tn_lst, av_lst, sanak_lst, alku_lst, nom_lst, gen_lst, par_lst, ess_lst, ill_lst, ine_lst)
        # nee: kun halutaan diff helpommin,
        # tulostetaan vain välttämätön
        if args.nee == False:
                tulosta(m, nom_lst, gen_lst, par_lst, ess_lst, ill_lst, ine_lst)
        
        
def tulosta_nayte(m, lst, tn_lst, av_lst, sanak_lst, alku_lst, nom_lst, gen_lst, par_lst, ess_lst, ill_lst, ine_lst):

        if m > 0:
                m = "m"
        else:
                m = "y"
        
        at = 0
        while at < len(alku_lst):
                # infolistat
                if args.debug:
                        print(lst[at]+" ['"+sanak_lst[at]+"'", tn_lst[at], av_lst[at], "("+m+")"+"]")
                # taivutusnäyte
                print(" "+alku_lst[at]+gen_lst[at])
                print(" "+alku_lst[at]+par_lst[at])
                print(" "+alku_lst[at]+ess_lst[at])
                print(" "+alku_lst[at]+ill_lst[at])
                # vain monikoille ine
                if m == "m":
                        print(" "+alku_lst[at]+ine_lst[at])
                at+=1
        
        
def tee_taivutuslistat(sana,tn,av):

        #tiedot = [0,0]

        #print("tee_taiv... av", av)
        # syötteessä esim "pallo5B"
        if tn > 0:
                
                t = mallipaate(sana, tn)
                a = uusin_astevaihtelu(sana, av)
                return t,a,tn,av,sana 

        # maks yksitt hakusanan pituus
        max_input_mjono = 9
        if  max_input_mjono > len(sana):
                hakusana = sana
        else:
                lyhennys = len(sana) - max_input_mjono
                hakusana = sana[lyhennys:]

        #print ("HAKUSANA:",hakusana)
        tiedot=[]
        tiedot = hae_kotus(hakusana)
        #print(tiedot)
        #print("tiedot[1]", tiedot[1])
        # derohaku jos ei löydy 1:1 
        if tiedot == False:
                tiedot=[]
                tiedot = hae_dero_kotus(hakusana)
                #s = tiedot[2]
                #print("DERO",tiedot)
                
        #else:
                #tiedot = hae_kotus(sana, 'tn', 'av')
                #s = hae_...

        tn = tiedot[0]
        av = tiedot[1]
        s = tiedot[2]
  
        if tn == 0:
                tn = 0
        tn = int(tn)

        #print ("tee_astev..", tn, av)
        
        t = mallipaate(sana, tn)
        a = uusin_astevaihtelu(sana, av)
         
        return t,a,tn,av,s 
#  t, a ja av_tyyppi on listoja

def uusin_astevaihtelu(sana, av):

        av_lista = ks_av_tyyppi(sana, av)
        
        return av_lista

# aiempi versio taydenna_t löytyy vanha.py vertailun vuoksi) 
def muokkaa_lista(sana, a_lista, tn):

        # monikko?
        mon = args.monikko;
        
        # lista skippaa offsetit
        yks_ja_mon_lst = [1,2,3,4,6,7,8,9,10]

        # offset muokataanko? 1 tarkoittaa että ei.
        # (offset on 0 tai negatiivinen) 
        offset_y = 1
        offset_m = 1
        
        # kun tämä lippu False, ei fiksata (lisätä) vokaaleja
        fix_loppu = True
        fix_mon_loppu = True
                       
        # vokaaliharmonia: ä=etuvokaali, a=takavokaali
        vok_var = vokaalih(sana)
        
        # korvataan ed. perusteella O -> o tai ö
        #O = 'o'
        #if vok_var == 'ä':
        #        O = 'ö'
          
        
        # vokaalimuuntelua?
        # temp! esim: opas oppAAn
        
        # vok pidentymä?
        vok_pid = ""
        if sana[-1] in vokaalit:
                vok_pid = sana[-1]
        else:
                if sana[-2] in vokaalit:
                        vok_pid = sana[-2]

        v = vok_pid

        # 1-4 vok loppuisia
        #valo/ #häly aurinko !
        if tn == 1:
                malli = "valo"
                t_lista = [0, "n", "a", "na", v+"n",
                           0, "jen", "ja", "ina", "ihin", "issa" ]
                
        # palvelu/
        if tn == 2:
                malli = "palvelu"
                t_lista = [0, "n", "a", "na", v+"n",
                           0, "jen", "ja", "ina", "ihin", "issa"] 
        #valtio/
        if tn == 3:
                malli = "valtio"
                t_lista = [0, "n", "ta", "na", v+"n",
                           0, "iden", "ita", "ina", "ihin", "issa"]
        
        #laatik/ko ! (av+tämä) A+4: o+n ko ko+na ko+on
        #laatik
        #laatik k o
        #eli kk_k
        #esim tänne tulee +"o"
        #laatik
        #oikeasti pitäis pätkäistä av:n mukaan
        #laati/kk_k
        #ja eikö myös hämää että että av tulee kuin tyhjästä?
        #ts jos tn 4 malli on av A kk_k
        #eikö se pitäisi näkyä täällä tai (sitä) kutsua täältä?
        #(siis tn 4 aina astevaihtelun kanssa?)
        #mut ei me välitetä!
        if tn == 4:
                malli = "laatikko"
                t_lista = [-2, "n", "a", "na", v+"n",
                           -2, "jen", "ja", "ina", "ihin", "issa"]
        # 5-7 i-loppuisia
        # risti 5 esim tuoli, pyykki (A) OFFSET -1 koska monikko!
        #risti/ ... rist/i (? monikko) zen/
        if tn == 5:
                malli = "risti"
                # voiko i olla muu vokaali? 
                # i voisi olla nimeltään v ja se voisi olla ylhäällä
                # ts tässä geneerinen mikä tahansa?
                i = ""
                # jos lop. konsonantti esim "zen"
                if sana[-1] not in vokaalit: 
                        i = "i"
                        offset_m = 0
                else:
                        fix_mon_loppu = False

                
                if sana in ["tunti"]:
                        i = "i"
                        fix_loppu = False
                
                t_lista = [0, i+"n", i+"ä", i+"nä", i+"in",
                           -1, "ien", "ejä", "einä", "eihin", "eissä"]

                #if mon and a_lista == pp_p:
                #tunti mon ei toimi
                #if mon and a_lista in [pp_p, nt_nn]:
                #        fix_loppu = False
                        
                # tarvitaanko fix_loppu? (lisätään vokaali koska adhoc)
                # esim "takki" (astevaihtelu A kk_k) tarvii fix_loppu
                # mutta "risti" (ei astevaihtelua) ei tarvitse
                # jos tarvii poikkeuksen, sano fix_loppu = True/False

                # takki -> takit (monikko)
                #if a_lista == kk_k and mon:
                #        fix_loppu = False
           #     if vok:
           #             txt = txt.replace(":", "")
           #     else:
           #             txt = txt.replace(":", "i")

        # paper/i  ...(!) .. oikeasti: (mon) papereitten/papereiden
        # mutta nyt sisältö +täysin+ sama kuin 5
        if tn == 6:
                malli = "paperi"
                t_lista = [0, "n", "a", "na", "in",
                           -1, v+"en", "eja", "eina", "eihin", "eissa"]
        # ov/i #veli: v = j
        if tn == 7:
                malli = "ovi"
                j = ""
                if sana == "veli":
                        j = "j"
                t_lista = [-1, j+"en", j+"ea", j+"ena", j+"een",
                           -1, j+"ien", j+"ia", j+"ina", j+"iin", j+"issa"]
                # järki, arki, särki 7 L
                if a_lista == k_j:
                        fix_loppu = False
                # tähti mon ei fix
                if a_lista == t_d:
                        fix_loppu = False
                fix_mon_loppu = False
        # 8 (...) spede nonsense 
        # nalle 
        if tn == 8:
                malli = "nalle"
                t_lista = [0, "n", "a", "na", "en",
                           0, "jen", "ja", "ina", "ihin", "issa"]

        # POIKKEUS poika aika
        #if tn in [9,10] and sana in ['poika','aika']:
        #        offset_y = -3
        #        t_lista = [0, "n", "a", "na", v+"n",
        #                   -1, "ien", "ia", "ina", "iin", c+"issa"

        # 9-15 a/ä-loppu
        # kala/
        # ks poikkeus aika 9 D (alla)
        if tn == 9:
                malli = "kala"
                a = ""
                #if sana in ["virta"] and mon:
                #        a = "a"
                t_lista = [0, a+"n", "a", "na", "an",
                           -1, "ojen", "oja", "oina", "oihin", "oissa"]
        
                fix_mon_loppu = False
        
        # koira/ # reikä ->  rei'issä (mon ine)
        #ks poikkeus poika 10 D (alla)
        if tn == 10:
                malli = "koira"
                c = ""
                if sana in ['reikä']:
                        c = "^"
                t_lista = [0, "n", "a", "na", v+"n",
                           -1, "ien", "ia", "ina", "iin", c+"issa"]
            
                fix_mon_loppu = False

        
        # omena/ (ei av?) # ödeema
        if tn == 11:
                malli = "omena"
                t_lista = [0, "n", "a", "na", v+"n",
                           -1, "ien", "ia", "ina", "iin", "issa"]
        # kulkija
        if tn == 12:
                malli = "kulkija"
                t_lista = [0, "n", "a", "na", v+"n",
                           -1, "oiden", "oita", "oina", "oihin", "oissa"]
        # katiska
        if tn == 13:
                malli = "katiska"
                t_lista = [0, "n", "a", "na", v+"n",
                           -1, "ojen", "oja", "oina", "oihin", "oissa"]
        # solakka av a
        if tn == 14:
                malli = "solakka"
                t_lista = [-2, "n", "a", "na", "an",
                           -2, "ojen", "oja", "oina", "oihin", "oissa"]
            
                fix_mon_loppu = False
                        
        # korkea
        if tn == 15:
                malli = "korkea"
                t_lista =  [0, "n", "a", "na", "an",
                            -1, "iden", "ita", "ina", "isiin", "issa"]
        # vanhempi H mp_mm
        # "molemmat" on rikki
        if tn == 16:
                malli = "vanhempi"
                t_lista = [-2, "an", "aa", "ana", "aan",
                           -2, v+"en", v+"a", v+"na", v+v+"n", v+"ssa"]
                fix_loppu = False
                fix_mon_loppu = False
        # vapaa
        if tn == 17:
                malli = "vapaa"
                t_lista = [0, "n", "ta", "na", "seen",
                           -1, "iden", "ita", "ina", "isiin", "issa"]
        # maa
        if tn == 18:
                malli = "maa"
                t_lista = [0, "n", "ta", "na", "han",
                           -1, "iden", "issa", "ina", "ihin", "issa"]
        # suo
        if tn == 19:
                malli = "suo"
                t_lista = [0, "n", "ta", "na", "hon",
                           -2, "oiden", "oita", "oina", "oihin", "oissa"]
        # filee ks. sanakirjasta!
        if tn == 20:
                malli = "filee"
                t_lista = [0, "n", "tä", "nä", "seen",
                           -1, "iden", "itä", "inä", "isiin", "issä"]
        # rosé ks. sanakirjasta!
        if tn == 21:
                malli = "rosé"
                if sana[-1] in ["é"]:
                        v = "e"
                #playboyhin, gayhin
                if sana[-1] in ["y"]:
                        v = "i"
                #kung-fuhun
                t_lista = [0, "n", "ta", "na", "h"+v+"n",
                           0, "iden", "ita", "ina", "ihin", "issa"]
        # parfait ?... Katso että merkki ^ on oikea
        if tn == 22:
                malli = "parfait"
                t_lista = [0, "^n", "^a", "^na", "^hen",
                           0, "^iden", "^ita", "^ina", "^ihin", "^issa"]
        # tiili
        if tn == 23:
                malli = "tiili"
                t_lista = [-1, "en", "tä", "enä", "een",
                           0, "en", "ä", "nä", "in", "ssä"]
        # uni
        if tn == 24:
                malli = "uni"
                t_lista = [-1, "en", "ta", "ena", "een",
                           0, "en", "a", "na", "in", "ssa"]
        # toimi
        if tn == 25:
                malli = "toimi"
                t_lista = [-1, "en", "ea", "essa", "een",
                           0, "en", "a", "na", "in", "ssa"]
        # pien/i § kieli, nuoli
        if tn == 26:
                malli = "pieni"
                t_lista = [-1, "en", "tä", "enä", "een",
                           -1, "ien", "ien", "inä", "iin", "issä"]
        # käsi
        if tn == 27:
                malli = "käsi"
                t_lista = [-2, "den", "ttä", "tenä", "teen",
                           0, "en", "ä", "nä", "in", "ssä"]
        # kynsi varsi
        if tn == 28:
                malli = "kynsi"
                if len(sana) > 2:
                        x = sana[-3]
                t_lista = [-2, x+"en", "ttä", "tenä", "teen",
                           0, "en", "ä", "nä", "in", "ssä"]
        # lapsi
        if tn == 29:
                malli = "lapsi"
                t_lista = [-3, "psen", "sta", "psena", "pseen",
                           0, "en", "a", "na", "in", "ssa"]
        # veitsi
        if tn == 30:
                malli = "veitsi"
                t_lista = [-3, "tsen", "stä", "tsenä", "tseen",
                           0, "en", "ä", "nä", "in", "ssä"]
        # kaksi
        if tn == 31:
                malli = "kaksi"
                t_lista = [-3, "hden", "hta", "htena", "hteen",
                           0, "en", "a", "na", "in", "ssa"]
        # sisar
        if tn == 32:
                malli = "sisar"
                t_lista = [0, "en", "ta", "ena", "een",
                           0, "ten", "ia", "ina", "iin", "issa"]
        # kytki/n # ydin; C t_tt: keitin kehitin
        if tn == 33:
                malli = "kytkin"
                t_lista = [-2, "imen", "intä", "imenä", "imeen",
                           -2, "mien", "miä", "minä", "miin", "missä"]
                fix_loppu = False

        # onneton C ? t_tt
        if tn == 34:
                malli = "onneton"
                t_lista = [-2, "man", "nta", "mana", "maan",
                           -2, "mat", "mia", "mina", "miin", "missa"]
                # ???
                if sana == "alaston":
                        offset_y = -1
                        offset_m = -1
                        
        # lämmin H mm_mp
        if tn == 35:
                malli = "lämmin"
                t_lista = [-3, "män", "ntä", "mänä", "mään",
                           -3, "mien", "miä", "minä", "miin", "missä"]
        # sisin
        if tn == 36:
                malli = "sisin"
                t_lista = [-1, "mmän", "ntä", "mpänä", "mpään",
                           -1, "mpien", "mpiä", "mpinä", "mpiin", "mmissä"]
        # vasen
        if tn == 37:
                malli = "vasen"
                t_lista = [-1, "mman", "nta", "mpana", "mpaan",
                           -1, "mpien", "mpia", "mpina", "mpiin", "mmissa"]
        # nainen
        if tn == 38:
                malli = "nainen"
                t_lista = [-3, "sen", "sta", "sena", "seen",
                           -3, "sien", "sia", "sina", "siin", "sissa"]
        # vastaus
        if tn == 39:
                malli = "vastaus"
                t_lista = [-1, "ksen", "sta", "ksena", "kseen",
                           -1, "kset", "ksia", "ksina", "ksiin", "ksissa"]
        # kalleus kalleu/s
        if tn == 40:
                malli = "kalleus"
                t_lista = [-1, "den", "tta", "tena", "teen",
                           -1, "ksien", "ksia", "ksina", "ksiin", "ksissa"]
        # vieras
        # viera/s /an /sta /ana /aseen # keidas # opas
        # op/as /p(aa)n /(a)sta /p(aa)na /p(aa)seen
        # #opas: astevaihtelun offset isompi, se ratkaisee
        if tn == 41:
                malli = "vieras"
                t_lista = [-1, v+"n", "sta", v+"na", v+"seen",
                           -1, "iden", "ita", "ina", "isiin", "issa"]
                if a_lista == kk_k:
                        offset_y = -2
                        offset_m = -2
                        
        # mies
        if tn == 42:
                malli = "mies"
                t_lista = [-1, "hen", "stä", "henä", "heen",
                           -1, "hien", "hiä", "hinä", "hiin", "hissä"]
        # ohut
        if tn == 43:
                malli = "ohut"
                t_lista = [-1, "en", "tta", "ena", "een",
                           -1, "iden", "ita", "ina", "isiin", "issa"]
        # kevät
        if tn == 44:
                malli = "kevät"
                t_lista = [-1, "än", "ttä", "änä", "äseen",
                           -1, "iden", "itä", "inä", "isiin", "issä"]
        # kahdeksas
        if tn == 45:
                malli = "kahdeksas"
                t_lista = [-1, "nnen", "tta", "ntena", "nteen",
                           -1, "nsien", "nsia", "nsina", "nsiin", "nsissa"]
        # tuhat
        if tn == 46:
                malli = "tuhat"
                t_lista = [-1, "nnen", "tta", "ntena", "nteen",
                           -1, "nsien", "nsia", "nsina", "nsiin", "nsissa"]
        # kuollut
        if tn == 47:
                malli = "kuollut"
                t_lista = [-2, "een", "utta", "eena", "eeseen",
                           -2, "eiden", "eita", "eina", "eisiin", "eissa"]
        # hame/ perse/
        if tn == 48:
                malli = "hame"
                t_lista = [0, "en", "tta", "ena", "eseen",
                           0, "iden", "ita", "ina", "isiin", "issa"]

                # hede
                if a_lista == d_t:
                        offset_y = -2
                        offset_m = -2
                # kate
                
                        


        # askel
        if tn == 49:
                malli = "askel"
                t_lista = [0, "en", "ta", "ena", "eeseen",
                           0, "ten", "ia", "ina", "iin", "issa"]
                
        # + yhdysnominit + (ei toimi malleina?)
        # isoäiti
        #50: [0, "näidin", "aäitiä", "naäitinä", "...",
        #   0, "", "A", "A", "", "A"],
        # nuoripari 
        #51: [0, "n", "A", "A", "",
        #   0, "", "A", "A", "", "A"]

        # poikkeuksia
        if sana in ['poika', 'aika']:
                        a_lista[1] = "j"
                        a_lista[2] = "ik"
                        a_lista[3] = "ik"
                        a_lista[4] = "ik"
                        a_lista[6] = "ik"
                        a_lista[7] = "ik"
                        a_lista[8] = "ik"
                        a_lista[9] = "ik"
                        a_lista[10] = "j"
                        #"ik", "ik", -3, "k", "k", "k", "k", ""]
                        offset_y = -3
                        offset_m = -3
                        

        
        # * offset fix? vai fix_loppu? (eri asioita) *
        # ts. lisätäänkö vokaalinpidennys vai loppuvokaali astevaihtelun
        # jälkeen vai ei?

        # ???
        
        # poikkeuksia
        for i in yks_ja_mon_lst:

                txt = t_lista[i]

                #poikkeuksia
                #poika 10 D aika 9 D
                #if sana in ['poika', 'aika']:
                #       offset_y = -3
                #       offset_m = -3
                #       # poJan, aJan, poIKia, aIKoja
                #       # 1: gen y 10: mon ine
                #       if i in [1, 10]:
                #               txt = "j"+txt
                #       else:
                #               a_lista[i] = "ik"
                #
         
                
        # jos astevaihtelu (a_lista), isompi (negatiivinen) siirtymä
        # valitaan jos offset ei ole muokattu (1 on muokkaamaton)
        if a_lista:
                if a_lista[0] < t_lista[0] and offset_y == 1:
                        t_lista[0] = a_lista[0]
                if a_lista[5] < t_lista[5] and offset_m == 1:
                        t_lista[5] = a_lista[5]

        #print ("offset y ", offset_y)                
        if offset_y < 1:
                t_lista[0] = offset_y
                #print ("offset y muokattu:", offset_y)

        #print ("offset m ", offset_m)                        
        if offset_m < 1:        
                t_lista[5] = offset_m
                #print ("offset m muokattu:", offset_m)


      
        # yks_ja_mon_lst skippaa offset (0 ja 5) koska ei ole merkkejä  
        for i in yks_ja_mon_lst:

                txt = t_lista[i]                        

                # vaihdetaan mallin aoäö jos tarvi
                
                if vok_var == "ä":
                        txt = txt.replace("a", "ä")
                        txt = txt.replace("o", "ö")
                if vok_var == "a":
                        txt = txt.replace("ä", "a")
                        txt = txt.replace("ö", "o")
                        
                # vok variantti a/ä yksikössä vaihtelee!!
                if sana in ['meri', 'veri'] and i < 3:
                        txt = txt.replace("ä", "a")
                
                #if fix_loppu:
                # ei ole tässä oikeastaan vok_pid
                #        txt = vok_pid+txt

                # katsotaan ekaksi onko ees periaatteessa fix...
                fix = False
                if a_lista:        
                        av_len = len(a_lista[i])
                        offs = offset_y
                        ekstra = offs+av_len
                        if i > 4:
                                offs = offset_m
                        if offs+av_len > 0:
                                fix = True
                        else:
                                if offs < ekstra:
                                        fix = True
                # ...jos fix periaatteessa voidaan tarvita,
                # katsotaan vielä onko liput fix_ True
                # jos on, fiksataan
                if fix:
                        if i < 5 and fix_loppu: 
                                txt = vok_pid+txt
                                debug("y fix")
                        if i > 4 and fix_mon_loppu:
                                txt = vok_pid+txt
                                debug("m fix")
                        #print("* offs < ekstra *")
                        #if ekstra > av_len:
                        #        txt = vok_pid+txt
                        #print("ekstra",ekstra,"offs",offs,"av_len",av_len)

                if args.debug:
                        print("fix_loppu",fix_loppu,"fix_mon_loppu",fix_mon_loppu)

                t_lista[i] = txt


        # pikafix! vok pid jää puuttumaan kun tehdään monikoita
        # esim
        # virrAt (yks gen)
        #if a_lista and mon and fix_loppu == False:
        #         t_lista[1] = vok_pid+t_lista[1]
               

        # monikko perusmuoto yks genetiivistä ongelmoi
        # tyhmän fix_loppu takia
          
        return t_lista


# * entä "interaktiivinen" syöte? *
def _input_():
        if len(sys.argv) > 1:
                
                input_value = sys.argv[1]
                
        else:                 
                input_value = input("syötä nimi:\n")
        
        return input_value
    
        
# syöte listaksi
def input_to_lst(input_value):


    # poistetaan lopusta välilyönnit
    # muuten tulee listaan ylimääräinen None
    input_value = input_value.rstrip()
    
    lst = input_value.split(' ')
    n = len(lst)
    #print("Sanoja", n)
    
    #print("input_to_lst len, lst:",n , lst)

    # -r rajoittaa kolmeen hakusanaan
    if args.rajoita == True:
            if n > 3:
                    return lst[:3]
    return lst

# onko syötteessä nro? jos on, se on taivutus (nro)
# sen jälkeen jos tulee jotain, se on astevaihtelu (kirjain)
# nro ja *kaikki sen jälkeen tuleva poistetaan*
# return *lyhennetty sana*, tn, av
def poista_nro_ja_loppu(sana):
        debug("BEFORE:'"+sana+"'") 
        n = re.search(r'\d+', sana).group()
        mis = sana.index(n)
        sana = sana[:mis]
        debug("AFTER:'"+sana+"'")
        return sana
          
def re_(sana):
        
        n = 0
        a = 0

        #lista = [n,a]
        
        n = re.search(r'\d+', sana).group()

        if args.debug: 
                print("re_ n:", n)
        #mis = sana.index(n)           
        a = sana[-1:]
        if args.debug:
                print(a)
        # onko viimeinen merkki kirjain?
        if a.isalpha() == True:
                if args.debug:
                        print("re_ a:", a)
                a = a.upper()
        else:
                a = 0
                if args.debug:
                        print("ei a!")
        n = int(n)

        if (n < 1 or n > 49):
                print("* tn oltava 1-49 *")
                n = 0
                
        
        if a not in[0,"A","B","C","D","E","F","G","H","I","J","K","L","M"]:
                print("* av oltava A-M tai tyhjä *")
                a = 0
        
        #lista = [n,a]
        #return[n,a]
        return[n,a] # väärin! jossain vikaa!
        

        

# taivutusnumero

def hae_kotus(sana):

        tn = 0
        av = 0
 
        for t in root.findall('st'):
                teksti = t.find('s').text
                
                # täsmääkö?
                if teksti == sana:
                        for t_ in t.iter('tn'):
                                #print(teksti[loppu:])
                                #print(t.text)
                                tn = (t_.text)
                        for a_ in t.iter('av'):
                                #print(teksti[loppu:])
                                #print(t.text)
                                av = (a_.text)
                        return[tn,av,teksti]
        return False

# hae_dero_kotus (detrimentaalinen haku)
# kaikki ei ole listassa, mutta derohaku hakee
# "detrimentaalisesti" lyhentämällä syötettä kohtiloppuosaa
# kunnes löytyy lähin vastine, esim:
# "odysseus"
# 39 0 a fariseus

def hae_dero_kotus(sana):
        #for i > 0
        #i = 1        
        #print(sana[dero:])
    d = 0
    pituus = len(sana)

# ALKU difflib 
# difflib etsii samankaltaisen sanan (jos eidiff-lippu false) 
    teksti_lista = []
    _d = 0
    while (pituus > _d and args.eidiff == False):
        _d+=1
        _loppu = _d-pituus

        #teksti = 0
        for t in root.findall('st'):
            _teksti = t.find('s').text
            #print("_teksti",_teksti)
            if _teksti[_loppu:] == sana[_d:]:
                    # ööh syötetty sana saa olla yhden merkin lyhyempi kuin sanak.
                    if len(_teksti) < len(sana)+2:
                            teksti_lista.append(t.find('s').text)
                            if args.debug:
                                    print("teksti_lista", teksti_lista)
                            # ei tehdä listasta pidempää kuin 9
                            if len(teksti_lista) > 8:
                                    break
        melkein = []
        melkein = difflib.get_close_matches(sana, teksti_lista)
        if args.debug:
                print(melkein)
        if len(melkein)>0:
                if args.debug:
                        print("* melkein:", melkein[0], "*")
                return hae_kotus(melkein[0])
   

# LOPPU difflib

    while pituus > d:
        d+=1
        #sanoja_lst = ['zen','aakkonen']
        
        loppu = d-pituus
        
        #print(sana[d:])
        tn = 0
        av = 0
        #teksti = 0
        for t in root.findall('st'):
            teksti = t.find('s').text
    
            #mahd_sanoja_lst

            #teksti[loppu:] == sana[d:]
            #mahd_sanoja_lst.append(teksti)
                
            # täsmääkö?
            
            if teksti[loppu:] == sana[d:]:
                #teksti_lista.append(t.find('s').text)
                    
                
                
                for t_ in t.iter('tn'):
                        #print(teksti[loppu:])
                        if args.debug:
                                print("tn ",t_.text)
                        tn = (t_.text)
                          
                for a_ in t.iter('av'):
                        #print(teksti[loppu:])
                        #print(t.text)
                        av = (a_.text)
                return[tn,av,teksti]
        
                
# vokaalisointu tai -häly, vokaalivariantti 
# onko a vai ä?
# ks str.find str.index jne

# HUOM! vokaalih palauttaa a / ä
# se tarkoittaa kuitenkin vain (tai jopa) onko
# etu- (y,ö,ä) vai takavokaalit (u,o,a)
def vokaalih(sana):
        #print(sana)
                # ö ä y + i + e usein -> ä
                # mutta esim vierasp jne esim lyon

        if ('a' in sana) or ('o' in sana) or ('u' in sana):
                vokaalipaate = 'a'
        else:
                vokaalipaate = 'ä'
                
        return vokaalipaate;                
        

# onko viimeinen kirjain vokaali vai ei
def vok_loppu(sana):

        if sana[-1] in vokaalit:
                return True
        else:
                return False

def ks_av_tyyppi(sana,av):
        if av == 'A':
                # alokas on k_kk (ei kk_k)
                if (sana[-3] == "k" and sana[-2] == "k"):
                        return kk_k
                else:
                        return k_kk
        if av == 'B':
                if sana[-2] == "p":
                        return pp_p
                else:
                        return p_pp
        if av == 'C':
                # onneton on t_tt (ei tt_t!)
                if sana[-3] == "t" and sana[-2] == "t":
                        return tt_t
                else:
                        return t_tt
        if av == 'D':
                if sana[-2] == "k":
                        return k_
                else:
                        return _k
        if av == 'E':
                if sana[-2] == "p":
                        return p_v
                else:
                        return v_p
        if av == 'F':
                if sana[-2] == "t":
                        return t_d
                else:
                        return d_t
        if av == 'G':
                if sana[-2] == "k":
                        return nk_ng
                else:
                        return ng_nk
        if av == 'H':
                if sana[-2] == "p":
                        return mp_mm
                else:
                        return mm_mp
        if av == 'I':
                if sana[-2] == "t":
                        return lt_ll
                else:
                        return ll_lt
        if av == 'J':
                if sana[-2] == "t":
                        return nt_nn
                else:
                        return nn_nt
        if av == 'K':
                if sana[-2] == "t":
                        return rt_rr
                else:
                        return rr_rt
        if av == 'L':
                if sana[-2] == "k":
                        return k_j
                else:
                        return j_k
        if av == 'M':
                return k_v
                
        return []


# m on monikko jos > 0 tietyt monikot: ine
def tulosta(m, nom,gen,par,ess,ill,ine):

       # if args.monikko == True:
       #         ko = luo(sana,1)
       #         # nyt tarvittaisiin monikon offset
       #         # johon pistettäisiin "/"
       #         # tyyliin:
       #         # offset = hae_offset(sana, luku)
       #         # ...sieltä (listasta) sitten haettaisiin tt/av [5]
       #         print('"'+ko+"'")

        print("")
        # esim "valkea/ im/pi"
        jakaja=" "
        i=1
        print(end='"')
        for s in nom:
                i+=1
                if i>(len(nom)):
                        jakaja='"'
                print(s, end=jakaja)
        print(",")

        # esim gen "n/men"
        jakaja="/"

        i=1
        print(end=' gen "')
        for paate in gen:               
                i+=1
                if i>(len(gen)):
                        jakaja=""
                print(paate, end=jakaja)
        print(end='",')

        jakaja="/"

        i=1

        print(end=' par "')
        for paate in par:               
                i+=1
                if i>(len(par)):
                        jakaja=""
                print(paate, end=jakaja)
        print(end='",')

        jakaja="/"

        i=1

        
        print(end=' ess "')
        for paate in ess:               
                i+=1
                if i>(len(ess)):
                        jakaja=""
                print(paate, end=jakaja)
        print(end='",')

        jakaja="/"

        i=1

        
        print(end=' ill "')
        for paate in ill:               
                i+=1
                if i>(len(ill)):
                        jakaja=""
                print(paate, end=jakaja)
        print(end='",')

        jakaja="/"

        i=1

        # tietyt monikot tarvitsee ine (mitkä? miksi? miten?)
        if m > 0:
                print(end=' ine "')
                for paate in ine:               
                        i+=1
                        if i>(len(ine)):
                                jakaja=""
                                print(paate, end=jakaja)
                                print(end='",')

                jakaja="/"

                i=1
                
        print("\n")

        

# ks §15.5 
        
# return offset (yks/mon), yks gen (av),  
#tak/ki   in  Kia Kina Kiin    Kien Keja Keina Keihin eissa
#takki : takin
kk_k = [-2, "", "k", "k", "k", -2, "k", "k", "k", "k", ""] 
#hake : hakkeen
k_kk = [-1, "k", "", "k", "k", -1, "k", "k", "k", "k", "k"] 
#kaappi : kaapin
pp_p = [-2, "", "p", "p", "p", -2, "p", "p", "p", "p", ""] 
#opas : oppaan
p_pp = [-2, "p", "", "p", "p", -2, "p", "p", "p", "p", "p"] 
#tyttö : tytön
tt_t = [-2, "", "t", "t", "t", -2, "t", "t", "t", "t", ""]
#kate : katteen
t_tt = [-1, "t", "", "t", "t", -1, "t", "t", "t", "t", "t"]
#reikä : reiän
k_   = [-2, "", "k", "k", "k", -2, "k", "k", "k", "k", ""] 
#aie : aikeen
_k   = [-1, "k", "", "k", "k", -1, "k", "k", "k", "k", "k"] 
#sopu : sovun
p_v  = [-2, "v", "p", "p", "p", -2, "p", "p", "p", "p", "v"] 
#taive : taipeen
v_p  = [-2, "p", "v", "p", "p", -2, "p", "p", "p", "p", "p"] 
#satu : sadun
t_d  = [-2, "d", "t", "t", "t", -2, "t", "t", "t", "t", "d"] 
#keidas : keitaan
d_t  = [-3, "t", "d", "t", "t", -3, "t", "t", "t", "t", "t"] 
#aurinko : auringon
nk_ng =[-2, "g", "k", "k", "k", -2, "k", "k", "k", "k", "g"] 
#rengas : renkaan
ng_nk =[-3, "k", "g", "k", "k", -3, "k", "k", "k", "k", "k"] 
#kumpi : kumman
mp_mm =[-2, "m", "p", "p", "p", -2, "p", "p", "p", "p", "m"] 
#lumme : lumpeen
mm_mp =[-2, "p", "m", "p", "p", -2, "p", "p", "p", "p", "p"] 
#ilta : illan
lt_ll =[-2, "l", "t", "t", "t", -2, "t", "t", "t", "t", "l"]
#sivellin : siveltimen
ll_lt =[-3, "t", "l", "t", "t", -3, "t", "t", "t", "t", "t"]
#hento : hennon
nt_nn =[-2, "n", "t", "t", "t", -2, "t", "t", "t", "t", "n"] 
#vanne: vanteen
nn_nt =[-2, "t", "n", "t", "t", -2, "t", "t", "t", "t", "t"] 
#virta : virran
rt_rr =[-2, "r", "t", "t", "t", -2, "t", "t", "t", "t", "r"] 
#porras : portaan
rr_rt =[-3, "t", "r", "t", "t", -3, "t", "t", "t", "t", "t"] 
#arki : arjen
k_j  = [-2, "j", "k", "k", "k", -2, "k", "k", "k", "k", "j"] 
#hylje : hylkeen
j_k  = [-2, "k", "j", "k", "k", -2, "k", "k", "k", "k", "k"] 
#suku : suvun
k_v  = [-2, "v", "k", "k", "k", -2, "k", "k", "k", "k", "v"] 


# huom. muokkaa_lista voi muuttaa OFFSET (listassa 1. ja 5.)
def mallipaate(sana, tn):

        t = {
                # 1-4 vok loppuisia
                #valo/ #häly aurinko !
                1: [0, "n", "A", "nA", "+n",
                    0, "jen", "jA", "inA", "ihin", "issA" ], 
                # palvelu/
                2: [0, "n", "A", "nA", "n",
                    0, "jen", "jA", "inA", "ihin", "issA"], 
                #valtio/
                3: [0, "n", "tA", "nA", "+n",
                    0, "iden", "itA", "inA", "ihin", "issA"],
                #laatik/ko ! (av+tämä) A+4: o+n ko ko+na ko+on
                #laatik   
                4: [-2, "n", "A", "nA", "On",
                    -2, "Ojen", "OjA", "OinA", "Oihin", "OissA"],
                # 5-7 i-loppuisia
                # risti 5 esim tuoli, pyykki (A) OFFSET -1 koska monikko!
                #risti/ ... rist/i (? monikko) zen/
                5: [0, ":n", ":A", ":nA", ":in",
                    -1, "ien", "ejA", "einA", "eihin", "eissA"],
                # paper/i  ...(!) .. oikeasti: (mon) papereitten/papereiden
                # mutta nyt sisältö +täysin+ sama kuin 5
                6: [0, "n", "A", "nA", "in",
                    -1, "ien", "ejA", "einA", "eihin", "eissA"],
                # ov/i #veli: j = j
                7: [-1, "en", "eA", "enA", "een",
                    -1, "ien", "iA", "inA", "iin", "issA"],
                # 8 oma ryhmänsä? vierasperäisiä?
                # nalle
                8: [0, "n", "A", "nA", "en",
                   0, "jen", "jA", "inA", "ihin", "issA"],
                # 9-15 a/ä-loppu
                # kala/
                9: [0, "n", "A", "nA", "An",
                -1, "ojen", "ojA", "oinA", "oihin", "oissA"],        
                # koira/ # reikä ->  rei'issä (mon ine) 
                10: [0, "n", "A", "nA", "+n",
                     -1, "ien", "iA", "inA", "iin", "issA"],
                # omena/ (ei av?) # ödeema
                11: [0, "n", "A", "nA", "+n",
                   -1, "ien", "iA", "inA", "iin", "issA"],
                # kulkija
                12: [0, "n", "A", "nA", "+n",
                   -1, "Oiden", "OitA", "OinA", "Oihin", "OissA"],
                # katiska
                13: [0, "n", "A", "nA", "+n",
                   -1, "Ojen", "OjA", "OinA", "Oihin", "OissA"],
                # solakka av A
                14: [-2, "n", "A", "nA", "An",
                   -2, "Ojen", "Oja", "OinA", "Oihin", "OissA"],
                # korkea
                15: [0, "n", "A", "nA", "An",
                   -1, "iden", "itA", "inA", "isiin", "issA"],
                # vanhempi H mp_mm
                16: [-2, "An", "AA", "AnA", "AAn",
                   -2, "+en", "+A", "+nA", "++n", "+ssA"],
                # vapaa
                17: [0, "n", "tA", "nA", "seen",
                   -1, "iden", "itA", "inA", "isiin", "issA"],
                # maa
                18: [0, "n", "tA", "nA", "hAn",
                   -1, "iden", "issA", "inA", "ihin", "issA"],
                # suo
                19: [0, "n", "tA", "nA", "hon",
                   -2, "Oiden", "OitA", "Oina", "Oihin", "OissA"],
                # filee ks. sanakirjasta!
                20: [0, "n", "tA", "nA", "seen",
                   -1, "iden", "itA", "inA", "isiin", "issA"],
                # rosé ks. sanakirjasta!
                21: [0, "n", "tA", "nA", "hen",
                   0, "iden", "itA", "inA", "isiin", "issA"],
                # parfait ?... Katso että merkki ^ on oikea
                22: [0, "^n", "^A", "^nA", "^hen",
                   0, "^iden", "^ita", "^inA", "^ihin", "^issA"],
                # tiili
                23: [-1, "en", "tA", "enA", "een",
                   0, "en", "A", "nA", "in", "ssA"],
                # uni
                24: [-1, "en", "tA", "enA", "een",
                   0, "en", "A", "nA", "in", "ssA"],
                # toimi
                25: [-1, "en", "eA", "essA", "een",
                   0, "en", "A", "nA", "in", "ssA"],
                # pien/i § kieli
                26: [-1, "en", "tA", "enA", "een",
                     -1, "ien", "ien", "inA", "iin", "issA"], #nuoli
                # käsi
                27: [-2, "den", "ttA", "tenA", "teen",
                   0, "en", "A", "nA", "in", "ssA"],
                # kynsi varsi
                28: [-2, "Xen", "ttA", "tenA", "teen",
                   0, "en", "A", "nA", "in", "ssA"],
                # lapsi
                29: [-3, "psen", "stA", "psenA", "pseen",
                   0, "en", "A", "nA", "in", "ssA"],
                # veitsi
                30: [-3, "tsen", "stA", "tsenA", "tseen",
                   0, "en", "A", "nA", "in", "ssA"],
                # kaksi
                31: [-3, "hden", "htA", "htenA", "hteen",
                   0, "en", "A", "nA", "in", "ssA"],
                # sisar
                32: [0, "en", "tA", "enA", "een",
                   0, "ten", "iA", "inA", "iin", "issA"],
                # kytki/n
                33: [-1, "men", "ntA", "menA", "meen",
                     -1, "mien", "miA", "minA", "miin", "missA"], # ydin
                # onneton C ?
                34: [-2, "mAn", "ntA", "mAnA", "mAAn",
                   -2, "mAt", "miA", "minA", "miin", "missA"],
                # lämmin H mm_mp
                35: [-3, "mAn", "ntA", "mAnA", "mAAn",
                   -3, "mien", "miA", "minA", "miin", "missA"],
                # sisin
                36: [-1, "mmAn", "ntA", "mpAnA", "mpAAn",
                   -1, "mpien", "mpiA", "mpinA", "mpiin", "mmissA"],
                # vasen
                37: [-1, "mmAn", "ntA", "mpAnA", "mpAAn",
                   -1, "mpien", "mpiA", "mpinA", "mpiin", "mmissA"],
                # nainen
                38: [-3, "sen", "stA", "senA", "seen",
                   -3, "sien", "siA", "sinA", "siin", "sissA"],
                # vastaus
                39: [-1, "ksen", "stA", "ksenA", "kseen",
                   -1, "kset", "ksiA", "ksinA", "ksiin", "ksissA"],
                # kalleus kalleu/s
                40: [-1, "den", "ttA", "tenA", "teen",
                   -1, "ksien", "ksiA", "ksinA", "ksiin", "ksissA"],
                # vieras
                # viera/s /an /sta /ana /aseen # keidas # opas
                # op/as /p(aa)n /(a)sta /p(aa)na /p(aa)seen
                # #opas: astevaihtelun offset isompi, se ratkaisee
                41: [-1, "+n", "stA", "+nA", "+seen",
                     -1, "iden", "itA", "inA", "isiin", "issA"],
                # mies
                42: [-1, "hen", "stA", "henA", "heen",
                   -1, "hien", "hiA", "hinA", "hiin", "hissA"],
                # ohut
                43: [-1, "en", "ttA", "enA", "een",
                   -1, "iden", "itA", "inA", "isiin", "issA"],
                # kevät
                44: [-1, "An", "ttA", "AnA", "Aseen",
                   -1, "iden", "itA", "inA", "isiin", "issA"],
                # kahdeksas
                45: [-1, "nnen", "ttA", "ntenA", "nteen",
                   -1, "nsien", "nsiA", "nsinA", "nsiin", "nsissA"],
                # tuhat
                46: [-1, "nnen", "ttA", "ntenA", "nteen",
                   -1, "nsien", "nsiA", "nsinA", "nsiin", "nsissA"],
                # kuollut
                47: [-2, "een", "uttA", "eenA", "eeseen",
                   -2, "eiden", "eitA", "einA", "eisiin", "eissA"],
                # hame/ perse/
                48: [0, "en", "ttA", "enA", "eseen",
                     0, "iden", "itA", "inA", "isiin", "issA"],
                # askel
                49: [0, "en", "tA", "enA", "eeseen",
                   0, "ten", "iA", "inA", "iin", "issA"],
                # + yhdysnominit + (ei toimi malleina?)
                # isoäiti
                #50: [0, "näidin", "aäitiä", "naäitinä", "...",
                #   0, "", "A", "A", "", "A"],
                # nuoripari 
                #51: [0, "n", "A", "A", "",
                #   0, "", "A", "A", "", "A"]
        }
        
        lista = t.get(tn)
        # jos None, täytyy tehdä jotain muuta
        try:
                return lista
        except:
                print("Taivutusmallia (numeroa) ei löydy!") # None!


_main_()

