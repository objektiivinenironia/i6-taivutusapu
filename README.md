# Apuohjelma taivutusten tulostamiseen
*Python-skripti ja ad hoc Kotus-sanalista nominien taivutusohjeiden tuottamiseen Inform 6-ohjelmalle*

Apuohjelma hakee sanalistasta lähimmän vastaavuuden ja yrittää tuottaa ohjeet Inform-6 ohjelmalle taivutuksista *genetiivi, partitiivi, essiivi ja illatiivi* (monikossa myös *inessiivi*). Taivutusohjeet tarvitaan suomenkieliseen Inform 6-ohjelmaan jotta se tulostaa taivutuksia.

   - Python riippuvuudet: xml.etree.ElementTree, sys, argparse, re ja difflib.

Ohjelmaan syötetään nomini(t) yksikössä perusmuodossa (nominatiivi)

Monikko tulostetaan valitsimella -m. 

Puute: yksikköä ja monikkoa ei voi tulostaa samasta nimestä. Sitä ei voi tehdä Inform 6 kotoistuksessakaan ("nakki ja muusi" tai "nakit ja  muusit" muttei "nakit ja muusi")

Koska sanalistassa ei ole erisnimiä pienet kirjaimet todennäköisimmin täsmää, mutta listassa on joitain yleisiä lyhenteitä isoilla kirjaimilla.

TODO: valitsin jolla pien- ja suuraakkosten ero ohitetaan haussa.

TODO: syötteen kelpoutus.

Valitsin -e kytkee vertailevan haun pois jolloin haku ohittaa merkkejä kunnes loppuosa täsmää (detrimentaalinen haku). 

Kun halutaan tuottaa taivutusohje tietyn mallin mukaan, voidaan lisätä taivutusnumero (Kotus-luokka) syötteeseen. Esimerkiksi kun tiedetään että erisnimi "Spede" ei taivu kuin "hede" (48 F) vaan kuin mallisana "nalle" (8), annetaan syöte "Spede8", jolloin saadaan haluttu taivutusohje.

```
 spedejen
 spedejä
 spedeinä
 spedeihin
 spedeissä

"spede/t",
 gen "jen", par "jä", ess "inä", ill "ihin", ine "issä",
```

