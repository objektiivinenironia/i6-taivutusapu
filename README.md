# Apuohjelma taivutusten tulostamiseen
*Ad hoc nominien taivutusapu Inform 6-ohjelmalle (Python3-skripti ja muokattu Kotus-sanalista)*

Apuohjelma hakee sanalistasta lähimmän vastaavuuden ja yrittää tuottaa ohjeet Inform-6 ohjelmalle taivutuksista *genetiivi, partitiivi, essiivi ja illatiivi* (monikossa myös *inessiivi*). Taivutusohjeet tarvitaan suomenkieliseen Inform 6-kotoistuksen taivutusten tulostamiseen.

Ohjelmaan syötetään nomini(t) yksikössä perusmuodossa (nominatiivi).

```
> python3 tee.py "spede" 
````


Monikko tulostetaan valitsimella -m. 

Puute: yksikköä ja monikkoa ei voi tulostaa samasta nimestä -- sitä ei voi tehdä Inform 6 kotoistuksessakaan: *"nakki ja muusi"* tai *"nakit ja  muusit"* toimii, muttei *"nakit ja muusi"*.

Koska sanalistassa ei ole erisnimiä pienet kirjaimet todennäköisimmin täsmää, mutta listassa on joitain yleisiä lyhenteitä isoilla kirjaimilla.

TODO: valitsin jolla pien- ja suuraakkosten ero ohitetaan haussa.

TODO: syötteen kelpoutus.

Valitsin -e kytkee vertailevan haun pois jolloin haku ohittaa merkkejä kunnes loppuosa täsmää (detrimentaalinen haku). 

Kun halutaan tuottaa taivutusohje tietyn mallin mukaan, voidaan lisätä taivutusnumero (Kotus-luokka) syötteeseen. Esimerkiksi kun tiedetään ettei "Spede" taivu kuin "hede" (48 F), vaan kuin mallisana "nalle" (8), annetaan syöte "Spede8" ja saadaan haluttu taivutusohje.

```
 spedejen
 spedejä
 spedeinä
 spedeihin
 spedeissä

"spede/t",
 gen "jen", par "jä", ess "inä", ill "ihin", ine "issä",
```

Apuohjelmassa hyödynnetään Kotimaisten kielten keskuksen sanalistasta muokattua versiota. Listasta on poistettu mm. verbit.
Mukana on myös *sanalistan-kuvaus*.
Alkuperäinen kotus-sanalista, sanalistan kuvaus ja niiden käyttöehdot löytyvät täältä:

<https://kaino.kotus.fi/sanat/nykysuomi/>

Tämän apuohjelma käyttää samoja ehtoja ja on (c) Jack Zyrp 2021-2023.

GNU LGPL (Lesser General Public License), EUPL v.1.1 (Euroopan unionin yleinen lisenssi) ja CC Nimeä 3.0.


