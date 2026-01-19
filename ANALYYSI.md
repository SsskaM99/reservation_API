# ANALYYSI

## 1. Mitä tekoäly teki hyvin?

Tekoäly onnistui luomaan toimivan lähtötason ratkaisun suhteellisen nopeasti.
Se tuotti selkeän projektirakenteen, jossa vastuut oli jaettu loogisesti eri
kerroksiin (API, palvelulogiikka, tallennus, skeemat ja testit).

API täytti tehtävän perusvaatimukset:
- varauksen luonti
- varauksen peruutus
- varausten listaus huoneittain

Lisäksi tekoäly:
- toteutti päällekkäisten varausten tarkistuksen oikein
- huomioi aikavalidoinnit (menneisyys ja aloitusajan oltava ennen lopetusaikaa)
- loi sekä yksikkö- että integraatiotestejä
- hyödynsi FastAPI:n ja Pydanticin perusominaisuuksia järkevästi

Tekoälyn tuottama koodi oli ajettavaa ja toimi peruscaseissa ilman käsin tehtyä
debuggausta, mikä teki siitä hyvän pohjan jatkokehitykselle.

---

## 2. Mitä tekoäly teki huonosti?

Tekoälyn tuottamassa koodissa oli useita puutteita ja epäkohtia, jotka vaativat
ihmisen tekemää katselmointia ja korjaamista.

Merkittävimmät ongelmat olivat:
- Pydantic v2 -yhteensopivuusongelmat (vanhentuneet `@validator`-dekorattorit ja
  `orm_mode`-konfiguraatio)
- Epäselvä API-sopimus, jossa `room_id` oli sekä URL-polussa että request bodyn
  sisällä, ja arvoa jopa ylikirjoitettiin ohjelmallisesti
- Liian monimutkainen ja osittain turha aikavyöhykevalidaatiologiikka
- Puutteellinen testikattavuus reunatapauksille (esim. vierekkäiset varaukset,
  tyhjän huoneen listaus, naive datetime -arvot)
- Puuttuvat testiriippuvuudet (`httpx`), mikä esti testien ajamisen aluksi
- Rakennetyökalujen generoimien tiedostojen (esim. `__pycache__`) päätyminen
  versionhallintaan ilman `.gitignore`a

Nämä ovat tyypillisiä ongelmia, joita syntyy, kun tekoäly tuottaa koodia ilman
täyttä kontekstia käytetystä kirjastoversiosta tai projektin pitkän aikavälin
ylläpidettävyydestä.

---

## 3. Mitkä olivat tärkeimmät parannukset ja miksi?

Tärkeimmät parannukset keskittyivät koodin selkeyteen, ylläpidettävyyteen ja
luotettavuuteen:

1. **Pydantic v2 -korjaukset**  
   Päivitin validaattorit ja konfiguraation vastaamaan Pydantic v2 -käytäntöjä.
   Tämä poisti varoitukset ja varmisti yhteensopivuuden tulevien versioiden kanssa.

2. **API-sopimuksen selkeyttäminen**  
   Poistin `room_id`:n request bodysta ja käytin sitä vain path-parametrina.
   Tämä teki rajapinnasta yksiselitteisen ja poisti tarpeen Pydantic-mallien
   mutatoinnille.

3. **Aikavyöhykevalidaation yksinkertaistaminen**  
   Yksinkertaistin validaatiologiikkaa siten, että vain timezone-aware datetime
   -arvot hyväksytään ja kaikki ajat normalisoidaan sisäisesti UTC:ksi.
   Tämä paransi koodin luettavuutta ilman toiminnallisia muutoksia.

4. **Reunatapausten lisääminen testeihin**  
   Lisäsin testejä tilanteille, joita tekoäly ei alun perin kattanut, kuten
   vierekkäiset varaukset, tyhjän huoneen listaus ja naive datetime -arvojen
   hylkääminen. Tämä paransi luottamusta varauslogiikan oikeellisuuteen.

5. **Versionhallinnan siistiminen**  
   Lisäsin `.gitignore`-tiedoston estämään build-artifaktien ja paikallisten
   työpaperien päätymisen versionhallintaan.

Yleisesti ottaen tekoäly toimi hyvänä “junior-parikoodaajana”, joka tuotti
käyttökelpoisen lähtötason. Ihmisen rooli oli tunnistaa epäselvyydet,
kirjastoversioihin liittyvät ongelmat sekä rajatapaukset, ja jalostaa ratkaisu
ammattimaiseksi ja ylläpidettäväksi kokonaisuudeksi.
