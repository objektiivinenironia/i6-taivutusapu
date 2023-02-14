# Tulostusapu (Inform 6 nominien taivutuksen tulostusohjeen kehitin)

_Apuohjelma nominien taivutusohjeiden tulostamiseen inform 6/11-kirjaston kotoistukselle_

Inform 6/11 tarvitsee ohjeita kun tulostetaan nominien taivutuksia.
Taivutusohjeet voi yrittää tulostaa tällä apuohjelmalla.
Python3-skripti. 
Käyttää näitä: xml.etree.ElementTree, sys, argparse, re ja difflib.
Lisäksi mukana on kotus-sanalista_lyh.xml ja sanalistan-kuvaus.txt 
Sanalista on karsittu versio Kotimaisten kielten tutkimuskeskuksen sanalistasta v:lta 2006.
Alkuperäiset löytyvät täältä:


Sanalistassa ei ole verbejä, erisnimiä, fantasiasanoja (keksittyjä tai muuten) ohjelma antaa ehdotuksen samankaltaisen sanan perusteella.

Kun sanaa ei löydy listasta, difflib etsii samankaltaisia sanoja ja antaa yhden ehdotuksen. Jos se ei tunnu antavan oikeaa taivutusta, valitsin -e kytkee difflibin pois jolloin haku ohittaa merkkejä kunnes loppuosa täsmää (detrimentaalinen haku). 

Pienet kirjaimet todennäköisimmin täsmää koska listassa ei ole erisnimiä, mutta listassa on joitain yleisiä lyhenteitä isoilla kirjaimilla.

TODO: valitsin jolla ohitetaan kirjainkoko haussa. 

Esimerkiksi kuvitteellinen hahmo nimeltä Jack Zyrp:

python3 tee.py "Zyrp"

 Zyrpin
 Zyrpiä
 Zyrpinä
 Zyrpiin

 "Zyrp/",
  gen "in", par "iä", ess "inä", ill "iin",

Täydennät vain "Jack", jos et halua etunimeä taivutettavan.
 
"Jack Zyrp/",

Monikko tulostetaan valitsimella -m. 

Puute: yksikkö ja monikko ei voi tulostaa samaan nimestä. Tätä kirjoitettaessa sitä ei voi tehdä Inform 6 kotoistuksessakaan.

Kaikki ei tulostu automaattisesti oikein.
jos apuohjelma tulostaa taivutusohjeen  väärin, voi antaa taivutusnumeron (ja tarvittaessa astevaihtelua merkitsevän kirjaimen) syötteen loppuun, esim. tn 5 on melko yleinen kun taivutetaan vierasperäisiä nomineja.

Esimerkiksi "Spede" ei taivu ohjelmalla niinkuin toivoisi (taivuttaa "hede" mukaan). Ongelma voidaan ratkaista muokkaamalla taivutusohjetta suoraan

"Spede/",
 gen "n", par "ä", ess "nä", ill "en",

...tai kun tiedetään että Spede taipuu kuin mallisana "nalle" (tn 8), voidaan syöttää "Spede8" tai jopa lisätä Spede sanalistaan.
