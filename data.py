"""Source tables for The World Daily, Sunday 22 November 2026."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Story:
    region: str
    place: str
    kicker: str
    headline: str
    detail: str
    status: str
    glyph: str
    source: str


def S(region, place, kicker, headline, detail, status, glyph, source):
    return Story(region, place, kicker, headline, detail, status, glyph, source)


# Ordered by page prominence: four illustrated leads, then the editorial wells.
STORIES = [
 S("EUROPE","Antalya, Turkey","CLIMATE","COP31 ends with no deal: the Antalya collapse","44h overrun · first failed COP since 2009","C","alert","Reuters · BBC · Guardian"),
 S("MIDDLE EAST","Black Sea","WAR AT SEA","Russian corvette Berberus sunk in the Black Sea","drone strike suspected · Kyiv has not commented","R","flag","Black Sea Fleet · AP · Naval News"),
 S("EUROPE","Kyiv, Ukraine","AIR WAR","Drone strike guts an apartment block in Kyiv","at least 2 dead · 14 unaccounted · 4 wounded","C","drone","Zelensky · Tkachenko · BBC"),
 S("EUROPE","Budapest, Hungary","ELECTION","Hosszú wins Hungary's election in a sharp turn","opposition takes the vote · Fidesz concedes","C","ballot","Hungarian election office · AP"),
 S("LATIN AMERICA","Sinaloa, Mexico","CAPTURE","Mexico seizes an FBI top-ten fugitive in Sinaloa","special-forces raid · Meza Flores, 10+ yrs on run","C","block","Reuters · AP · Ahram"),
 S("MIDDLE EAST","Khartoum corridor","SHIPPING","US strike hits a 64.5m-tonne tanker bound for Europe","off Khartoum corridor · Washington cites sanctions","R","tanker","US military · Reuters · Lloyd's List"),
 S("AFRICA","Khartoum, Sudan","CIVILIAN WAR","RSF drones hit Khartoum homes and a UN building","4 dead · drones ≈3/4 of Sudan war deaths this yr","C","drone","Reuters · EastAfrican · UN"),
 S("SOUTH & EAST ASIA","Shenzhen, China","DIPLOMACY","Xi, Trump, Putin sign 'declaration toward peace'","first trilateral summit · Shenzhen, 19 Nov","C","bridge","Xinhua · China Daily"),
 S("MIDDLE EAST","West Bank","SETTLER VIOLENCE","Settlers set cars and homes alight in four villages","≈8 vehicles torched · Eisenkot: 'terrorism'","C","house","AFP · Al Arabiya · ToI"),
 S("EUROPE","Ukraine","ENERGY","Russian strike leaves 5 oblasts on emergency power cuts","Dnipro: 1 woman dead, 9 hurt · 186 drones fired","C","power","Ukrenergo · Kyiv Post · UA AF"),
 S("EUROPE","Finnish waters","SHIPPING","Russian cargo ship burns, drifts into Finnish waters","suspected Ukrainian drone strike · crew safe","C","snow","Reuters · BBC"),
 S("EUROPE","Bratislava, Slovakia","EUROPE","Fico refuses Slovakia's share of the €45bn Ukraine loan","keeps humanitarian aid · defies Berlin's push","C","money","Fico · Slovak FM"),
 S("EUROPE","Prague, Czechia","BUDGET","Babiš rejects parts of the EU's 2028-34 budget","wants Kyiv funded outside it · CZK 7.5bn cut","R","power","Reuters · Babiš"),
 S("EUROPE","Brussels, Belgium","TAX","Costa proposes a 3% tax on big digital firms","to fund a smaller EU budget · France says no","R","explosion","Costa proposal · DW"),
 S("EUROPE","Moldova","AIRSPACE","Russian drone crossed into Moldova's airspace twice","jet-powered UAV · Troitske and Purcari","C","crash","Moldova MoD"),
 S("EUROPE","Paris, France","MATHEMATICS","AI-written proof of the Riemann hypothesis verified","Alpöge · Lean/Mathlib check · 17M lines of code","R","phone","FRANCE 24 · Meduza"),
 S("NORTH AMERICA","Washington, US","CYBERSECURITY","FBI investigates a hack of its criminal-justice database","same week: USDA hit by a cyberattack","C","eyes","AP · NBC News"),
 S("NORTH AMERICA","Washington, US","OVERSIGHT","Trump orders contractors to clear with the White House","before answering any congressional inquiry","C","alert","AP · Reuters"),
 S("NORTH AMERICA","Doha, Qatar","NUCLEAR TALKS","US and Iran split on enriched uranium, mediator says","Qatar brokers · Trump wants a 'permanent' deal","R","plane","Arab News · Fox · Dawn"),
 S("LATIN AMERICA","Rio Grande do Sul","FLOODS","Rio Grande do Sul floods hit 25,000 in 42 towns","calamity decree for Tupanciretã · 116 mm of rain","C","water","RS Civil Defence"),
 S("LATIN AMERICA","Brasília, Brazil","HEALTH","Bolsonaro in ICU with an obstructive acute abdomen","serving 27 years · no release date given","C","heart","DF Star bulletin · Arab News"),
 S("LATIN AMERICA","Essequibo","BORDER","Trump official urged Guyana to cede part of Essequibo","Caracas–Georgetown standoff goes on","R","bridge","Reuters via Efecto Cocuyo"),
 S("LATIN AMERICA","Falklands","LAW OF SEA","Argentina argues Falklands oil rights at the Law of Sea court","Sea Lion project north of the islands","R","court","MercoPress"),
 S("MIDDLE EAST","Bahrain","RETALIATION","Iran hits a Bahrain industrial facility; 2 hurt","1 Bahraini citizen + 1 Pakistani resident","C","explosion","Bahrain MoFA · Dawn"),
 S("MIDDLE EAST","New York","UN SUCCESSION","Two veto-holding powers block Grynspan for UN chief","Costa Rica's candidate fails a straw poll","R","key","Reuters"),
 S("MIDDLE EAST","Lahj, Yemen","MISSILE","Houthi missile hits a health centre in Lahj, ~10 dead","5 more soldiers killed in southern clashes","R","alert","Soth24"),
 S("MIDDLE EAST","Gaza","GAZA","Gaza toll 74,742; a kitchen car struck, 3 workers dead","6 bodies in 24h · WCK denies current staff ties","C","memory","Gaza MoH · Palestine Chronicle"),
 S("MIDDLE EAST","Neyshabur, Iran","PUBLIC HEALTH","Iran: bootleg alcohol kills 4 and poisons 72 in Neyshabur","12 people arrested over production and sale","R","flask","IRNA / MNA"),
 S("MIDDLE EAST","Berlin, Germany","MIGRATION","AfD's Chrupalla wants up to 2.6m people repatriated","Ukrainians, Syrians, Afghans · legal expiries","R","truck","Chrupalla · DW"),
 S("MIDDLE EAST","Tehran, Iran","POWER","Iran resumes scheduled power cuts as winter bites","fuel supply squeeze · a million jobs at risk","R","power","Tavanir · IRNA"),
 S("MIDDLE EAST","Athens, Greece","DEFENCE","Greek–Israeli €3bn air-defence agreement advances","Elbit training-centre expansion also on table","R","crash","Naharnet"),
 S("MIDDLE EAST","Iran","LABOUR","Truck drivers in several Iranian cities strike","over costs and stagnant freight rates","R","flag","Iranian outlets"),
 S("SOUTH & EAST ASIA","Hong Kong","ELECTION","Hong Kong committee poll: record turnout, 723 seats","856 candidates ran across 31 sectors","C","ballot","China Daily · Xinhua"),
 S("SOUTH & EAST ASIA","Taipei, Taiwan","ELECTION","Taipei mayoral race hits 'Super Sunday', a week out","local elections are the year's last big vote","C","ballot","Focus Taiwan · Taiwan News"),
 S("SOUTH & EAST ASIA","Beijing, China","SPACEFLIGHT","Pakistan's first astronaut heads to Beijing","Ahsan Iqbal arrives for the launch ceremony","C","star","APP"),
 S("SOUTH & EAST ASIA","Haryana, India","EXERCISE","Two Indian soldiers killed by a tank on exercise","Hisar district, Haryana · inquiry opened","C","alert","Indian Express"),
 S("SOUTH & EAST ASIA","Mumbai, India","PRICES","India's inflation hits a record 18.8%","food and fuel surge · household budgets under strain","R","money","India statistics office · Reuters"),
 S("SOUTH & EAST ASIA","Taiwan","CINEMA","63rd Golden Horse Awards: the results","Taiwan's top film prizes handed out","C","star","Focus Taiwan"),
 S("SOUTH & EAST ASIA","Afghanistan","HEALTH","WHO counts 50 polio cases in Afghanistan","Kabul's health ministry disputes the finding","R","flask","TOLOnews"),
 S("SOUTH & EAST ASIA","Myanmar","DIPLOMACY","Myanmar's junta calls ASEAN's decision 'unfair'","as the ICJ Rohingya genocide ruling lands","R","memory","Reuters"),
 S("AFRICA","Pretoria, South Africa","OBITUARY","Mlambo-Ngcuka, S. Africa's first woman deputy president, dies","71 · ex-UN Women head · UN, AU pay tribute","C","memory","UN · allAfrica · UNAIDS"),
 S("AFRICA","Global","HUNGER","WFP asks $12.1bn for 2027 to feed 91 million people","warns millions more will go hungry","C","money","UN · APP"),
 S("AFRICA","Belgrade, Serbia","DIPLOMACY","Beijing signals close ties with Serbia's new government","Student List takes power · China projects under review","R","plane","SCMP"),
 S("AFRICA","Benghazi, Libya","PROXY WAR","Libya warns the port attack risks a proxy war on its soil","Benghazi govt: Libya is not a party to the war","R","ship","Libyan govt · Reuters"),
 S("OCEANIA & POLAR","Deep space","VOYAGER","Voyager 1 passes one light-day from Earth","launched 1977 · still transmitting","C","snow","Dawn"),
 S("OCEANIA & POLAR","Las Vegas, US","FORMULA ONE","Verstappen wins Las Vegas GP: his 75th victory","held off McLaren's Norris in a chaotic race","C","star","AFP"),
 S("OCEANIA & POLAR","California, US","WEATHER","Californian coast pounded by 9-metre swells","coastal hazard warnings all week","C","water","Guardian"),
]

STATUS_ORDER = ["C", "R", "L", "P"]
STATUS_LABEL = {"C": "CONFIRMED", "R": "REPORTED", "L": "CLAIM", "P": "PENDING"}

DATE_CHECK = [
    ("19 Nov", "Shenzhen trilateral summit (Xi–Trump–Putin)", "Asia", "too old"),
    ("20 Nov", "400 drones + 2 missiles enter Poland", "Europe", "too old"),
    ("20 Nov", "Kerch Bridge road span struck", "Europe", "too old"),
    ("21 Nov", "France's sixth weekend of cost-of-living protests", "Europe", "too old"),
    ("21 Nov", "Russia fires 165 missiles in one week", "Europe", "too old"),
]
