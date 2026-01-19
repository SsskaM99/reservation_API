# DEVELOPMENT_PLAN

## 1. Tavoite
Tavoitteena on toteuttaa tehtävänannossa kuvattu Meeting Room Reservation API.
Projektissa keskitytään varauslogiikan oikeellisuuteen, selkeään rakenteeseen ja
testattavuuteen.

---

## 2. Työtapa
Työ tehdään vaiheittain:
- ensin rakennetaan toimiva perusratkaisu
- tämän jälkeen toimintaa testataan
- havaittuja puutteita korjataan
- korjausten jälkeen testit ajetaan uudelleen

Jokainen vaihe tallennetaan omana commitinaan versionhallintaan.

---

## 3. Vaiheet

### 3.1 Suunnittelu
- määritellään API:n endpointit
- määritellään varauksen tietomalli
- määritellään säännöt:
  - varaukset eivät saa mennä päällekkäin
  - varauksia ei saa luoda menneisyyteen
  - aloitusajan tulee olla ennen lopetusaikaa

---

### 3.2 Toteutus
- rakennetaan FastAPI-sovellus
- toteutetaan in-memory-tallennus
- toteutetaan varauslogiikka ja rajapinta

---

### 3.3 Testaus
- testataan varauslogiikan toiminta
- testataan API:n perustoiminnot
- huomioidaan reunatapaukset

Testaus tehdään pytestillä.

---

### 3.4 Korjaus
- korjataan testauksessa havaitut virheet
- ajetaan testit uudelleen

---

## 4. Lopputulos
Lopputuloksena on toimiva ja testattu API, joka vastaa tehtävänannon vaatimuksia.
