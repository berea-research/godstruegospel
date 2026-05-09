"""
skill_v5_preflight.py — godstruegospel skill v5.1, module 5: pre-flight
========================================================================

Pre-flight vangnet. Roept interview aan, detecteert chronologie en relevante
interpretatieve keuzes, bouwt bronnen-manifest, rapporteert poort-status.
Bij dichte poort en --enforce exit code 1.

CLI:
    python3 skill_v5_preflight.py --vraag "<vraag>" --json
    python3 skill_v5_preflight.py --vraag "<vraag>" --enforce --json
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KENNIS = os.path.join(ROOT, "Kennis")
INTERVIEW_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill_v5_interview.py")

CHRONO_PATTERNS = [
    r'\bchronologi',
    r'\btijdrekening\b',
    r'\bjaren?\s+sinds\b',
    r'\bjaren\s+\w+\s+sinds\b',
    r'\bhoeveel jaar\b',
    r'\bhoeveel jaren\b',
    r'\banno homin(is|us|es)\b',
    r'\banno mundi\b',
    r'\bgeslachtsregister',
    r'\btijdlijn\b',
    r'\bdatering\b',
    r'\bjubeljaar',
    r'\bjubelcycli',
    r'\bsabbatsjaar',
    r'\bzeventig jaarweken\b',
    r'\bzondvloed\b',
    r'\bvan adam tot\b',
    r'\bvan abraham tot\b',
    r'\bsinds adam\b',
    r'\bsinds abraham\b',
    r'\buittocht\b',
    r'\btempel\b.*\b(bouw|fundering|voltooiing)\b',
    r'\bduizend(\s+jaar|jarig)',
    r'\bmillenni',
]

# Interpretatieve keuzes uit Kennis/protocollen/interpretatieve-keuzes.md
# Elke chronologie-vraag activeert standaard alle 7 keuzepunten voor expliciete
# bron-weging. De skill past de werk-conclusies toe en vermeldt zwakkere alternatieven.
INTERPRETATIEVE_KEUZEPUNTEN_BIJ_CHRONOLOGIE = [
    'K1: Inclusief tellen (werk-conclusie: inclusief, bron Lev 23/25 + NT)',
    'K2: Halve-jaar correctie (werk-conclusie: ja, marge ~9 jaar over 18 generaties)',
    'K3: Terach 70 of 130 (werk-conclusie: 130 via Hand 7:4 + Gen 11:32 + 12:4)',
    'K4: Belofte bij vertrek of vóór Charan (werk-conclusie: vóór Charan, Abram 70, via Hand 7:2-3 + Gal 3:17 + Gen 15:13 + 21:5)',
    'K5: Tempel-eindpunt fundering of voltooiing (werk-conclusie: voltooiing tempel + paleis = +20 jaar, via 1 Kon 6:38 + 7:1 + 9:10)',
    'K6: Daniël 9 = 490 of 500 (genuinely meerduidig, beide opties tonen)',
    'K7: Externe BC/AD-ankering (geen voorkeur, op verzoek meerdere ankerpunten tonen)',
]

# Externe historische tradities — context, geen alternatieve leeshoeken
EXTERNE_TRADITIES_VRAAGSIGNALEN = {
    'ussher': [r'\bussher\b', r'\b4004\s*v\.?c\.?\b'],
    'joods-rabbinaal': [r'\bjoodse kalender\b', r'\bseder olam\b', r'\bam\s*5[0-9]{3}', r'\b3761\s*v\.?c\.?\b', r'\b5786\b'],
    'septuagint-byzantijns': [r'\blxx\b', r'\bseptuagint\b', r'\bbyzantijns', r'\bam\s*7[0-9]{3}'],
    'modern-archeologisch': [r'\bmodern[ -]archeologisch', r'\bwetenschappelijk\b', r'\b967\s*v\.?c\.?\b'],
}

# Typologie-laag: signalen die activatie van de typologie-laag triggeren.
# Per categorie: regex-patronen + bestand(en) die geladen moeten worden.
TYPOLOGIE_TRIGGERS = {
    'B_cijfer/120': {
        'patterns': [r'\b120\b', r'\bhonderdtwintig\b', r'\bjubel', r'\bmozes\b', r'\bpinkster', r'\bnumeri\s+7\b', r'\bdani[eë]l\s+6\b'],
        'pad': 'Kennis/typologie/B_cijfer/120.md',
    },
    'B_cijfer/3': {
        'patterns': [r'\b(cijfer\s+)?drie\b', r'\bderde\b', r'\bdriemaal\b', r'\bdrievoudig', r'\b(twee\s+of\s+)?drie\s+getuigen', r'\bdrie\s+dagen\b', r'\bderde\s+dag\b', r'\bpetrus.{0,30}(verloochen|drie)', r'\bjona\b', r'\bhosea\s+6\b', r'\bbileam\b', r'\bheilig\s*,?\s*heilig\s*,?\s*heilig\b', r'\bdrie\s+jaar\b', r'\bdrie\s+maanden\b'],
        'pad': 'Kennis/typologie/B_cijfer/3.md',
    },
    'B_cijfer/7': {
        'patterns': [r'\b(cijfer\s+)?zeven\b', r'\bzevende\b', r'\bzevenmaal\b', r'\bzevenvoudig', r'\bsabbat', r'\bsabbatsjaar\b', r'\bjubel', r'\bbe[eë]r\W?sjeba\b', r'\bjericho\b', r'\bna[aä]man\b', r'\bzeven\s+dagen\b', r'\bzeven\s+jaar', r'\bzeven\s+gemeenten\b', r'\bzeven\s+(zegels|trompetten|schalen|geesten|kandelaren|sterren|hoofden)\b', r'\bzeventig\s+maal\s+zeven\b', r'\bopenbaring\s+1?\d\b', r'\bjozef.{0,20}droom', r'\bjakob.{0,20}rachel'],
        'pad': 'Kennis/typologie/B_cijfer/7.md',
    },
    'B_cijfer/8': {
        'patterns': [r'\b(cijfer\s+)?acht\b', r'\bachtste\b', r'\bbesnij(d|den)', r'\bachtste\s+dag\b', r'\bacht\s+dagen\b', r'\bacht\s+zielen\b', r'\boktaem|oktah[eè]', r'\batzeret\b', r'\bsluitingsfeest\b', r'\bnoach.{0,20}acht', r'\bisai.{0,20}(acht|zonen)', r'\bverheerlijking\b', r'\bhizkia.{0,20}(tempel|reinig)', r'\bbeest.{0,30}achtste\b', r'\bopenbaring\s+17\b'],
        'pad': 'Kennis/typologie/B_cijfer/8.md',
    },
    'B_cijfer/10': {
        'patterns': [r'\b(cijfer\s+)?tien\b', r'\btiende\b', r'\btienden\b', r'\btien\s+(woorden|geboden)\b', r'\btien\s+plagen\b', r'\btien\s+(maagden|talenten|knechten|melaatsen|drachmen|hoorns|stammen|dagen|generaties|rechtvaardig)', r'\bmelchizedek\b', r'\bma[\'’]aser\b', r'\bdaniel\s+1\b', r'\bdaniel\s+7\b', r'\bopenbaring\s+(2|12|13|17)\b', r'\bsodom.{0,30}rechtvaardig', r'\bjerobeam\b', r'\btien.?stammenrijk\b'],
        'pad': 'Kennis/typologie/B_cijfer/10.md',
    },
    'B_cijfer/12': {
        'patterns': [r'\b(cijfer\s+)?twaalf\b', r'\btwaalfde\b', r'\btwaalf\s+(stammen|zonen|discipelen|apostelen|stenen|broden|vorsten|hoofden|verspieders|staven|tronen|legioenen|poorten|fundamenten|sterren|manden|vruchten|jaar)\b', r'\b144[\s\.]?000\b', r'\bnieuw\s+jeruzalem\b', r'\bopenbaring\s+(7|12|21|22)\b', r'\bborststuk\s+hogepriester\b', r'\btoonbroden\b', r'\bjordaan(overgang|.{0,15}stenen)\b', r'\bbloedvloeiende\s+vrouw\b', r'\bja[iï]rus', r'\bja[ck]obus\s+1\b'],
        'pad': 'Kennis/typologie/B_cijfer/12.md',
    },
    'B_cijfer/40': {
        'patterns': [r'\b(cijfer\s+)?veertig\b', r'\b40\s+(dagen|jaar|jaren|nachten|slagen)\b', r'\bvloed\b', r'\b(woestijn|woestijntijd)\b', r'\bsinai\b', r'\bhoreb\b', r'\bnineve', r'\b(jezus|christus).{0,30}vasten', r'\bverheerlijking\b', r'\bgoliath\b', r'\bdavid.{0,20}regeer', r'\bsalomo.{0,20}regeer', r'\b(othniel|debora|gideon|eli)\b', r'\bmozes.{0,30}(midian|fasen|leven)', r'\bezechi[eë]l\s+4\b', r'\bopstand(ing).{0,30}40', r'\bhemelvaart\b'],
        'pad': 'Kennis/typologie/B_cijfer/40.md',
    },
    'B_cijfer/50': {
        'patterns': [r'\b(cijfer\s+)?vijftig\b', r'\bvijftigste\b', r'\bjubel(jaar)?\b', r'\bpinkster(en|dag)?\b', r'\bpentekost', r'\bomer.{0,15}(telling|tell)', r'\b50\s+(dagen|jaar|lussen|haken|mannen)\b', r'\blevit(en|isch).{0,30}(uitdienst|leeftijd|50)', r'\belia.{0,30}50', r'\bachazja\b', r'\bobadja.{0,30}profeten', r'\bsodom.{0,30}vijftig', r'\bvrijheid\s+uitroep'],
        'pad': 'Kennis/typologie/B_cijfer/50.md',
    },
    'B_cijfer/70': {
        'patterns': [r'\b(cijfer\s+)?zeventig\b', r'\b70\s+(zielen|oudsten|jaar|jaren|palmbomen|zonen|discipelen|volken|weken)\b', r'\bbalingschap\b', r'\bbabel.{0,20}(70|zeventig)', r'\bjeremia\s+(25|29)\b', r'\bdaniel\s+9\b', r'\bjaar(weken|week)\b', r'\bzeventig\s+maal\s+zeven\b', r'\belim\b', r'\bgideon.{0,20}zonen\b', r'\babimelech\b', r'\bachab.{0,20}zonen\b', r'\bjehu\b', r'\bsanhedrin\b', r'\blukas\s+10\b', r'\bvolken.?tafel\b'],
        'pad': 'Kennis/typologie/B_cijfer/70.md',
    },
    'B_cijfer/144': {
        'patterns': [r'\b144(\.?000)?\b', r'\b(honderd\W?vier\W?en\W?veertig|honderdvierenveertig)(duizend)?\b', r'\bverzegelden\b', r'\b144[\s\.]?000\b', r'\bopenbaring\s+(7|14|21)\b', r'\blam.{0,30}sion\b', r'\bnieuw\s+lied\b', r'\bnieuw\s+jeruzalem.{0,30}muur', r'\b12\s*[x×*]\s*12\b'],
        'pad': 'Kennis/typologie/B_cijfer/144.md',
    },
    'B_cijfer/153': {
        'patterns': [r'\b153\b', r'\b(honderd\W?drie\W?en\W?vijftig|honderddrieenvijftig)\b', r'\bjohannes\s+21\b', r'\bjoh\s+21\b', r'\bwonder(bare|lijke).{0,15}vis(vang|vangst)', r'\bvisvangst\b', r'\b(vissen).{0,30}(Tiberias|Genesareth)', r'\bpetrus.{0,30}(net|herstel|hou)\s', r'\bderde.{0,30}verschijn'],
        'pad': 'Kennis/typologie/B_cijfer/153.md',
    },
    'B_cijfer/666': {
        'patterns': [r'\b666\b', r'\b(zes\W?honderd\W?zes\W?en\W?zestig|zeshonderdzesenzestig)\b', r'\bgetal\s+(van\s+)?(de\s+|het\s+)?beest\b', r'\bmens.?getal\b', r'\bgematria\b', r'\bopenbaring\s+13\b', r'\bsalomo.{0,30}(666|talent|goud.{0,15}jaar)', r'\bkoningswet\b', r'\bdeuteronomium\s+17\b', r'\badonikam\b'],
        'pad': 'Kennis/typologie/B_cijfer/666.md',
    },
    'B_cijfer/1000': {
        'patterns': [r'\b(cijfer\s+)?duizend\b', r'\b1000\b', r'\bmillennium\b', r'\bduizend.?jarig(e)?\s+rijk\b', r'\bduizend\s+(jaar|jaren|geslachten|bergen)\b', r'\bopenbaring\s+20\b', r'\bsatan.{0,20}(gebonden|los)\b', r'\b2\s*petrus\s+3\b', r'\bels?[ae]f\b', r'\boversten\s+over\s+duizend\b', r'\bsaul.{0,30}(duizenden|tienduizenden)', r'\bdavid.{0,30}(duizend|tienduizend|telling)\b', r'\bbethlehem.{0,30}(klein|duizenden|alfei)'],
        'pad': 'Kennis/typologie/B_cijfer/1000.md',
    },
    'C_tijd/derde-dag': {
        'patterns': [r'\bderde dag\b', r'\bdrie dagen\b', r'\bopstanding\b', r'\bjona\b', r'\bhosea\s+6\b', r'\bemma[üu]s', r'\babraham\b.*\bisaak\b', r'\bsina[iï]'],
        'pad': 'Kennis/typologie/C_tijd/derde-dag.md',
    },
    'C_tijd/dagen-eerste': {
        'patterns': [r'\beerste\s+dag\b', r'\beerste\s+(van\s+)?(de\s+)?week\b', r'\bopstandings?morgen\b', r'\byom\s+echad\b', r'\bmia\s+(t[oō]n\s+)?sabbat', r'\bgenesis\s+1[\s:.]', r'\beerste\s+maand\b', r'\beerste\s+dag\s+van\s+(de\s+)?eerste\s+maand\b', r'\btabernakel.{0,30}opgericht\b', r'\bhizkia.{0,20}tempel.{0,20}reinig', r'\bezra.{0,30}terugkeer', r'\bbroodbreking\b', r'\bheer.?dag\b'],
        'pad': 'Kennis/typologie/C_tijd/dagen-eerste.md',
    },
    'C_tijd/dagen-tweede': {
        'patterns': [r'\btweede\s+dag\b', r'\btwee\s+dagen\b', r'\bgenesis\s+1[\s:.]?[6-8]\b', r'\b(wateren|water).{0,15}(scheid|uitspansel)', r'\bhet\s+was\s+goed.{0,30}ontbreekt', r'\bhosea\s+6[\s:.]?2\b', r'\blazarus.{0,30}(twee\s+dagen|wacht)', r'\bsamaritaanse\b', r'\bsychar\b', r'\bmozes.{0,30}(egyptenaar|tweede\s+dag)', r'\btweede\s+pesach\b', r'\btweede\s+maand\b'],
        'pad': 'Kennis/typologie/C_tijd/dagen-tweede.md',
    },
    'C_tijd/dagen-vierde': {
        'patterns': [r'\bvierde\s+dag\b', r'\bvier\s+dagen\b', r'\b(zon\s+en\s+maan\s+en\s+sterren|zon|maan|sterren)\s+(geschapen|geplaatst)', r'\btwee\s+grote\s+lichten\b', r'\bgenesis\s+1[\s:.]?(1[4-9])\b', r'\blazarus.{0,30}(vier\s+dagen|tetartaios|riekt\s+al)', r'\bcornelius\b', r'\bvierde\s+(trompet|zegel|schaal|engel)\b', r'\bopenbaring\s+8[\s:.]?12\b', r'\bme[\'’]orot\b', r'\bmo[\'’]adim\b', r'\btekens\s+en\s+vastgestelde\s+tijden\b'],
        'pad': 'Kennis/typologie/C_tijd/dagen-vierde.md',
    },
    'C_tijd/dagen-vijfde': {
        'patterns': [r'\bvijfde\s+dag\b', r'\bvijf\s+dagen\b', r'\bvijfde\s+deel\b', r'\bgenesis\s+1[\s:.]?(2[0-3])\b', r'\bzeegedierte\b', r'\b(eerste\s+)?zegen\s+god\b', r'\beerste\s+bara\b', r'\bnefesh\s+chayah\b', r'\bschuldoffer.{0,30}toevoeg', r'\blossing(s)?regel', r'\bvijfde\s+(zegel|trompet|schaal|fundament)\b', r'\bvallende\s+ster\b', r'\babyssos\b', r'\bsprinkhanen.{0,20}openbaring'],
        'pad': 'Kennis/typologie/C_tijd/dagen-vijfde.md',
    },
    'C_tijd/dagen-zesde': {
        'patterns': [r'\bzesde\s+dag\b', r'\bzesde\s+uur\b', r'\bzesde\s+maand\b', r'\bzesde\s+jaar\b', r'\bgenesis\s+1[\s:.]?(2[4-9]|3[01])\b', r'\bmens.{0,15}beeld\s+god', r'\bzeer\s+goed\b', r'\bnaar\s+ons\s+beeld\b', r'\bmanna.{0,30}dubbel', r'\bsabbat(s)?jaar.{0,30}voorbereiding', r'\bzesde\s+(zegel|trompet|schaal)\b', r'\beufraat\b', r'\bduisternis.{0,20}kruisiging\b', r'\bgabriel\s+(maria|engel)', r'\belisabet.{0,20}zwanger'],
        'pad': 'Kennis/typologie/C_tijd/dagen-zesde.md',
    },
    'C_tijd/dagen-zevende': {
        'patterns': [r'\bzevende\s+dag\b', r'\bsabbat(d?ag|sdienst)?\b', r'\bvierde\s+gebod\b', r'\bgenesis\s+2[\s:.]?[1-3]\b', r'\bgod.{0,20}rustte\b', r'\bsabbat(s)?jaar\b', r'\bsabbatismos\b', r'\bheer.?dag\b', r'\bkuriak[eē]\s+h[eē]mera\b', r'\bheer\s+der\s+sabbat\b', r'\bovergebleven\s+sabbat', r'\bhebree[eë]n\s+4\b', r'\bsabbat(s)?(genezing|genezen)\b', r'\bverbondsteken\s+sabbat\b'],
        'pad': 'Kennis/typologie/C_tijd/dagen-zevende.md',
    },
    'C_tijd/dagen-achtste': {
        'patterns': [r'\bachtste\s+dag\b', r'\bna\s+acht\s+dagen\b', r'\bachtste\s+jaar\b', r'\batzeret\b', r'\bsluitingsfeest\b', r'\bloofhutten.{0,30}(slot|achtste|grote\s+dag)', r'\bjohannes\s+(7|20)\b', r'\btomas.{0,30}geloof', r'\bdrempel.{0,20}nieuwe\s+cyclus\b', r'\bvanaf.{0,20}achtste\s+dag', r'\bezechi[eë]l\s+43\b'],
        'pad': 'Kennis/typologie/C_tijd/dagen-achtste.md',
    },
    'C_tijd/jaren-veertig': {
        'patterns': [r'\bveertig\s+ja(ar|ren)\b', r'\b40\s+ja(ar|ren)\b', r'\bwoestijn(tijd|periode|jaren)\b', r'\bgeneratie.{0,30}(woestijn|sterft|veertig)', r'\bdavid.{0,20}40\s+jaar', r'\bsalomo.{0,20}40\s+jaar', r'\bjoas.{0,20}40\s+jaar', r'\b(othniel|debora|gideon|eli).{0,30}(rust|richter|jaar)', r'\bezechi[eë]l\s+(4|29)\b', r'\bhebree[eë]n\s+3\b', r'\bps(alm)?\s+95\b'],
        'pad': 'Kennis/typologie/C_tijd/jaren-veertig.md',
    },
    'C_tijd/jaren-vijftig': {
        'patterns': [r'\bvijftigste\s+jaar\b', r'\b50\s+jaar\b', r'\bjubel(jaar)?\b', r'\bvrijheid\s+uitroep', r'\bderor\b', r'\byovel\b', r'\blevit(en|isch).{0,20}50'],
        'pad': 'Kennis/typologie/C_tijd/jaren-vijftig.md',
    },
    'C_tijd/jaren-zeventig': {
        'patterns': [r'\bzeventig\s+ja(ar|ren)\b', r'\b70\s+ja(ar|ren)\b', r'\bbalingschap\b', r'\bbabel.{0,20}70', r'\bjeremia\s+(25|29)\b', r'\bdaniel\s+9[\s:.]?[12]\b', r'\b2\s+kron(ieken)?\s+36\b', r'\btyrus.{0,20}70', r'\bps(alm)?\s+90[\s:.]?10\b'],
        'pad': 'Kennis/typologie/C_tijd/jaren-zeventig.md',
    },
    'C_tijd/cycli-sabbat': {
        'patterns': [r'\bsabbat.?cyclus\b', r'\bsabbat(s)?ritme\b', r'\bweek.?sabbat\b', r'\b(zes|6)\s+dagen.{0,20}(zevende|7e)', r'\bsabbatsjaar.?cyclus\b', r'\bschaling.{0,20}zeven\b', r'\bkosmische\s+sabbat\b'],
        'pad': 'Kennis/typologie/C_tijd/cycli-sabbat.md',
    },
    'C_tijd/cycli-jubel': {
        'patterns': [r'\bjubel.?cyclus\b', r'\b7\s*x\s*7\s*\+\s*1\b', r'\b49\s+jaar\b', r'\bjes(aja)?\s+61\b', r'\bluk(as)?\s+4[\s:.]?(18|19)\b', r'\baangenaam\s+jaar.{0,15}heer'],
        'pad': 'Kennis/typologie/C_tijd/cycli-jubel.md',
    },
    'C_tijd/cycli-feesten': {
        'patterns': [r'\bfeest.?(cyclus|kalender)\b', r'\bdrie\s+pelgrimsfeesten\b', r'\bmo[\'’]ad(im)?\b', r'\bvastgestelde\s+tijd', r'\beerstelingen\s+(feest|offer)', r'\bsjavoeot\b', r'\bsukkot\b', r'\byom\s+kippur\b', r'\byom\s+teruah\b', r'\bbazuinen.?feest\b', r'\bverzoendag\b', r'\bleviticus\s+23\b'],
        'pad': 'Kennis/typologie/C_tijd/cycli-feesten.md',
    },
    'C_tijd/profetisch-zeventig-weken': {
        'patterns': [r'\bzeventig\s+weken\b', r'\bjaarweken\b', r'\b490\s+jaar\b', r'\bdaniel\s+9[\s:.]?(2[4-7])\b', r'\bmashiach.{0,20}nagid', r'\bgezalfde\s+vorst\b', r'\bgruwel.{0,15}verwoesting\b'],
        'pad': 'Kennis/typologie/C_tijd/profetisch-zeventig-weken.md',
    },
    'C_tijd/profetisch-tijden-en-tijden': {
        'patterns': [r'\btijd\s*,?\s*tijden.{0,15}halve\s+tijd\b', r'\b3[\s,.]?5\s+jaar\b', r'\bdrie\s+en\s+een\s+halve\s+jaar\b', r'\b1260\s+dagen\b', r'\b42\s+maanden\b', r'\bdaniel\s+(7[\s:.]?25|12[\s:.]?7)\b', r'\bopenbaring\s+(11|12|13)\b', r'\btwee\s+getuigen\b', r'\bvrouw\s+in\s+(de\s+)?woestijn\b'],
        'pad': 'Kennis/typologie/C_tijd/profetisch-tijden-en-tijden.md',
    },
    'A_entiteit/adam': {
        'patterns': [r'\badam\b', r'\beerste\s+mens\b', r'\blaatste\s+adam\b', r'\bbeeld\s+god\b', r'\b1\s*kor\s+15[\s:.]?(2[1-9]|4[5-9])\b', r'\brom(einen)?\s+5[\s:.]?(1[2-9]|2[01])\b', r'\btypos\b', r'\bzondeval\b', r'\beva.{0,15}zijde\b'],
        'pad': 'Kennis/typologie/A_entiteit/adam.md',
    },
    'A_entiteit/noach': {
        'patterns': [r'\bnoach\b', r'\bark\s+(noach|gen)', r'\bvloed\b', r'\bregenboog\b', r'\b1\s*pet(rus)?\s+3[\s:.]?(2[01])\b', r'\b2\s*pet(rus)?\s+2[\s:.]?5\b', r'\bachtste\s+prediker\b', r'\bantitypon\b'],
        'pad': 'Kennis/typologie/A_entiteit/noach.md',
    },
    'A_entiteit/abraham': {
        'patterns': [r'\babraham\b', r'\bvader\s+(des\s+)?gelo[ov]', r'\bgen(esis)?\s+(12|15|17|22)\b', r'\brom(einen)?\s+4\b', r'\bgal(aten)?\s+(3|4)\b', r'\bisaak.{0,20}(offer|moria)', r'\bmelchizedek\b', r'\bzaad\s+abraham', r'\bgen\s+22[\s:.]?4\b'],
        'pad': 'Kennis/typologie/A_entiteit/abraham.md',
    },
    'A_entiteit/isaak': {
        'patterns': [r'\bisaak\b', r'\bbeloofde\s+zoon\b', r'\bakedah\b', r'\bgen(esis)?\s+22\b', r'\bhebr(ee[eë]n)?\s+11[\s:.]?1[7-9]\b', r'\beliezer.{0,20}rebekka', r'\bbe[eë]r.?sjeba.{0,20}isaak', r'\beniggeboren', r'\blam\s+gods'],
        'pad': 'Kennis/typologie/A_entiteit/isaak.md',
    },
    'A_entiteit/jakob': {
        'patterns': [r'\bjakob\b', r'\bisrael\b', r'\bezau\b', r'\beerstgeboren.{0,20}omkering', r'\bbethel\b', r'\bjakobs\s+ladder\b', r'\bjoh\s+1[\s:.]?51\b', r'\bpni[eë]l\b', r'\bworstel(ing)?\s+god', r'\bnaam(s)?(verandering|wijziging).{0,20}(jakob|israel)', r'\btwaalf\s+zonen\s+jakob\b', r'\bhos(ea)?\s+11[\s:.]?1\b', r'\bmat\s+2[\s:.]?15\b'],
        'pad': 'Kennis/typologie/A_entiteit/jakob.md',
    },
    'A_entiteit/jozef': {
        'patterns': [r'\bjozef\b', r'\bgeliefde\s+zoon\b', r'\bdromer\b', r'\bverkocht.{0,20}(broers|zilver)', r'\bpotifar\b', r'\bfarao.{0,20}jozef', r'\bzeven\s+jaren\s+(overvloed|honger)', r'\bredder.{0,20}volken', r'\bhand(elingen)?\s+7[\s:.]?(9|1[0-6])\b', r'\bjozef.{0,20}(30\s+jaar|dertig)'],
        'pad': 'Kennis/typologie/A_entiteit/jozef.md',
    },
    'A_entiteit/mozes': {
        'patterns': [r'\bmozes\b', r'\bprofeet\s+als\s+m', r'\bdeut(eronomium)?\s+18[\s:.]?1[5-9]\b', r'\bbemiddelaar\b', r'\bwetgever\b', r'\bkoperen\s+slang\b', r'\bjoh\s+3[\s:.]?14\b', r'\bmanna\b', r'\brots.{0,20}water', r'\b1\s*kor(inthe)?\s+10[\s:.]?[1-4]\b', r'\bhebr(ee[eë]n)?\s+3\b', r'\b3\W?fasen.{0,20}mozes', r'\b3\s*x\s*40'],
        'pad': 'Kennis/typologie/A_entiteit/mozes.md',
    },
    'A_entiteit/jozua': {
        'patterns': [r'\bjozua\b', r'\byehoshua\b', r'\biesous\b', r'\bjhwh\s+redt\b', r'\bjordaan(doortocht)?\b', r'\bjericho\b', r'\bvorst.{0,20}leger.{0,20}jhwh\b', r'\bzach(aria)?\s+(3|6)\b', r'\btzemach\b', r'\bspruit\b', r'\bhebr(ee[eë]n)?\s+4[\s:.]?[8-9]\b'],
        'pad': 'Kennis/typologie/A_entiteit/jozua.md',
    },
    'A_entiteit/boaz': {
        'patterns': [r'\bboaz\b', r'\bruth\b', r'\blosser\b', r'\bgo[\'’]el\b', r'\bvier\s+vrouwen.{0,15}mat\s+1\b', r'\bheidense\s+bruid\b', r'\bbethlehem.{0,15}stamboom'],
        'pad': 'Kennis/typologie/A_entiteit/boaz.md',
    },
    'A_entiteit/david': {
        'patterns': [r'\bdavid\b', r'\bzoon\s+(van\s+)?david\b', r'\bdavidisch(e)?\s+verbond\b', r'\b2\s*sam(uel)?\s+7\b', r'\bps(alm)?\s+(22|110)\b', r'\bmashiach\s+ben\s+david\b', r'\beli\s+eli\s+lama\b', r'\bsabachthani\b', r'\btroon.{0,15}david\b', r'\bachtste\s+zoon\s+isa[iï]\b', r'\bbethlehem.{0,15}herder'],
        'pad': 'Kennis/typologie/A_entiteit/david.md',
    },
    'A_entiteit/salomo': {
        'patterns': [r'\bsalomo\b', r'\bshelomoh\b', r'\bvrede(s)?koning\b', r'\btempel.{0,20}bouw', r'\bkoningin\s+(van\s+)?sheba\b', r'\bhooglied\b', r'\bmat\s+12[\s:.]?42\b', r'\bmeer\s+dan\s+salomo\b', r'\b1\s*kn\s+(3|4|6|7|8|10|11)\b'],
        'pad': 'Kennis/typologie/A_entiteit/salomo.md',
    },
    'A_entiteit/elia': {
        'patterns': [r'\belia\b', r'\beliyahu\b', r'\bkarmel\b', r'\bhoreb\b', r'\bvurige\s+wagen\b', r'\bmal(eachi)?\s+4\b', r'\bjohannes\s+doper.{0,20}elia', r'\bverheerlijking', r'\b1\s*kn\s+(17|18|19)\b', r'\b2\s*kn\s+2\b'],
        'pad': 'Kennis/typologie/A_entiteit/elia.md',
    },
    'A_entiteit/elisa': {
        'patterns': [r'\belisa\b', r'\belisha\b', r'\bdubbel(e)?\s+deel\s+geest\b', r'\bna[aä]man\b', r'\bsunamitisch', r'\bweduwe\s+olie\b', r'\bluk(as)?\s+4[\s:.]?27\b', r'\b2\s*kn\s+(2|4|5|6|13)\b'],
        'pad': 'Kennis/typologie/A_entiteit/elisa.md',
    },
    'A_entiteit/jona': {
        'patterns': [r'\bjona\b', r'\bnineve', r'\bteken\s+(van\s+)?jona\b', r'\bdrie\s+dagen.{0,15}vis\b', r'\bmat\s+12[\s:.]?(3[8-9]|4[01])\b', r'\bluk(as)?\s+11[\s:.]?(2[9-9]|3[012])\b'],
        'pad': 'Kennis/typologie/A_entiteit/jona.md',
    },
    'A_entiteit/simson': {
        'patterns': [r'\bsimson\b', r'\bshimshon\b', r'\bnazirefer\b', r'\bnazireeer\b', r'\bdelila\b', r'\bri(chteren)?\s+(13|14|15|16)\b', r'\bfilistijnen.{0,20}simson'],
        'pad': 'Kennis/typologie/A_entiteit/simson.md',
    },
    'A_entiteit/gideon': {
        'patterns': [r'\bgideon\b', r'\bjerubaal\b', r'\b300\s+mannen\b', r'\bvacht.?teken\b', r'\bbazuinen.{0,15}fakkels\b', r'\bri(chteren)?\s+(6|7|8|9)\b', r'\babimelech.{0,20}70\b'],
        'pad': 'Kennis/typologie/A_entiteit/gideon.md',
    },
    'A_entiteit/melchizedek': {
        'patterns': [r'\bmelchizedek\b', r'\bmalki[\s\-]tzedek\b', r'\bsalem\b', r'\bpriester[\s\-]koning\b', r'\bbrood\s+en\s+wijn\s+abraham\b', r'\bps(alm)?\s+110[\s:.]?4\b', r'\bhebr(ee[eë]n)?\s+(5|7)\b', r'\borde\s+(van\s+)?melchizedek\b'],
        'pad': 'Kennis/typologie/A_entiteit/melchizedek.md',
    },
    'A_entiteit/eva': {
        'patterns': [r'\beva\b', r'\bchavah\b', r'\bvrouw\s+uit\s+(zijde|rib)\b', r'\bgen(esis)?\s+(2[\s:.]?2[1-4]|3)\b', r'\b2\s*kor\s+11[\s:.]?3\b', r'\b1\s*tim\s+2[\s:.]?1[34]\b', r'\bef(eze)?\s+5[\s:.]?(3[01]|32)\b', r'\bprotoevangelie\b', r'\bzaad\s+(van\s+)?(de\s+)?vrouw\b'],
        'pad': 'Kennis/typologie/A_entiteit/eva.md',
    },
    'A_entiteit/sara-hagar': {
        'patterns': [r'\bsara\b', r'\bsarai\b', r'\bhagar\b', r'\bismaël\b', r'\bismael\b', r'\bgal(aten)?\s+4[\s:.]?(2[1-9]|3[01])\b', r'\ballegoroumena\b', r'\btwee\s+verbonden\b', r'\bjeruzalem\s+boven\b', r'\bslavin\s+(en\s+)?vrije\b'],
        'pad': 'Kennis/typologie/A_entiteit/sara-hagar.md',
    },
    'A_entiteit/rachab': {
        'patterns': [r'\brachab\b', r'\brahab\b', r'\bjericho.{0,20}hoer', r'\bscharlaken\s+koord\b', r'\bverspieders\s+(joz|jozua)', r'\bjoz(ua)?\s+(2|6)\b', r'\bhebr(ee[eë]n)?\s+11[\s:.]?31\b', r'\bjak(obus)?\s+2[\s:.]?25\b'],
        'pad': 'Kennis/typologie/A_entiteit/rachab.md',
    },
    'A_entiteit/ruth': {
        'patterns': [r'\bruth\b', r'\bmoabietisch\b', r'\bnaomi\b', r'\buw\s+volk.{0,15}mijn\s+volk\b', r'\baren.?rapen\b', r'\bre[\'’]ut\b'],
        'pad': 'Kennis/typologie/A_entiteit/ruth.md',
    },
    'A_entiteit/hannah-maria': {
        'patterns': [r'\bhannah\b', r'\bhanna\b', r'\bmagnificat\b', r'\blofzang\s+(maria|hannah)', r'\b1\s*sam(uel)?\s+(1|2)\b', r'\bluk(as)?\s+1[\s:.]?(4[6-9]|5[0-5])\b', r'\bsamuel.{0,15}geboorte\b'],
        'pad': 'Kennis/typologie/A_entiteit/hannah-maria.md',
    },
    'A_entiteit/kain': {
        'patterns': [r'\bka[iï]n\b', r'\babel\b', r'\bbroedermoord\b', r'\bgen(esis)?\s+4\b', r'\bhebr(ee[eë]n)?\s+11[\s:.]?4\b', r'\b1\s*joh(annes)?\s+3[\s:.]?12\b', r'\bjud(as)?\s+11\b', r'\bweg\s+(van\s+)?ka[iï]n\b'],
        'pad': 'Kennis/typologie/A_entiteit/kain.md',
    },
    'A_entiteit/bileam': {
        'patterns': [r'\bbileam\b', r'\bbalaam\b', r'\bbalak\b', r'\bezel.{0,20}(spreek|drie\s+keer)', r'\bster\s+uit\s+jakob\b', r'\bnum(eri)?\s+(22|23|24|25|31)\b', r'\b2\s*pet(rus)?\s+2[\s:.]?(1[5-6])\b', r'\bjud(as)?\s+11\b', r'\bopenbaring\s+2[\s:.]?14\b', r'\bleer\s+(van\s+)?bileam\b'],
        'pad': 'Kennis/typologie/A_entiteit/bileam.md',
    },
    'A_entiteit/korach': {
        'patterns': [r'\bkorach\b', r'\bkore\b', r'\bdatan\s+(en\s+)?abiram\b', r'\baarde\s+opent.{0,20}(korach|opstand)', r'\baäron(s)?\s+staf\s+bloei', r'\bnum(eri)?\s+(16|17)\b', r'\btegenspraak\s+(van\s+)?korach\b', r'\bjud(as)?\s+11\b'],
        'pad': 'Kennis/typologie/A_entiteit/korach.md',
    },
    # ---- Fase 9: H_contrast (twaalf binaire opposities) ----
    'H_contrast/eerste-laatste-adam': {
        'patterns': [r'\beerste.{0,10}(adam|laatste)', r'\blaatste\s+adam\b', r'\bin\s+adam\b', r'\bin\s+christus\b.{0,30}(allen|leven)', r'\btypos\s+tou\s+mellontos\b', r'\beschatos\s+adam\b', r'\bprotos\s+adam\b', r'\bchoikos\b', r'\bepouranios\b', r'\brom(einen)?\s+5[\s:.]?(1[2-9]|2[01])\b', r'\b1\s*kor(inthe)?\s+15[\s:.]?(2[12]|4[5-9])\b'],
        'pad': 'Kennis/typologie/H_contrast/eerste-laatste-adam.md',
    },
    'H_contrast/twee-bergen-sinai-sion': {
        'patterns': [r'\b(berg\s+)?sina[iï]\b.{0,30}(berg\s+)?sion\b', r'\b(berg\s+)?sion\b.{0,30}(berg\s+)?sina[iï]\b', r'\bhemels\s+jeruzalem\b', r'\bpaneguris\b', r'\bekklesia\s+prototokon\b', r'\bhebr?(ee[eë]n)?\s+12[\s:.]?(1[8-9]|2[0-4])\b', r'\bouk\s+gar\s+proseluthate\b', r'\btastbare\s+berg\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-bergen-sinai-sion.md',
    },
    'H_contrast/twee-bergen-gerizim-ebal': {
        'patterns': [r'\bgerizim\b', r'\beba(a)?l\b', r'\bzegen.{0,15}vloek\b', r'\bvloek.{0,15}zegen\b', r'\bdeut(eronomium)?\s+(11|27|28)\b', r'\bjoz(ua)?\s+8[\s:.]?(3[0-5])\b', r'\barur\b', r'\bgal(aten)?\s+3[\s:.]?(1[0-4])\b', r'\bvloek\s+der\s+wet\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-bergen-gerizim-ebal.md',
    },
    'H_contrast/twee-steden-babel-jeruzalem': {
        'patterns': [r'\bbabylon\b.{0,30}(jeruzalem|hoer|gevallen)', r'\bgevallen\s+gevallen\s+(is\s+)?babylon\b', r'\bnieuw\s+jeruzalem\b', r'\bhoer\s+(van\s+)?babylon\b', r'\bgrote\s+stad\b', r'\bhe\s+polis\s+he\s+megale\b', r'\bopenbaring\s+(11|14|17|18|21)\b', r'\bop\s+(11|14|17|18|21)\b', r'\bgen(esis)?\s+11[\s:.]?[1-9]\b', r'\btoren\s+(van\s+)?babel\b', r'\bpelgrim.{0,15}stad\b', r'\bval\s+(van\s+)?babylon\b', r'\bbabylon.{0,15}(val|gevallen|verwoesting)'],
        'pad': 'Kennis/typologie/H_contrast/twee-steden-babel-jeruzalem.md',
    },
    'H_contrast/twee-steden-sodom-jeruzalem': {
        'patterns': [r'\bsodom\b.{0,30}jeruzalem\b', r'\bjeruzalem\b.{0,30}sodom\b', r'\beze(chiel|chiël)?\s+16\b', r'\bsodom.{0,15}zuster\b', r'\bzuster\s+(van\s+)?sodom\b', r'\bgaon\s+sov\b', r'\bjes(aja)?\s+1[\s:.]?(9|10)\b', r'\bgomorra\b', r'\bopenbaring\s+11[\s:.]?8\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-steden-sodom-jeruzalem.md',
    },
    'H_contrast/twee-verbonden-hagar-sara': {
        'patterns': [r'\bhagar\b.{0,30}sara\b', r'\bsara\b.{0,30}hagar\b', r'\bisma[eë]l\b.{0,30}izaak\b', r'\ballegoroumena\b', r'\bgal(aten)?\s+4[\s:.]?(2[1-9]|3[01])\b', r'\bpaidiske\b', r'\beleuthera\b', r'\bduo\s+diatheka[is]\b', r'\bano\s+ierousalem\b', r'\btwee\s+verbonden\b.{0,30}(hagar|sara)', r'\bgen(esis)?\s+(16|17|21)\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-verbonden-hagar-sara.md',
    },
    'H_contrast/twee-verbonden-oud-nieuw': {
        'patterns': [r'\bnieuw\s+verbond\b', r'\boud\s+verbond\b', r'\btwee\s+verbonden\b', r'\bbrith\s+chadasha\b', r'\bdiatheke\s+kaine\b', r'\bjer(emia)?\s+31\b', r'\bhebr?(ee[eë]n)?\s+8\b', r'\bgramma.{0,10}pneuma\b', r'\b2\s*kor(inthe)?\s+3[\s:.]?(6|7|14)\b', r'\bbloed\s+des\s+nieuwen\s+verbonds\b', r'\bbeter\s+verbond\b', r'\bkreittonos\s+diathekes\b', r'\beze(chiel|chiël)?\s+36[\s:.]?(2[6-7])\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-verbonden-oud-nieuw.md',
    },
    'H_contrast/twee-wegen-smal-breed': {
        'patterns': [r'\bsmalle\s+(weg|poort)\b', r'\bbrede\s+weg\b', r'\bwijde\s+poort\b', r'\bmat(theus|theüs)?\s+7[\s:.]?(1[3-4])\b', r'\bluk(as)?\s+13[\s:.]?(2[3-4])\b', r'\bagonizesthe\b', r'\bstene\s+pule\b', r'\boligoi\b.{0,15}polloi\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-wegen-smal-breed.md',
    },
    'H_contrast/twee-wegen-leven-dood': {
        'patterns': [r'\bkies\s+(dan\s+)?(het\s+)?leven\b', r'\bweg\s+des\s+levens\b', r'\bweg\s+des\s+doods\b', r'\bderech\s+ha-?chajim\b', r'\bdeut(eronomium)?\s+30[\s:.]?(1[5-9]|20)\b', r'\bjer(emia)?\s+21[\s:.]?[89]\b', r'\bjoz(ua)?\s+24[\s:.]?15\b', r'\brom(einen)?\s+6[\s:.]?23\b', r'\bjoh(annes)?\s+5[\s:.]?24\b', r'\bloon\s+van\s+(de\s+)?zonde\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-wegen-leven-dood.md',
    },
    'H_contrast/twee-wegen-wijs-dwaas': {
        'patterns': [r'\bwijs\b.{0,15}\bdwaas\b', r'\bdwaas\b.{0,15}\bwijs\b', r'\bphronimos\b.{0,15}moros\b', r'\bchokhma\b', r'\bksil\b', r'\bspr(euken)?\s+(1|4|9|14|16)\b', r'\bps(alm)?\s+1[\s:.]?[1-6]\b', r'\bpad\s+der\s+rechtvaardigen\b', r'\bweg\s+der\s+goddelozen\b', r'\bmat(theus|theüs)?\s+25[\s:.]?[1-9]\b', r'\btien\s+maagden\b', r'\brots\s+(versus|tegen|of)\s+zand\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-wegen-wijs-dwaas.md',
    },
    'H_contrast/twee-vrouwen-op12-op17': {
        'patterns': [r'\bzon.?vrouw\b', r'\bvrouw\s+(bekleed\s+)?met\s+de\s+zon\b', r'\bhoer\s+(van\s+)?babylon\b', r'\bbruid\s+(van\s+het\s+)?lam\b', r'\bnumphe\s+(tou\s+)?arniou\b', r'\bopenbaring\s+12[\s:.]?[1-9]\b', r'\bopenbaring\s+17[\s:.]?[1-6]\b', r'\bopenbaring\s+(19|21)[\s:.]?[1-9]\b', r'\bdraak.{0,30}vrouw\b', r'\bmeter\s+(ton\s+)?pornon\b'],
        'pad': 'Kennis/typologie/H_contrast/twee-vrouwen-op12-op17.md',
    },
    'H_contrast/oude-nieuwe-schepping': {
        'patterns': [r'\bnieuwe\s+hemel\b.{0,20}nieuwe\s+aarde\b', r'\bshamayim\s+chadashim\b', r'\bkaine\s+ktisis\b', r'\bnieuwe\s+schepping\b', r'\bjes(aja)?\s+65[\s:.]?(1[7-9])\b', r'\bjes(aja)?\s+66[\s:.]?22\b', r'\b2\s*kor(inthe)?\s+5[\s:.]?17\b', r'\bgal(aten)?\s+6[\s:.]?15\b', r'\bopenbaring\s+21[\s:.]?[1-7]\b', r'\bkaina\s+panta\s+poio\b', r'\b2\s*pet(rus)?\s+3[\s:.]?(1[0-3])\b', r'\bgen(esis)?\s+1[\s:.]?1\b.{0,30}openb(aring)?', r'\bpaliggenesia\b'],
        'pad': 'Kennis/typologie/H_contrast/oude-nieuwe-schepping.md',
    },
    # ---- D_taal entry-specific triggers ----
    'D_taal/paronomasie-dabar-devash': {
        'patterns': [r'\bdabar\b.{0,30}\bdevash\b', r'\bdevash\b.{0,30}\bdabar\b', r'\bparonomasie.{0,15}(dabar|devash|honing|woord)', r'\bps(alm)?\s+19[\s:.]?(10|11)\b', r'\bps(alm)?\s+119[\s:.]?103\b', r'\bzoeter dan honing\b'],
        'pad': 'Kennis/typologie/D_taal/paronomasie-dabar-devash.md',
    },
    'D_taal/paronomasie-shalom-shalem': {
        'patterns': [r'\bshalom\b.{0,30}\bshalem\b', r'\bshalem\b.{0,30}\bshalom\b', r'\bparonomasie.{0,15}(shalom|shalem|salem|jeruzalem)', r'\bsalem\b.{0,30}\bjeruzalem\b', r'\bmelchizedek.{0,30}salem\b'],
        'pad': 'Kennis/typologie/D_taal/paronomasie-shalom-shalem.md',
    },
    'D_taal/wortel-chesed': {
        'patterns': [r'\bchesed\b', r'\bgoedertierenheid\b', r'\bverbondstrouw\b', r'\bloving.?kindness\b', r'\bps(alm)?\s+136\b', r'\bwortel.{0,15}chesed\b'],
        'pad': 'Kennis/typologie/D_taal/wortel-chesed.md',
    },
    'D_taal/wortel-tsedek': {
        'patterns': [r'\btsedek\b', r'\btsedakah\b', r'\bgerechtigheid\b.{0,30}wortel\b', r'\bwortel.{0,15}tsedek\b', r'\btzaddik\b'],
        'pad': 'Kennis/typologie/D_taal/wortel-tsedek.md',
    },
    'D_taal/wortel-rua': {
        'patterns': [r'\bruach\b', r'\bpneuma\b.{0,15}wind\b', r'\bwind.{0,15}geest\b', r'\badem.{0,15}geest\b', r'\bwortel.{0,15}ruach\b', r'\bjoh(annes)?\s+3[\s:.]?8\b'],
        'pad': 'Kennis/typologie/D_taal/wortel-rua.md',
    },
    'D_taal/hapax-overzicht': {
        'patterns': [r'\bhapax(\s+legomenon|\s+legomena)?\b', r'\beenmaal\s+voorkomend\s+woord\b', r'\bunieke.{0,15}voorkomen\b', r'\b1\s*x\s*voorkomen', r'\bhapaxen\b'],
        'pad': 'Kennis/typologie/D_taal/hapax-overzicht.md',
    },
    'D_taal/gematria-inventaris': {
        'patterns': [r'\bgematria\b', r'\bletter.?getal.?waarde\b', r'\bnumerieke\s+waarde\s+(van\s+)?(woord|naam|letter)', r'\bopenbaring\s+13[\s:.]?18\b', r'\b666\b.{0,15}(gematria|getal)', r'\bnaam.{0,15}getal\b'],
        'pad': 'Kennis/typologie/D_taal/gematria-inventaris.md',
    },
    'D_taal/polysemie-elohim': {
        'patterns': [r'\belohim\b.{0,30}(meervoud|meerduidig)', r'\bpolysemie.{0,15}elohim\b', r'\bmeervoud\s+van\s+majesteit\b', r'\belohim.{0,30}(rechters|god|goden)', r'\bps(alm)?\s+82\b'],
        'pad': 'Kennis/typologie/D_taal/polysemie-elohim.md',
    },

    # ---- E_structuur entry-specific triggers ----
    'E_structuur/chiasme-ester': {
        'patterns': [r'\bchiasme.{0,15}ester\b', r'\bester.{0,15}chiasme\b', r'\bester.{0,15}structuur\b', r'\bboek\s+ester\s+structuur\b'],
        'pad': 'Kennis/typologie/E_structuur/chiasme-ester.md',
    },
    'E_structuur/chiasme-onze-vader': {
        'patterns': [r'\bchiasme.{0,15}onze\s+vader\b', r'\bonze\s+vader.{0,15}chiasme\b', r'\bonze\s+vader.{0,15}structuur\b', r'\bmat(theus|theüs)?\s+6[\s:.]?(9|1[0-3])\b.{0,30}structuur'],
        'pad': 'Kennis/typologie/E_structuur/chiasme-onze-vader.md',
    },
    'E_structuur/chiasme-leviticus-19': {
        'patterns': [r'\bchiasme.{0,15}lev(iticus)?\s+19\b', r'\blev(iticus)?\s+19[\s:.]?18\b', r'\bnaastenliefde.{0,15}structuur\b', r'\bleviticus.{0,15}middenvers\b'],
        'pad': 'Kennis/typologie/E_structuur/chiasme-leviticus-19.md',
    },
    'E_structuur/chiasme-narratief-jona': {
        'patterns': [r'\bchiasme.{0,15}jona\b', r'\bjona.{0,15}chiasme\b', r'\bjona.{0,15}structuur\b', r'\bjona.{0,15}narratief\s+structuur\b'],
        'pad': 'Kennis/typologie/E_structuur/chiasme-narratief-jona.md',
    },
    'E_structuur/parallellismen-psalmen': {
        'patterns': [r'\bparallellisme[ns]?\b.{0,30}psalmen\b', r'\bsynoniem.{0,15}parallel\b', r'\bantithetisch.{0,15}parallel\b', r'\bsynthetisch.{0,15}parallel\b', r'\bpoetisch.{0,15}parallel\b'],
        'pad': 'Kennis/typologie/E_structuur/parallellismen-psalmen.md',
    },
    'E_structuur/inclusio-mattheus': {
        'patterns': [r'\binclusio.{0,15}mat(theus|theüs)?\b', r'\bemmanuel.{0,30}(begin|eind)', r'\bmat(theus|theüs)?\s+(1[\s:.]?23|28[\s:.]?20)\b', r'\bgod\s+met\s+ons.{0,30}einde'],
        'pad': 'Kennis/typologie/E_structuur/inclusio-mattheus.md',
    },
    'E_structuur/inclusio-genesis-openbaring': {
        'patterns': [r'\binclusio.{0,15}(genesis|gen)\b.{0,30}openbaring\b', r'\bgenesis.{0,30}openbaring.{0,30}(boom|paradijs|hemel)', r'\bparadijs.{0,30}herstel\b', r'\bhemel\s+en\s+aarde.{0,30}(begin|eind)'],
        'pad': 'Kennis/typologie/E_structuur/inclusio-genesis-openbaring.md',
    },
    'E_structuur/inclusio-johannes-romeinen': {
        'patterns': [r'\binclusio.{0,15}(johannes|joh)\b', r'\binclusio.{0,15}(romeinen|rom)\b', r'\bjohannes.{0,30}(begin|eind).{0,30}structuur\b', r'\bromeinen.{0,30}(begin|eind).{0,30}structuur\b'],
        'pad': 'Kennis/typologie/E_structuur/inclusio-johannes-romeinen.md',
    },
    'E_structuur/tabernakel-hemels-patroon': {
        'patterns': [r'\btabernakel.{0,30}hemels(\s+patroon)?\b', r'\bhebreen?\s+8[\s:.]?5\b', r'\bschaduw.{0,15}hemels\b', r'\bhemels\s+heiligdom\b', r'\bsanctuary.{0,15}heaven\b'],
        'pad': 'Kennis/typologie/E_structuur/tabernakel-hemels-patroon.md',
    },
    'E_structuur/feest-cyclus-heilshistorie': {
        'patterns': [r'\bfeestcyclus\b', r'\bfeest.?cyclus\b', r'\bisra[eë]l(itisch)?e?\s+feesten\b', r'\blev(iticus)?\s+23\b', r'\bpasen.{0,15}pinksteren.{0,15}loofhutten\b', r'\bheilshistorie.{0,15}feest'],
        'pad': 'Kennis/typologie/E_structuur/feest-cyclus-heilshistorie.md',
    },
    'E_structuur/acrostichon-alefbet': {
        'patterns': [r'\bacrostichon\b', r'\balfabetisch.{0,15}(psalm|gedicht)\b', r'\balefbet.{0,15}structuur\b', r'\bps(alm)?\s+(9|10|25|34|37|111|112|119|145)\b.{0,30}structuur', r'\bklaagliederen.{0,30}(structuur|acrostichon)'],
        'pad': 'Kennis/typologie/E_structuur/acrostichon-alefbet.md',
    },
    'E_structuur/refrein-chesed-ps136': {
        'patterns': [r'\bps(alm)?\s+136\b', r'\bzijn\s+goedertierenheid.{0,30}eeuwig\b', r'\brefrein.{0,15}chesed\b', r'\bgrote\s+halleel\b'],
        'pad': 'Kennis/typologie/E_structuur/refrein-chesed-ps136.md',
    },
    'E_structuur/getals-formule-x-en-x-plus-1': {
        'patterns': [r'\bgetals?.?formule\b', r'\b(drie|zes)\s+(en|of)\s+(vier|zeven)\b', r'\bspr(euken)?\s+(6[\s:.]?16|30[\s:.]?(15|18|21|29))\b', r'\bamos\s+1[\s:.]?3\b', r'\bx\s+en\s+x\s*\+\s*1\b'],
        'pad': 'Kennis/typologie/E_structuur/getals-formule-x-en-x-plus-1.md',
    },
    'E_structuur/staircase-parallellisme': {
        'patterns': [r'\bstaircase\s+parallel', r'\btrapsgewijs\s+parallel', r'\bclimactisch\s+parallel', r'\bopeenvolgend\s+parallel', r'\bpsalm\s+29\b'],
        'pad': 'Kennis/typologie/E_structuur/staircase-parallellisme.md',
    },
    'E_structuur/zevenvoudige-opbouw': {
        'patterns': [r'\bzevenvoudige\s+opbouw\b', r'\bzeven[\s-]?delige\s+structuur\b', r'\b7\s*delen\s*structuur\b', r'\bopenbaring.{0,30}zeven\s+(zegels|trompetten|schalen)\b.{0,30}structuur'],
        'pad': 'Kennis/typologie/E_structuur/zevenvoudige-opbouw.md',
    },

    # ---- F_verhaal entry-specific triggers ----
    'F_verhaal/opdracht-vervulling-ark': {
        'patterns': [r'\bnoach.{0,30}ark\b.{0,30}(opdracht|gehoorzaam)', r'\bopdracht.{0,15}ark\b', r'\bgen(esis)?\s+6[\s:.]?(13|14|15|16|17|18|19|20|21|22)\b', r'\bnoach.{0,30}gehoorzaamheid\b'],
        'pad': 'Kennis/typologie/F_verhaal/opdracht-vervulling-ark.md',
    },
    'F_verhaal/opdracht-vervulling-tempel': {
        'patterns': [r'\bdavid.{0,30}plan.{0,30}tempel\b', r'\bsalomo.{0,30}bouwt.{0,30}tempel\b', r'\bopdracht.{0,15}tempel\b', r'\b1\s*kron(ieken)?\s+28\b', r'\b2\s*kron(ieken)?\s+(2|3|4|5)\b'],
        'pad': 'Kennis/typologie/F_verhaal/opdracht-vervulling-tempel.md',
    },
    'F_verhaal/profetie-vervulling-bethlehem': {
        'patterns': [r'\bbethlehem.{0,15}profetie\b', r'\bmicha\s+5[\s:.]?2\b', r'\bmat(theus|theüs)?\s+2[\s:.]?(5|6)\b', r'\bgeboorteplaats.{0,15}messias\b', r'\bbethlehem.{0,30}vervulling\b'],
        'pad': 'Kennis/typologie/F_verhaal/profetie-vervulling-bethlehem.md',
    },
    'F_verhaal/profetie-vervulling-cyrus': {
        'patterns': [r'\bcyrus\b.{0,15}(profetie|jesaja)', r'\bjes(aja)?\s+44[\s:.]?28\b', r'\bjes(aja)?\s+45[\s:.]?(1|2|3|4|5)\b', r'\bkores\b', r'\bperzisch.{0,15}koning.{0,15}terugkeer\b'],
        'pad': 'Kennis/typologie/F_verhaal/profetie-vervulling-cyrus.md',
    },
    'F_verhaal/profetie-meervoudig-jes-7-14': {
        'patterns': [r'\bjes(aja)?\s+7[\s:.]?14\b', r'\bachaz.{0,30}(teken|profetie)\b', r'\bmaagd.{0,15}zal\s+zwanger\s+worden\b', r'\bemmanuel\b.{0,30}profetie\b', r'\bmeervoudige\s+vervulling.{0,15}(achaz|messias)'],
        'pad': 'Kennis/typologie/F_verhaal/profetie-meervoudig-jes-7-14.md',
    },
    'F_verhaal/profetie-meervoudig-joel-2': {
        'patterns': [r'\bjo[eë]l\s+2[\s:.]?(28|29|30|31|32)\b', r'\bvroege\s+regen.{0,15}late\s+regen\b', r'\bgeest.{0,15}uitstort.{0,15}vervulling\b', r'\bpinksteren.{0,15}joel\b', r'\bhand(elingen)?\s+2[\s:.]?(16|17|18|19|20|21)\b'],
        'pad': 'Kennis/typologie/F_verhaal/profetie-meervoudig-joel-2.md',
    },
    'F_verhaal/eerstgeborene-omkering': {
        'patterns': [r'\beerstgeborene.{0,15}omkering\b', r'\bjongere\s+(zoon|broer).{0,30}gekozen\b', r'\bka[iï]n\b.{0,30}\babel\b.{0,30}omkering', r'\bezau.{0,30}jakob.{0,30}omkering', r'\bmanasse.{0,30}efraim\b', r'\badonia.{0,30}salomo\b'],
        'pad': 'Kennis/typologie/F_verhaal/eerstgeborene-omkering.md',
    },
    'F_verhaal/drievoudige-herhaling-petrus': {
        'patterns': [r'\bpetrus.{0,30}drie\s+(maal|keer)\b', r'\bpetrus.{0,15}verloochen', r'\bjoh(annes)?\s+(13[\s:.]?38|18[\s:.]?(17|25|27)|21[\s:.]?(15|16|17))\b', r'\bhebt\s+gij\s+mij\s+lief\b', r'\bpetrus.{0,15}herstel\b'],
        'pad': 'Kennis/typologie/F_verhaal/drievoudige-herhaling-petrus.md',
    },
    'F_verhaal/drievoudige-herhaling-bileam': {
        'patterns': [r'\bbileam.{0,30}ezel.{0,30}drie\b', r'\bezel.{0,15}slaan.{0,15}drie\s+keer\b', r'\bnum(eri)?\s+22[\s:.]?(28|29|30|31|32|33)\b', r'\bbileam\s+ezel\b'],
        'pad': 'Kennis/typologie/F_verhaal/drievoudige-herhaling-bileam.md',
    },
    'F_verhaal/drievoudige-herhaling-samuel': {
        'patterns': [r'\bsamuel.{0,30}drie\s+keer\s+geroepen\b', r'\b1\s*sam(uel)?\s+3[\s:.]?(4|5|6|7|8|9|10)\b', r'\bspreek\s+heer\s+uw\s+knecht\s+hoort\b'],
        'pad': 'Kennis/typologie/F_verhaal/drievoudige-herhaling-samuel.md',
    },
    'F_verhaal/reis-en-terugkeer-jakob': {
        'patterns': [r'\bjakob.{0,30}laban.{0,30}terugkeer\b', r'\bjakob.{0,30}haran.{0,30}terug\b', r'\bjakob\s+vlucht.{0,15}terug\b', r'\bbethel.{0,30}terug\b', r'\bgen(esis)?\s+(28|31|32|35)\b'],
        'pad': 'Kennis/typologie/F_verhaal/reis-en-terugkeer-jakob.md',
    },
    'F_verhaal/reis-en-terugkeer-jozef': {
        'patterns': [r'\bjozef.{0,30}egypte.{0,30}gebeente.{0,30}terug\b', r'\bjozef.{0,30}beloften.{0,30}gebeente\b', r'\bgen(esis)?\s+50[\s:.]?(24|25|26)\b', r'\bex(odus)?\s+13[\s:.]?19\b', r'\bjoz(ua)?\s+24[\s:.]?32\b'],
        'pad': 'Kennis/typologie/F_verhaal/reis-en-terugkeer-jozef.md',
    },
    'F_verhaal/reis-en-terugkeer-jezus': {
        'patterns': [r'\bjezus.{0,30}egypte.{0,30}terug\b', r'\buit\s+egypte\s+heb\s+ik\s+mijn\s+zoon\s+geroepen\b', r'\bmat(theus|theüs)?\s+2[\s:.]?(13|14|15|19|20|21)\b', r'\bhos(ea)?\s+11[\s:.]?1\b'],
        'pad': 'Kennis/typologie/F_verhaal/reis-en-terugkeer-jezus.md',
    },
    'F_verhaal/verschijning-aan-verlatene-hagar': {
        'patterns': [r'\bhagar.{0,30}engel.{0,30}woestijn\b', r'\bgen(esis)?\s+(16|21)[\s:.]?(7|8|9|10|11|12|13|17|18|19)\b', r'\bel-roi\b', r'\bgij\s+zijt\s+een\s+god\s+die\s+ziet\b'],
        'pad': 'Kennis/typologie/F_verhaal/verschijning-aan-verlatene-hagar.md',
    },
    'F_verhaal/verschijning-aan-verlatene-jakob': {
        'patterns': [r'\bjakob.{0,30}bethel.{0,30}droom\b', r'\bgen(esis)?\s+28[\s:.]?(10|11|12|13|14|15|16|17|18|19)\b', r'\bladder\s+naar\s+(de\s+)?hemel\b', r'\bjakob.{0,30}peniel\b', r'\bgen(esis)?\s+32[\s:.]?(24|25|26|27|28|29|30)\b'],
        'pad': 'Kennis/typologie/F_verhaal/verschijning-aan-verlatene-jakob.md',
    },
    'F_verhaal/verschijning-aan-verlatene-mozes': {
        'patterns': [r'\bmozes.{0,30}braamstruik\b', r'\bbrandende\s+braamstruik\b', r'\bex(odus)?\s+3[\s:.]?(1|2|3|4|5|6)\b', r'\bik\s+ben\s+die\s+ik\s+ben\b', r'\bjhwh.{0,30}roep.{0,30}mozes\b'],
        'pad': 'Kennis/typologie/F_verhaal/verschijning-aan-verlatene-mozes.md',
    },
    'F_verhaal/verschijning-aan-verlatene-maria': {
        'patterns': [r'\bmaria.{0,30}graf.{0,30}opstanding\b', r'\bmaria\s+magdalena.{0,30}jezus\b', r'\bjoh(annes)?\s+20[\s:.]?(11|12|13|14|15|16|17|18)\b', r'\brabboeni\b', r'\bopstandingsmorgen.{0,15}maria\b'],
        'pad': 'Kennis/typologie/F_verhaal/verschijning-aan-verlatene-maria.md',
    },

    # ---- G_rol entry-specific triggers ----
    'G_rol/drie-ambten-profeet': {
        'patterns': [r'\bprofeet.{0,15}als\s+mij\b', r'\bdeut(eronomium)?\s+18[\s:.]?(15|18|19)\b', r'\bmozes.{0,30}christus.{0,30}profeet\b', r'\bhand(elingen)?\s+(3[\s:.]?22|7[\s:.]?37)\b', r'\bambt\s+van\s+profeet\b'],
        'pad': 'Kennis/typologie/G_rol/drie-ambten-profeet.md',
    },
    'G_rol/drie-ambten-priester': {
        'patterns': [r'\bambt.{0,15}priester\b', r'\bmelchizedek.{0,30}priester\b', r'\bhebr?(een|eeën)?\s+(5|6|7)\b', r'\baaron.{0,15}priester\b', r'\bhogepriester.{0,15}christus\b'],
        'pad': 'Kennis/typologie/G_rol/drie-ambten-priester.md',
    },
    'G_rol/drie-ambten-koning': {
        'patterns': [r'\bambt.{0,15}koning\b', r'\bdavid.{0,30}christus.{0,30}koning\b', r'\bzoon\s+van\s+david\b', r'\bps(alm)?\s+(2|110)\b', r'\bzetel.{0,15}david\b'],
        'pad': 'Kennis/typologie/G_rol/drie-ambten-koning.md',
    },
    'G_rol/drie-ambten-samenval': {
        'patterns': [r'\bdrie\s+ambten.{0,15}samen\b', r'\bprofeet\s+priester\s+koning\b', r'\bchristus.{0,30}drie\s+ambt', r'\bsamenval.{0,15}ambten\b'],
        'pad': 'Kennis/typologie/G_rol/drie-ambten-samenval.md',
    },
    'G_rol/vader-zoon-abraham-isaak': {
        'patterns': [r'\babraham.{0,15}isaak.{0,30}offer\b', r'\bgen(esis)?\s+22\b', r'\bakeda\b', r'\bbinding\s+(van\s+)?isaak\b', r'\bvader.{0,15}zoon.{0,30}(abraham|moria)\b'],
        'pad': 'Kennis/typologie/G_rol/vader-zoon-abraham-isaak.md',
    },
    'G_rol/vader-zoon-david-salomo': {
        'patterns': [r'\bdavid.{0,30}salomo.{0,15}opvolg', r'\b2\s*sam(uel)?\s+7[\s:.]?(12|13|14|15|16)\b', r'\bzaad\s+(van\s+)?david\b', r'\bdavidisch\s+verbond\b'],
        'pad': 'Kennis/typologie/G_rol/vader-zoon-david-salomo.md',
    },
    'G_rol/broer-broer-kain-abel': {
        'patterns': [r'\bka[iï]n.{0,15}abel\b', r'\bgen(esis)?\s+4[\s:.]?(1|2|3|4|5|6|7|8|9|10|11)\b', r'\bbroedermoord\b', r'\bhebr?(een|eeën)?\s+(11[\s:.]?4|12[\s:.]?24)\b', r'\b1\s*joh(annes)?\s+3[\s:.]?12\b'],
        'pad': 'Kennis/typologie/G_rol/broer-broer-kain-abel.md',
    },
    'G_rol/broer-broer-ezau-jakob': {
        'patterns': [r'\bezau.{0,15}jakob\b', r'\bjakob.{0,15}ezau\b', r'\beerstgeboorterecht\b', r'\bgen(esis)?\s+(25|27|32|33)\b', r'\brom(einen)?\s+9[\s:.]?(11|12|13)\b'],
        'pad': 'Kennis/typologie/G_rol/broer-broer-ezau-jakob.md',
    },
    'G_rol/broer-broer-jozef-elf': {
        'patterns': [r'\bjozef.{0,15}broers\b', r'\bgen(esis)?\s+(37|42|43|44|45|50)\b', r'\bjozef.{0,15}verkocht\b', r'\bjozef.{0,15}vergeven\b', r'\bhand(elingen)?\s+7[\s:.]?(9|10|11|12|13|14)\b'],
        'pad': 'Kennis/typologie/G_rol/broer-broer-jozef-elf.md',
    },
    'G_rol/bruidegom-bruid-jhwh-israel': {
        'patterns': [r'\bjhwh.{0,15}bruidegom\b', r'\bisra[eë]l.{0,15}bruid\b', r'\bhos(ea)?\s+(1|2|3)\b', r'\bjer(emia)?\s+2[\s:.]?(2|3)\b', r'\bovertrouwde\s+vrouw\b', r'\beze(chiel|chiël)?\s+16\b'],
        'pad': 'Kennis/typologie/G_rol/bruidegom-bruid-jhwh-israel.md',
    },
    'G_rol/bruidegom-bruid-christus-gemeente': {
        'patterns': [r'\bchristus.{0,15}bruidegom\b', r'\bgemeente.{0,15}bruid\b', r'\bef(eze|eziërs)?\s+5[\s:.]?(22|23|24|25|26|27|28|29|30|31|32)\b', r'\bopenbaring\s+(19|21)[\s:.]?(7|9|10)\b', r'\bbruiloft\s+(van\s+het\s+)?lam\b'],
        'pad': 'Kennis/typologie/G_rol/bruidegom-bruid-christus-gemeente.md',
    },
    'G_rol/herder-schaap': {
        'patterns': [r'\bgoede\s+herder\b', r'\bps(alm)?\s+23\b', r'\beze(chiel|chiël)?\s+34\b', r'\bjoh(annes)?\s+10[\s:.]?(1|2|3|11|14|15|16)\b', r'\bdavid.{0,15}herder\b', r'\bschapen.{0,15}stem\b'],
        'pad': 'Kennis/typologie/G_rol/herder-schaap.md',
    },
    'G_rol/knecht-heer-eliezer': {
        'patterns': [r'\beliezer.{0,30}rebekka\b', r'\bgen(esis)?\s+24\b', r'\bknecht.{0,15}abraham.{0,15}rebekka\b', r'\beliezer.{0,15}geest', r'\bbruidwerver\b'],
        'pad': 'Kennis/typologie/G_rol/knecht-heer-eliezer.md',
    },
    'G_rol/knecht-heer-mozes': {
        'patterns': [r'\bmozes.{0,15}knecht\s+des\s+heren\b', r'\bmozes.{0,15}eved\b', r'\bdeut(eronomium)?\s+34[\s:.]?5\b', r'\bjoz(ua)?\s+1[\s:.]?(1|2|13|15)\b', r'\bnum(eri)?\s+12[\s:.]?(7|8)\b'],
        'pad': 'Kennis/typologie/G_rol/knecht-heer-mozes.md',
    },
    'G_rol/knecht-heer-christus': {
        'patterns': [r'\bjes(aja)?\s+(42|49|50|52|53)\b', r'\blijdende\s+knecht\b', r'\bebed\s+jhwh\b', r'\bservant\s+songs\b', r'\bfil(ippenzen|ippiërs)?\s+2[\s:.]?(5|6|7|8|9|10|11)\b', r'\bchristus.{0,15}gestalte\s+van\s+een\s+slaaf\b'],
        'pad': 'Kennis/typologie/G_rol/knecht-heer-christus.md',
    },
}

# Algemene categorie-triggers die wijzen op relevantie van een hele
# typologie-categorie, ook als geen specifieke entry nog bestaat.
TYPOLOGIE_CATEGORIE_SIGNALEN = {
    'A_entiteit': [r'\b(adam|noach|abraham|isaak|jakob|jozef|mozes|jozua|david|salomo|elia|elisa|jona|simson|gideon|boaz|melchizedek)\b', r'\b(berg|jordaan|jeruzalem|babel|sion|moria)\b', r'\b(ark|kandelaar|tabernakel|tempel)\b'],
    'B_cijfer': [r'\b(drie|zeven|acht|tien|twaalf|veertig|vijftig|zeventig|honderdtwintig|honderdvierenveertig)\b', r'\b(3|7|8|10|12|40|50|70|120|144|153|666|1000)\b'],
    'C_tijd': [r'\b(eerste|tweede|derde|vierde|vijfde|zesde|zevende|achtste)\s+dag\b', r'\bsabbat\b', r'\bjubel', r'\bzeventig (jaar)?weken\b', r'\bmillenni'],
    'D_taal': [r'\bgrondtekst\b', r'\bhebreeuws\b', r'\bgrieks\b', r'\bgematria\b', r'\bwoordklank', r'\bparonomasi'],
    'E_structuur': [r'\bchiasm', r'\bparallel', r'\binclusio\b', r'\btabernakel\b', r'\bfeest', r'\bopenbaring'],
    'F_verhaal': [r'\bopdracht\b', r'\bprofeti', r'\beerstgeboren', r'\bverschijning'],
    'G_rol': [r'\bprofeet\b', r'\bpriester\b', r'\bkoning\b', r'\bbruidegom\b', r'\bherder\b', r'\bknecht\b'],
    'H_contrast': [r'\beerste.{1,10}laatste\b', r'\boude.{1,10}nieuwe\b', r'\btwee\s+(berg|verbond|stad|vrouw)'],
}


def detect_chronologie(vraag):
    q = vraag.lower()
    for p in CHRONO_PATTERNS:
        if re.search(p, q):
            return True
    return False


def detect_externe_tradities(vraag):
    q = vraag.lower()
    relevant = []
    for naam, patterns in EXTERNE_TRADITIES_VRAAGSIGNALEN.items():
        for p in patterns:
            if re.search(p, q):
                relevant.append(naam)
                break
    return relevant


def detect_typologie_entries(vraag):
    """Detecteert welke specifieke typologie-entries relevant zijn voor de vraag."""
    q = vraag.lower()
    geactiveerd = []
    for naam, conf in TYPOLOGIE_TRIGGERS.items():
        for p in conf['patterns']:
            if re.search(p, q):
                geactiveerd.append({'entry': naam, 'pad': conf['pad']})
                break
    return geactiveerd


def detect_typologie_categorieen(vraag):
    """Detecteert welke typologie-categorieën als hele groep relevant zijn,
    ook waar geen specifieke entry nog bestaat. Gebruikt voor bredere activatie
    en om openstaande categorieën te signaleren."""
    q = vraag.lower()
    geactiveerd = []
    for cat, patterns in TYPOLOGIE_CATEGORIE_SIGNALEN.items():
        for p in patterns:
            if re.search(p, q):
                geactiveerd.append(cat)
                break
    return geactiveerd


def run_interview(vraag):
    try:
        proc = subprocess.run(
            ['python3', INTERVIEW_SCRIPT, '--infer', vraag, '--confirm', '--json'],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.stdout.strip():
            return json.loads(proc.stdout.strip())
    except Exception as e:
        return {'error': str(e), 'language': 'unknown', 'output_type': 'unknown', 'depth': 'unknown', 'missing': ['language', 'output_type', 'depth']}
    return {'language': 'unknown', 'output_type': 'unknown', 'depth': 'unknown', 'missing': ['language', 'output_type', 'depth']}


def detect_vers_referenties(vraag):
    pattern = r'\b([1-3]?\s*[a-z]{2,4})[\s\.]+(\d+)[:.](\d+)(?:\s*[-–,]\s*\d+)?\b'
    matches = re.findall(pattern, vraag.lower())
    return [{'boek': m[0].replace(' ', '').lower(), 'hoofdstuk': int(m[1]), 'vers': int(m[2])} for m in matches]


def bouw_bronnen_manifest(is_chronologie, vers_refs, typologie_entries=None, typologie_categorieen=None):
    manifest = {
        'grondtekst': [],
        'diepte': [],
        'index': [],
        'vertaal': [],
        'lxx': [],
        'protocollen': [],
        'typologie': [],
    }
    if is_chronologie:
        for boek in ['gen', 'exo', '1kg', '2kg', '2ch', 'eze', 'jer', 'dan', 'act', 'gal']:
            manifest['grondtekst'].append(f'Kennis/strong/{boek}.jsonl')
        manifest['vertaal'].append('Kennis/concordant-nl-hebreeuws.json')
        manifest['vertaal'].append('Kennis/concordant-nl-grieks.json')
        manifest['protocollen'].append('Kennis/protocollen/chronologie.md')
        manifest['protocollen'].append('Kennis/protocollen/interpretatieve-keuzes.md')
        manifest['protocollen'].append('Kennis/protocollen/typologie-detectie.md')
    for ref in vers_refs:
        boek = ref['boek']
        path = f'Kennis/strong/{boek}.jsonl'
        if path not in manifest['grondtekst']:
            manifest['grondtekst'].append(path)
        path_puur = f'Kennis/puur/{boek}.jsonl'
        if path_puur not in manifest['grondtekst']:
            manifest['grondtekst'].append(path_puur)
    if typologie_entries:
        for e in typologie_entries:
            manifest['typologie'].append(e['pad'])
    if typologie_categorieen:
        manifest['typologie'].append('Kennis/typologie/_raamwerk.md')
        manifest['typologie'].append('Kennis/typologie/_entry-sjabloon.md')
    return manifest


def bouw_poort_rapport(interview, manifest):
    poorten = {}
    if interview.get('missing'):
        poorten['poort_1_interview'] = {
            'status': 'DICHT',
            'reden': f"Dimensies onbekend: {', '.join(interview['missing'])}",
            'actie': 'Stel de gebruiker de ontbrekende vragen voordat output wordt geproduceerd.',
            'confirm_prompt': interview.get('confirm_prompt'),
        }
    else:
        poorten['poort_1_interview'] = {
            'status': 'OPEN-NA-BEVESTIGING',
            'reden': 'Alle dimensies geïnferd, gebruiker moet bevestigen.',
            'confirm_prompt': interview.get('confirm_prompt'),
        }
    totaal = sum(len(v) for v in manifest.values())
    if totaal == 0:
        poorten['poort_2_bronnen_manifest'] = {
            'status': 'DICHT',
            'reden': 'Geen bronnen geïdentificeerd. Vraag is mogelijk niet duidelijk genoeg.',
            'actie': 'Vraag de gebruiker om verduidelijking of een specifieke vers-referentie.',
        }
    else:
        poorten['poort_2_bronnen_manifest'] = {
            'status': 'OPEN',
            'reden': f'{totaal} bron-bestanden geïdentificeerd.',
            'manifest': manifest,
        }
    poorten['poort_3_anti_geheugen'] = {
        'status': 'OPEN',
        'reden': 'Eed geactiveerd: alle uitspraken worden gemarkeerd als bronnen-afgeleid of [EXTERN]/[ONBEKEND].',
        'eed': 'Geen cijfer, citaat, kruisreferentie of interpretatie zonder herleidbare bron of expliciete markering. Geen training-bias als default; bron-weging via interpretatieve-keuzes.md.',
    }
    return poorten


def bepaal_aanbeveling(is_chronologie, externe_tradities, typologie_entries, typologie_categorieen, poorten):
    a = []
    if poorten['poort_1_interview']['status'].startswith('DICHT'):
        a.append('STOP: vraag eerst de interview-dimensies aan de gebruiker.')
    if poorten['poort_2_bronnen_manifest']['status'].startswith('DICHT'):
        a.append('STOP: vraag verduidelijking; geen bronnen kunnen worden geïdentificeerd.')
    if is_chronologie:
        a.append('CHRONOLOGIE-PROTOCOL ACTIEF: lees Kennis/protocollen/chronologie.md en volg stappen C1 t/m C7.')
        a.append('VERPLICHT: pas alle 7 interpretatieve keuzepunten toe via bron-weging uit interpretatieve-keuzes.md.')
        a.append('VERPLICHT: NT-OT cross-references (Hand 7:2-3, Hand 7:4, Gal 3:17) zijn dwingend, niet optioneel.')
        a.append('VERPLICHT: stop bij laatste binnen-bijbelse anker, markeer BC/AD-conversie als externe ankering.')
        a.append('VERBODEN: leeshoeken-pluralisme als verkapt diplomatieke positie; werk-conclusies trekken op basis van bron-weging.')
        if externe_tradities:
            a.append(f'EXTERNE TRADITIES VERMELD IN VRAAG: {", ".join(externe_tradities)} - vermelden als context, niet als alternatieve leeshoek.')
    if typologie_entries:
        entries_lijst = ', '.join(e['entry'] for e in typologie_entries)
        a.append(f'TYPOLOGIE-LAAG ACTIEF (mode passief): laad entries [{entries_lijst}] en presenteer als coherentie-watermerk in Blok C en Blok E.')
    if typologie_categorieen:
        cat_lijst = ', '.join(typologie_categorieen)
        a.append(f'TYPOLOGIE-CATEGORIEEN GERAAKT: {cat_lijst}. Als geen specifieke entry voor de vraag bestaat: signaleer aan gebruiker als kandidaat voor onderzoek-sessie (mode actief).')
    if not a:
        a.append('Alle poorten open. Ga door met Stap 2 (vers- of Strong-resolutie).')
    return a


def format_rapport(r):
    lines = []
    lines.append("=" * 70)
    lines.append("PRE-FLIGHT RAPPORT - godstruegospel skill v5.2")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Vraag: {r['vraag']}")
    lines.append("")
    lines.append(f"Chronologie-vraag: {r['is_chronologie_vraag']}")
    lines.append(f"Externe tradities in vraag: {', '.join(r['externe_tradities_in_vraag']) or '(geen)'}")
    lines.append(f"Vers-referenties: {len(r['vers_referenties_gedetecteerd'])}")
    lines.append(f"Typologie-entries geactiveerd: {', '.join(e['entry'] for e in r.get('typologie_entries_geactiveerd', [])) or '(geen)'}")
    lines.append(f"Typologie-categorieen geraakt: {', '.join(r.get('typologie_categorieen_geactiveerd', [])) or '(geen)'}")
    lines.append("")
    lines.append("INTERVIEW:")
    iv = r['interview']
    lines.append(f"  taal: {iv.get('language')} | type: {iv.get('output_type')} | diepte: {iv.get('depth')}")
    if iv.get('missing'):
        lines.append(f"  MISSEND: {', '.join(iv['missing'])}")
    if iv.get('confirm_prompt'):
        lines.append("")
        lines.append("  Bevestigingsvraag voor gebruiker:")
        for ln in iv['confirm_prompt'].split("\n"):
            lines.append(f"  {ln}")
    lines.append("")
    if r.get('interpretatieve_keuzepunten'):
        lines.append("INTERPRETATIEVE KEUZEPUNTEN (toepassen via bron-weging):")
        for kp in r['interpretatieve_keuzepunten']:
            lines.append(f"  - {kp}")
        lines.append("")
    lines.append("POORTEN:")
    for naam, data in r['poorten'].items():
        lines.append(f"  {naam}: {data['status']}")
        lines.append(f"    {data.get('reden', '')}")
    lines.append("")
    lines.append("AANBEVELING:")
    for x in r['aanbeveling']:
        lines.append(f"  - {x}")
    lines.append("=" * 70)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vraag', required=True)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--enforce', action='store_true')
    args = parser.parse_args()

    is_chronologie = detect_chronologie(args.vraag)
    externe_tradities = detect_externe_tradities(args.vraag)
    vers_refs = detect_vers_referenties(args.vraag)
    typologie_entries = detect_typologie_entries(args.vraag)
    typologie_categorieen = detect_typologie_categorieen(args.vraag)
    if is_chronologie:
        for c in ['B_cijfer', 'C_tijd']:
            if c not in typologie_categorieen:
                typologie_categorieen.append(c)
    interview = run_interview(args.vraag)
    manifest = bouw_bronnen_manifest(is_chronologie, vers_refs, typologie_entries, typologie_categorieen)
    poorten = bouw_poort_rapport(interview, manifest)

    rapport = {
        'vraag': args.vraag,
        'is_chronologie_vraag': is_chronologie,
        'externe_tradities_in_vraag': externe_tradities,
        'vers_referenties_gedetecteerd': vers_refs,
        'typologie_entries_geactiveerd': typologie_entries,
        'typologie_categorieen_geactiveerd': typologie_categorieen,
        'interpretatieve_keuzepunten': INTERPRETATIEVE_KEUZEPUNTEN_BIJ_CHRONOLOGIE if is_chronologie else [],
        'interview': interview,
        'voorlopig_bronnen_manifest': manifest,
        'poorten': poorten,
        'aanbeveling': bepaal_aanbeveling(is_chronologie, externe_tradities, typologie_entries, typologie_categorieen, poorten),
    }

    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
    else:
        print(format_rapport(rapport))

    if args.enforce:
        for d in poorten.values():
            if d['status'] == 'DICHT':
                sys.exit(1)


if __name__ == '__main__':
    main()
