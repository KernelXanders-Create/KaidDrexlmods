"""K3: the three swamp concepts at the 9 Nov targets (PROPOSED sketch data).

Row format per site (pipe separated):
  name | role F/M/S | size s/t/p | x km | y km | library code | flags | stake
flags: d destructible, ap air-prep, ao air-only, tun tunnel (library), cap capstone
interior, li library interior, w on water/stilts, v vehicle objective, new part of
a new build, D1..D6 main draw.
Library names come from the Islands purpose map v2 (Miran's library as listed
there); whether each suits a swamp is ASSUMED until Compmaker checks.
"""

LIB = {
    "TR": "CIS Basic Trenchline with GPs", "MT": "CIS Metal Trench Line with GPs",
    "TRN2": "Mrogg trench part 2 (Support weapon)", "FD": "CIS Fuel Depot with GPs",
    "LFD": "CIS Large Fuel Depot with GPs", "AA": "CIS Medium AA Base with GPs",
    "AAC": "Medium Covered AA Base with GPs", "HAD": "CIS Heavy AD Tower with GPs",
    "ART": "CIS Small Artillery Base with GPs", "OP": "CIS Outpost with GPs (D)",
    "ZO": "Zavala CIS Outpost with GPs", "CK": "CIS Small Checkpoint with GPs",
    "DCK": "CIS Double Checkpoint with GPs", "COM": "CIS Comms Array with GPs",
    "RAD": "CIS Big Radio Tower with GPs", "PWR": "CIS Powerbank Facility with GPs",
    "LPWR": "CIS Large Power Facility with GPs", "LOG": "CIS Medium Logistics Base with GPs",
    "VD": "CIS Vehicle Depot with GPs (D)", "DEP": "CIS Depot (Fixed) with GPs (D)",
    "GT": "CIS Guard Tower with GPs", "TT": "CIS Turbolaser Tower with GPs",
    "BUN": "Tukata Turret Bunker", "WB": "Small Wall with Bunker",
    "SHD": "Destructable Shield Generator and its shield template", "MIN": "CIS Mining Complex with GPs",
    "CIT": "CIS Small Citadel with GPs", "FOR": "CIS Mini Fortress with GPs",
    "FF": "CIS Flower Fortress with GPs", "DAM": "CIS Fortress Dam with GPs",
    "LND": "CIS Landing Position with GPs", "TUN": "Royal Tunnel Holdout 1 (Mono)",
    "CAVE": "PLAD Cave Base with Escape", "ELP": "CIS Elevated Landing Pad Construction with GPs",
    "RDR": "Giant Radar Dish", "SR": "Claus - Small Radar", "CSFOB": "CIS Communications FOB with GPs",
    "TOWN": "hand-made town (town work, not a comp)", "NEW1": "NEW build 1 (centerpiece)",
    "NEW2": "NEW build 2 (centerpiece)",
}

# ============================================================== A
A = dict(
    key="A", title="The Mire Line", setting="original mud world (placeholder name; not Mimban)",
    draws={
        "D1": ("The Cauldron Refinery", "NEW 1", "A Droid-Factory-class gas refinery on stilts in a flooded strike crater (about 350 x 300 m), rim and spoil heaps as terrain", "It turns bog gas into droid fuel for the whole front; its flare stacks are seen across the bog"),
        "D2": ("The Moraine Citadel", "NEW 2 + capstone", "A Droid-Factory-class citadel dug into the north moraine; the planet's ONE capstone interior is inside", "The CIS front headquarters; its command galleries run the whole line"),
        "D3": ("The Esker Redoubt", "library cluster", "CIS Mini Fortress + Metal Trench Line + artillery on the only long gravel ridge in the west", "The only firm high ground in the west; its guns command the west bog"),
        "D4": ("The Drain Locks", "library cluster", "CIS Fortress Dam across the Drain + pump house + bunkers", "The lock keeps the CIS trenches drained and its crest road is the only heavy crossing of the Drain"),
        "D5": ("The Peat-Gas Works", "library cluster", "CIS Mining Complex + Large Fuel Depot + flare field on a cut-over peat bog", "It taps the bog gas that feeds the Cauldron; taking it starves the refinery"),
        "D6": ("The Old Listening Post", "library cluster", "CIS Communications FOB + Giant Radar Dish on the south-west rise", "A Republic listening post lost at the war's start; its dish now spies on the fleet. Retaking it gives the Republic eyes over the south"),
    },
    ops=[
        dict(op=1, week=1, name="Over the Wire", start=(8000, 800), prereq=[], fob="Wirefield Redoubt",
             rows="""Wirefield Redoubt|F|p|8.2|3.6|MT|li|Trench fortress in the middle of the south front; taking it gives the first FOB
Pillbox Knoll|M|t|6.6|2.9|BUN|d|Concrete knoll that sees both wings of the wire
Rail Halt|M|p|5.6|2.7|LOG|v|Railhead on the embankment; taking it lets Republic armour use the rail line
Crater Gun Pits|M|t|9.8|3.0|ART|ap|Guns dug into old craters; populated from the start for pilots
Dugout Command Post|M|t|8.9|4.4|TUN|tun|Roofed dugout (library tunnel 1 of 3); its maps show the salients behind
Wire Mill Ruin|S|s|7.0|2.0|OP||Ruin with cover in no man's land
Field Hospital Ruin|S|t|10.6|2.2|DEP|li|Captured clones held here; rescue them
Moraine Foot Checkpoint|S|s|8.4|1.8|CK|v|Road gate off the Republic moraine
Droid Gun Line|S|t|8.6|5.4|ART||Guns behind the redoubt; targets only (Zeus fires)
AA Pit|S|t|7.2|4.6|AA||Grounds LAATs over the south front
Crater Snipers|S|s|10.6|4.0|ZO||Snipers in the crater field
Sap Bunkers|S|s|6.2|3.9|WB||Forward bunkers on the west wing
Plank Road Gate|S|s|7.9|5.2|CK|v|Gate on the plank road north
Bog Gas Dump|S|t|9.6|4.8|FD|d|Fuel for the gun line; burns when hit
Observation Blimp|S|s|11.2|5.4|SR|ao|Spots for the guns; air only
Mortar Crater|S|s|6.0|4.6|TRN2||Mortars on the redoubt's flank (targets, Zeus fires)
Signal Mast|S|s|5.0|3.8|RAD||Relays the south front's traffic"""),
        dict(op=2, week=1, name="The Old Listening Post", start=(4400, 900), prereq=[[1]], fob="Old Listening Post",
             rows="""Old Listening Post|F|p|2.6|3.2|CSFOB|D6 li|The lost Republic post; retaking it gives eyes over the south
West Esker South Fort|M|p|4.0|5.2|FOR||Fort at the south end of the west esker
Kettle Pumphouse|M|t|2.8|6.0|PWR|d|Powers the post's dish; blowing it blinds the dish
Dish Field|M|t|1.4|3.0|RDR|d|The big dish that spies on the fleet
South Moraine West Battery|M|t|1.6|1.4|ART|ap|Guns on the moraine; populated from the start for pilots
Gravel Pit Bunkers|S|s|3.4|4.2|BUN||Pits as cover on the esker foot
Stake Hamlet|S|t|1.3|4.8|TOWN|li|Pile-house hamlet; droid billets
West AA|S|t|0.8|6.4|AAC||Covers the west sky
Esker Watchtower|S|s|4.6|4.0|GT||Sees the rail line and the post
Rail Embankment Gun|S|s|3.4|1.6|TT||Gun on the rail embankment
Moraine Spring Post|S|s|0.8|2.0|ZO||Holds the spring on the moraine
Comms Relay|S|s|2.0|5.4|COM||Relays the dish to the citadel
Fuel Bladders|S|s|3.0|2.2|FD|d|Fuel for the post; burns
Vehicle Park|S|t|4.4|2.6|VD||Walkers parked for counterattacks
Kettle Shore Trench|S|s|3.4|6.6|TR||Trench on the kettle lake shore
Kettle Sensor|S|s|1.0|7.6|SR|ao|Air only; cues the AA
Peat Road Checkpoint|S|s|4.8|6.2|CK|v|Road north to the peat village"""),
        dict(op=3, week=2, name="The Peat-Gas Fields", start=(8200, 3600), prereq=[[1]], fob="Peat-Gas Works",
             rows="""Peat-Gas Works|F|p|13.2|2.6|MIN|D5 d|Taps the bog gas that feeds the Cauldron
Kettle East Fort|M|p|13.6|5.4|FF||Fort on the east kettle; covers the gas field
Pipeline Pumping Station|M|t|11.6|3.4|LPWR|d|Pumps the gas north to the Cauldron
East Crater Battery|M|t|14.6|6.6|ART|ap|Guns over the east bog; for pilots
Gasworks Spur|M|t|11.2|1.6|LOG|v|Road and rail spur into the works
Flare Stack Field|S|s|14.4|1.6|FD|d|Flare stacks; burn when hit
Compressor Sheds|S|t|12.4|2.0|DEP|li|Compressors for the pipeline
South-east AA|S|t|15.2|3.0|AA||Covers the south-east sky
Bog Pool Pillboxes|S|s|12.6|4.4|WB||Pillboxes between the gas pools
Pipeline Checkpoint|S|s|10.4|2.4|CK|v|Road gate on the pipeline road
Gas Holders|S|s|15.0|4.6|FD|d|Big burn
Crater Snipers East|S|s|12.2|6.0|ZO||Snipers over the east bog
Workers' Barracks|S|t|13.6|0.8|LOG||Barracks on the moraine
Radar Rise|S|s|15.4|7.8|RDR||Watches the east
East Trench Line|S|t|14.0|7.6|TR||Trench at the north edge of the field
Gas Plume Sensor|S|s|15.6|0.6|SR|ao|Air only; watches the south-east
Spur Bridge Gate|S|s|11.0|4.6|CK|v|Gate on the spur road"""),
        dict(op=4, week=2, name="The Drain", start=(8200, 3600), prereq=[[2, 3]], fob="Peat Cutters' Village",
             rows="""Drain Locks|F|p|10.4|7.2|DAM|D4 d|The lock dam: the only heavy crossing of the Drain
Peat Cutters' Village|M|p|5.2|7.8|TOWN|li|Village on piles; the next FOB
Drain Rail Bridge|M|t|8.2|7.1|DCK|v|Rail bridge over the Drain; AI crossing
Central Salient|M|p|9.2|8.6|MT||Trench salient north of the Drain
Barge Quay|M|t|12.4|7.0|LND||CIS barges land supplies here
Signal Tower|S|s|8.0|6.0|RAD||Intel on the salients
Sap-head Bunkers|S|s|6.6|8.4|BUN||Forward bunkers west of the salient
Duckboard Maze|S|t|11.2|8.2|TR||Covered trench maze north of the locks
Fuel Point|S|s|9.6|6.0|FD|d|Fuel for the halftracks
Pump House|S|t|10.8|6.4|PWR|d|Keeps the trenches drained
Plank Road Bridge|S|s|7.6|7.6|CK|v|Plank road crossing; AI crossing
Drain AA|S|t|6.0|6.4|AAC||Covers the Drain
Esker Battery|S|t|6.2|9.0|ART|ap|Guns on the centre esker; for pilots
Kettle Lake Outpost|S|s|4.4|9.6|ZO||Watches the kettle lake
Halftrack Park|S|t|12.6|8.2|VD||Mobile reserve
Wire Belt Pillboxes|S|s|8.8|8.0|WB||Pillboxes in the wire
Drain Sensor Mast|S|s|13.6|7.0|SR|ao|Air only; watches the Drain"""),
        dict(op=5, week=3, name="Esker Road", start=(5200, 7800), prereq=[[2, 4]], fob="Esker Redoubt",
             rows="""Esker Redoubt|F|p|3.0|11.0|FOR|D3|Gravel fort on the only high ground in the west
Esker Road Gate|M|t|3.4|9.4|CK|v|The road onto the esker
Esker Dugouts|M|t|3.4|12.6|TUN|tun|Dugouts in the esker side (library tunnel 2 of 3)
North-west Battery|M|t|1.8|13.4|ART|ap|Guns over the west bog; for pilots
Moss Abbey Ruin|M|p|5.8|10.2|OP|li|Ruined abbey held by a platoon
Gravel Pit Bunkers II|S|s|2.0|10.0|BUN||Pits on the esker foot
West Esker AA|S|t|1.4|12.0|AA||Covers the west sky
Bog Pool Pillboxes|S|s|6.6|11.4|WB||Between the pools
Walker Park|S|t|5.0|12.4|VD||Walkers for counterattacks
Kettle North Trench|S|s|5.4|9.4|TR||Trench on the kettle's north shore
NW Comms|S|s|0.8|14.6|COM||Links the west to the citadel
Esker North Watch|S|s|2.6|14.8|GT||Sees the moraine
Stake Causeway Checkpoint|S|s|4.2|13.6|CK|v|Plank causeway north
West Fuel Dump|S|s|2.4|8.4|FD|d|Burns
Peat Bog Snipers|S|s|6.8|12.8|ZO||Snipers in the bog
Moraine West Post|S|t|4.6|15.0|OP||Post on the moraine's west end
Esker Beacon|S|s|0.6|11.0|SR|ao|Air only"""),
        dict(op=6, week=3, name="The Cauldron", start=(10400, 7200), prereq=[[3, 4]], fob="Cauldron rim",
             rows="""Cauldron Refinery|F|p|11.0|11.0|NEW1|D1 new w d|The gas refinery on stilts in the flooded crater
Rim Bunker Ring|M|p|10.4|10.4|MT||Bunkers round the crater rim
Terrace Batteries|M|t|11.6|11.6|ART|ap|Guns on the inner terraces; for pilots
Tank Laager|M|t|12.8|10.0|VD|v|CIS tanks on the crater apron
Cauldron Apron Town|M|p|13.6|11.2|TOWN|li|Workers' town on the crater apron
Rim Spoil Galleries|S|t|11.6|10.4|TUN|tun|Roofed cuts in the spoil (library tunnel 3 of 3)
Spoil Heap Snipers|S|s|12.4|11.8|ZO||High spoil heaps
Pipeline Pump|S|s|9.6|12.0|PWR|d|Pumps fuel north
Gas Holder|S|s|8.8|10.6|FD|ao d|Air only; big burn
Cauldron AA|S|t|10.2|11.8|AA||Covers the crater
NE Esker Fort|S|t|13.6|12.4|FOR||Fort on the north-east esker
Esker Watch NE|S|s|14.6|13.4|GT||Watches the north-east bog
Supply Depot NE|S|t|13.4|14.4|DEP|li|Stores for the citadel's east wing
Refinery Shield Pylon|S|s|11.0|12.4|SHD|d|Shields the refinery until blown
Crater Lip Pillboxes|S|s|14.4|9.0|WB||Cover the east approach
Comms Relay East|S|s|15.2|11.6|COM||Links the refinery to the citadel
Flare Stack Field|S|s|11.6|9.6|FD|d|Burns"""),
        dict(op=7, week=4, name="Moraine Foot", start=(10400, 10400), prereq=[[5, 6]], fob="Kesh Junction",
             rows="""Kesh Junction|F|p|10.6|13.2|TOWN|li|Rail junction town at the moraine foot; the next FOB
Command Dugout Salient|M|p|7.6|13.0|MT||Trench salient guarding the citadel's south
Rail Junction Yard|M|t|11.4|13.8|LOG|v|Rail yard; armour's way to the moraine
Moraine Outwork Battery|M|t|6.4|14.2|ART|ap|Guns on the outwork; for pilots
Moraine Road Gate|M|t|12.2|14.6|DCK|v|Road gate up the moraine
Mud Fort|S|s|8.4|12.2|BUN||Earth fort
Wrecked Walker Strongpoint|S|s|10.0|12.0|WB||Dead walker as a bunker
North AA|S|t|9.0|14.4|HAD||Covers the moraine
Prisoner Pens|S|t|11.0|14.9|DEP|li|Rescue clones
Reserve Camp|S|t|12.8|13.2|LOG||Reserve for counterattacks
Kettle North Pillboxes|S|s|6.0|12.4|WB||Cover the north kettle
Fuel Siding|S|s|10.8|12.4|FD|d|Burns
Moraine Spring Post|S|s|5.6|13.6|ZO||Water for the citadel
Water Tower Snipers|S|s|8.8|13.2|GT||Overwatch on the junction
Comms Mast|S|s|12.0|12.2|COM||Intel on the citadel
Junction Sensor|S|s|13.8|15.4|SR|ao|Air only
Junction Field Hospital|S|t|9.4|12.4|DEP|li|Captured medics held here; rescue them"""),
        dict(op=8, week=4, name="The Moraine Citadel", start=(10600, 13200), prereq=[[7]], fob="end of run",
             rows="""Moraine Citadel|F|p|8.4|15.2|NEW2|D2 new cap|CIS front headquarters; the capstone interior is inside
Citadel Gate|M|t|8.0|14.6|DCK|v|Gate into the citadel (starts closed)
Hangar Bunkers|M|p|10.4|15.3|ELP|li|Gunship bunkers
Moraine Battery|M|t|6.4|15.4|ART|ap|Guns on the moraine; for pilots
Citadel Power Plant|M|t|9.6|15.7|LPWR|d|Powers the citadel's shields
West Gate Bunkers|S|s|5.6|15.0|BUN||Second way in
Supply Railhead|S|t|12.0|15.4|LOG|v|Rail end
Comms Mast North|S|s|7.2|15.7|COM||Calls the fleet
Fuel Tanks|S|s|13.0|15.0|FD|d|Burns
Water Tower Overwatch|S|s|5.0|14.4|GT||Overwatch on the west gate
East Moraine AA|S|t|11.6|15.7|AA||Covers the citadel
Moraine Trench West|S|s|4.2|15.2|TR||West flank
Moraine Trench East|S|s|14.0|14.4|TR||East flank
Shield Pylons|S|t|9.0|14.8|SHD|d|Shield the citadel until blown
Orbital Uplink Dish|S|s|14.8|15.6|RDR|ao d|Air only
Citadel Barracks|S|t|7.4|14.6|LOG||Reserve garrison
Escape Pad|S|s|10.0|14.4|ELP||Stops officers escaping"""),
    ],
)

# ============================================================== B
B = dict(
    key="B", title="The Glow", setting="Felucia (canon Clone Wars battle world)",
    draws={
        "D1": ("The Felled Titan", "NEW 1", "A fallen giant stalk baked into the heightmap as a 2.8 km land berm across the main slough (terrain, dressed with simple rock and bark objects, no roof); the new build is a Droid-Factory-class bio-lab at its west root plate (about 300 x 250 m)", "The CIS harvest the Titan's spores here; the berm is the only dry crossing of the main slough"),
        "D2": ("The Spore Citadel", "NEW 2 + capstone", "A Droid-Factory-class lab citadel on the north rise; the planet's ONE capstone interior is inside", "Where the spore weapon is cultured; the end of the run"),
        "D3": ("The Canal Lock", "library cluster", "CIS Fortress Dam as the canal lock + levee bunkers + pump house", "The lock carries the only paved road north on the east side"),
        "D4": ("The Spore Ridge Grove", "library cluster", "CIS Small Citadel + Large Power Facility among giant-flora dressing on the limestone ridge", "The ridge forest's spore labs and the west's only high ground"),
        "D5": ("The Lake Hover Base", "library cluster", "CIS Elevated Landing Pads + Vehicle Depot + Covered AA on the south lake shore", "The droid hover fleet's base; it holds the lake, the Republic's way in"),
        "D6": ("The Cenote Caves", "library cluster", "PLAD Cave Base + Royal Tunnel Holdout in a ring of sinkholes", "Spore stores hidden in the sinkhole caves; the map's tunnel site"),
    },
    ops=[
        dict(op=1, week=1, name="Edge of the Grass", start=(8000, 600), prereq=[], fob="Lake Hover Base",
             rows="""Lake Hover Base|F|p|6.2|2.2|ELP|D5|The hover fleet's base on the lake shore; the first FOB
Heron Hammock Fort|M|p|7.6|3.4|FOR||Fort on the biggest south hammock
Lakeshore AA|M|t|8.8|2.4|AAC||Covers the lake; LAATs land once it falls
Gladeside Village|M|p|4.6|3.2|TOWN|li|Felucian-style stilt village; droid billets
Hover Depot|M|t|5.4|1.4|VD|ap|Hover tanks parked on the shore; for pilots
Sawgrass Pillboxes|S|s|9.4|3.4|WB||Pillboxes in open grass
Spore Sampler Station|S|s|10.6|3.0|COM||Intel: what the labs make
Hammock Gun Nest|S|t|11.8|4.2|ART||Guns over the grass (targets only)
Cenote Rim Post|S|s|5.8|4.2|ZO||Post on a sinkhole rim
Boardwalk Gate|S|s|6.8|3.0|CK||Gate on the village boardwalk
Fuel Silos South|S|s|9.6|1.4|FD|d|Burns
Lake Shore Trench|S|s|4.2|1.6|TR||Covers the west shore
South Slough Bunkers|S|t|8.2|4.6|BUN||Cover the main slough's mouth
Village Comms|S|s|3.6|4.4|RAD||Relays to the ridge
Grass Watchtower|S|s|10.2|4.8|GT||Sees the whole south grass
Spore Balloon Tether|S|s|8.6|5.6|SR|ao|Air only; spreads spores
Spore Press Shed|S|t|5.0|2.4|DEP||Presses spores for the labs; intel on the cargo"""),
        dict(op=2, week=1, name="Canal Road", start=(12800, 1200), prereq=[[1]], fob="Canal Lock",
             rows="""Canal Lock|F|p|13.8|6.4|DAM|D3 d|The lock carries the only paved road north
Ranger Station|M|p|12.2|7.2|OP|li|Old Republic post to retake
Levee Battery|M|t|13.4|8.6|ART|ap|Guns on the levee; for pilots
Pumping Station|M|t|14.4|7.6|LPWR|d|Powers the east shields
South Canal Checkpoint|M|t|13.8|3.6|DCK|v|Gate on the canal road
Canal Barge Yard|S|s|14.2|5.2|LND||Barges and boats (shore pads)
Levee Bunker Line|S|t|13.9|9.8|BUN||Bunkers on the levee
Fungus Farm Hammock|S|s|11.2|6.0|OP||Food and spores
Fuel Silos East|S|s|14.6|10.4|FD|d|Burns
Canal Bridge|S|s|13.6|11.2|CK|v|AI crossing of the canal
Levee AA|S|t|12.8|10.6|AA||Covers the canal
South-east Grass Post|S|s|15.2|2.0|ZO||Watches the south-east
Lake East Bunkers|S|s|11.6|1.4|WB||Cover the lake's east shore
Canal Depot|S|t|14.8|4.4|DEP||Stores for the lock
East Hammock Snipers|S|s|11.8|9.0|ZO||Snipers on a hammock
Canal Sensor|S|s|15.6|8.4|SR|ao|Air only
Lock Keeper's Post|S|s|12.6|5.4|GT||Watches the lock's south approach"""),
        dict(op=3, week=2, name="Spore Ridge", start=(4600, 3200), prereq=[[1]], fob="Spore Ridge Grove",
             rows="""Spore Ridge Grove|F|p|3.2|9.0|CIT|D4 li|Spore labs in the ridge forest
Ridge Road Fort|M|p|3.0|6.4|FOR|v|Fort on the ridge road
Ridge Power Station|M|t|3.6|10.6|LPWR|d|Powers the grove's labs
Ridge Gun Battery|M|t|3.6|5.0|ART|ap|Guns over the main slough; for pilots
Fungal Hamlet|M|t|1.6|5.6|TOWN|li|Hamlet among the giant caps
Giant Cap Snipers|S|s|2.4|7.8|ZO||Snipers under the caps
Ridge AA South|S|t|2.2|3.2|AA||Covers the south ridge
Cenote Pump House|S|s|4.6|7.2|PWR|d|Water for the labs
Glade Comms|S|s|5.0|9.8|COM||Intel on the Titan
Ridge South Gate|S|s|2.8|2.2|CK|v|Gate on the ridge road
West Grass Trench|S|s|1.0|8.6|TR||West flank
Spore Silos|S|t|2.6|11.6|FD|d|Burns
Ridge Watchtower|S|s|4.2|8.4|GT||Sees the slough
Ridge Depot|S|t|1.4|10.2|DEP||Stores
Root Bunkers|S|s|4.0|12.2|BUN||North end of the grove
Spore Venting Tower|S|s|1.2|12.6|SR|ao|Air only
Ridge Fuel Point|S|s|3.8|3.6|FD|d|Fuel for the ridge walkers; burns"""),
        dict(op=4, week=2, name="The Felled Titan", start=(4600, 3200), prereq=[[1, 3]], fob="Titan root plate",
             rows="""Titan Root Lab|F|p|6.4|8.4|NEW1|D1 new d|Spore harvest lab at the Titan's root plate
Titan Crown Fort|M|p|9.6|8.9|FOR||Fort in the fallen crown, east end of the berm
Mid-Titan Bunkers|M|t|8.0|8.7|BUN||Bunkers on the berm crest; the dry crossing
Slough Hover Pens|M|t|8.2|7.2|VD|ap|Hovers in the slough (shore pads); for pilots
Tree Island Battery|M|t|10.2|10.0|ART||Guns cover the berm
Channel Pillboxes|S|s|7.4|9.6|WB||On a hammock by the boat channel
Hammock Hamlet North|S|t|6.8|10.8|TOWN|li|Hamlet
Fungus Light Tower|S|s|9.0|7.6|COM||Comms
Spore Pond Pumps|S|s|10.8|7.8|PWR|d|Feed the lab
Mid-slough AA|S|t|7.0|7.4|AA||Covers the slough
Root Plate Trench|S|s|5.6|8.0|TR||West of the lab
Berm East Checkpoint|S|s|9.2|8.6|CK|v|Gate on the berm road
Bark Quarry|S|t|5.4|9.4|DEP||Cut bark for the lab
Crown Snipers|S|s|10.0|9.4|ZO||Snipers in the crown
Slough Fuel Point|S|s|7.0|6.4|FD|d|Burns
Titan Spore Sensor|S|s|8.6|10.2|SR|ao|Air only
Berm West Gate|S|s|6.0|9.0|CK|v|Gate where the berm road leaves the root plate"""),
        dict(op=5, week=3, name="East Hammocks", start=(12200, 7200), prereq=[[2, 4]], fob="Grass Sea Fort",
             rows="""Grass Sea Fort|F|p|12.4|10.4|FF||Fort on the biggest east hammock
Big Hammock Barracks|M|p|11.2|11.6|LOG||Barracks for the east
East Branch Bunkers|M|t|10.6|9.6|BUN||Cover the east branch slough
Hammock Battery|M|t|13.2|12.0|ART|ap|Guns reach the north rise; for pilots
Stilt Supply Depot|M|t|12.6|12.8|DEP||Supplies for the citadel (on a hammock)
Grass Sea Pillboxes|S|s|11.6|10.6|WB||In the grass
East Comms|S|s|14.2|11.6|COM||Intel
Hammock AA|S|t|12.0|9.0|AA||Covers the east grass
Fuel Barrels|S|s|13.8|10.2|FD|d|Burns
East Watchtower|S|s|15.0|12.2|GT||Sees the canal
Grass Trench|S|s|11.0|8.6|TR||South edge
Hover Park East|S|t|14.4|9.0|VD||Mobile reserve
Hammock Snipers|S|s|10.4|11.0|ZO||Snipers
Spore Drying Racks|S|s|13.0|11.0|OP||Spore drying
Grass Sensor|S|s|15.6|11.0|SR|ao|Air only
East Hammock Depot|S|t|13.6|9.4|DEP||Stores for the east
Branch Slough Trench|S|s|10.8|10.2|TR||Covers the east branch crossing"""),
        dict(op=6, week=3, name="The Cenote Caves", start=(12400, 10400), prereq=[[4, 5]], fob="Cenote Caves",
             rows="""Cenote Caves|F|p|11.4|12.8|CAVE|D6 tun|Spore stores in the sinkhole caves (library tunnel 1 of 2)
Cenote Ring Fort|M|p|10.4|13.6|FOR||Fort on the cenote rim
North Branch Bunkers|M|t|12.4|14.4|BUN||Cover the north branch slough
Cave Pump House|M|t|12.0|13.2|PWR|d|Keeps the caves dry
North-east AA|M|t|14.0|14.6|HAD|ap|Covers the north-east; for pilots
Cenote Hamlet|S|t|13.2|13.6|TOWN|li|Hamlet
Cave Depot|S|t|10.8|14.4|DEP||Stores
Rim Snipers|S|s|11.0|12.0|ZO||Snipers
Fuel Cache|S|s|13.6|15.2|FD|d|Burns
North-east Watch|S|s|15.2|14.0|GT||Watches the canal head
Cenote Trench|S|s|9.8|12.6|TR||West edge
Spore Kiln|S|t|14.8|13.0|OP||Kiln
Canal Head Gate|S|s|14.6|15.6|CK|v|Road gate
Drone Hive Tower|S|s|15.6|15.2|SR|ao|Air only
Cave Mouth Bunkers|S|s|11.8|12.2|BUN||Guard the main cave mouth
Cenote Comms|S|s|10.2|14.8|COM||Intel on the citadel
North Slough Pillboxes|S|s|12.8|15.4|WB||North branch crossing"""),
        dict(op=7, week=4, name="North-west Groves", start=(3200, 9000), prereq=[[3, 4]], fob="Spore Works North",
             rows="""Spore Works North|F|p|4.2|13.0|LPWR|li|Second spore lab on the ridge's north end
Root Cellar Maze|M|t|3.0|13.8|TUN|tun|Roofed cuts in the root mass (library tunnel 2 of 2)
North Ridge Fort|M|p|3.6|14.8|FOR||Fort on the ridge's north tip
Grove Battery|M|t|5.6|13.4|ART|ap|Guns over the north grass; for pilots
North-west AA|M|t|1.4|14.2|AA||Covers the north-west
Grove Hamlet|S|t|2.0|12.6|TOWN|li|Hamlet among the caps
North Branch Pillboxes|S|s|5.2|12.0|WB||By the north-west branch slough
Grove Comms|S|s|1.0|15.4|COM||Intel
Spore Tanks|S|s|4.8|14.6|FD|d|Burns
Grove Watchtower|S|s|6.2|14.8|GT||Sees the rise
Cap Snipers|S|s|2.4|15.4|ZO||Snipers
North Ridge Gate|S|s|3.8|11.8|CK|v|Ridge road gate
Grove Depot|S|t|6.4|12.2|DEP||Stores
North-west Sensor|S|s|0.6|13.0|SR|ao|Air only
Grove AA South|S|t|4.6|11.0|AAC||Covers the north grove
Spore Kiln West|S|s|1.6|11.2|OP||Kiln in the caps
Ridge North Trench|S|s|2.8|12.0|TR||Trench below the north fort"""),
        dict(op=8, week=4, name="The Spore Citadel", start=(9600, 12400), prereq=[[6, 7]], fob="end of run",
             rows="""Spore Citadel|F|p|8.2|15.0|NEW2|D2 new cap|The lab citadel; the capstone interior is inside
Culture Vat Halls|M|p|9.4|15.2|LOG|li|Vat halls beside the citadel
Citadel Gate Wall|M|t|8.6|14.4|DCK|v|Gate (starts closed)
Citadel Battery|M|t|10.6|14.8|ART|ap|Guns on the rise; for pilots
Generator Cap|M|t|7.0|15.4|LPWR|d|Power for the shield
Prisoner Pods|S|t|9.8|14.2|DEP|li|Rescue clones
West Gate Bunkers|S|s|6.2|14.4|BUN||Second way in
Landing Pad Ring|S|s|7.4|15.8|ELP||Escape pads
Citadel AA|S|t|10.2|15.8|AA||Covers the rise
Shield Pylons|S|s|8.0|14.0|SHD|d|Shield the citadel
Citadel Comms|S|s|9.2|15.8|COM||Calls the fleet
Rise Trench East|S|s|11.0|14.0|TR||East flank
Spore Silos North|S|s|7.0|14.0|FD|d|Burns
Rise Snipers|S|s|11.6|15.4|ZO||Overwatch
Uplink Dish|S|s|12.4|15.8|RDR|ao d|Air only
Rise Depot West|S|t|6.4|15.4|DEP||Stores for the citadel
Vat Coolant Pumps|S|s|10.8|15.4|PWR|d|Cool the vats; blowing them spoils a batch"""),
    ],
)

# ============================================================== C
C = dict(
    key="C", title="River Country", setting="Rodia (canon Clone Wars swamp world)",
    draws={
        "D1": ("The Stilt Refinery", "NEW 1", "A Droid-Factory-class fuel refinery on stilts in the west oxbow lake (about 350 x 250 m), with pier causeways", "Fuel for the whole CIS river fleet; its flares are seen from the river mouth"),
        "D2": ("The Headwater Foundry", "NEW 2 + capstone", "A Droid-Factory-class foundry on the east terrace; the planet's ONE capstone interior is inside", "Builds the droids that hold the river; the end of the run"),
        "D3": ("Rodian River City", "town work + library cluster", "A hand-made tiered Rodian town on the levee bend (town work, not a comp) + library checkpoints and AA", "The river's capital, with the main vehicle bridge"),
        "D4": ("The River Weir", "library cluster", "CIS Fortress Dam as a weir across the river + lock house + bunkers", "Holds the upper river's level; its crest road is an AI crossing"),
        "D5": ("The North Bluff Fort", "library cluster", "CIS Small Citadel + artillery + AA on the north bluff edge", "Its guns see the whole floodplain"),
        "D6": ("The South Bluff Quarry", "library cluster", "CIS Mining Complex + artillery on the south bluff", "Cuts the stone for the foundry; fills the south-east of the map"),
    },
    ops=[
        dict(op=1, week=1, name="River Mouth", start=(500, 5500), prereq=[], fob="Levee Fort West",
             rows="""Levee Fort West|F|p|1.6|5.0|FOR|v|Fort on the north levee road; the first FOB
Mouth Bridge|M|t|2.2|4.2|DCK|v|Road bridge at the mouth; AI crossing 1 of 4
Fishing Stilt Village|M|p|1.2|2.6|TOWN|li w|Rodian stilt village on the south bank
Levee Battery|M|t|4.2|4.0|ART|ap|Guns cover the river; for pilots
South Bluff AA|M|t|3.0|1.4|AA||Covers the river mouth
Ferry Landing|S|s|2.8|4.6|LND||Shore landing pads
Backswamp Pillboxes|S|s|3.4|6.0|WB||North backswamp
Levee Bunkers|S|t|4.4|5.2|BUN||Bunkers in the levee
Pump Tower|S|s|0.8|4.0|PWR|d|Water and power
Cypress Snipers|S|s|2.0|7.0|ZO||Snipers in the trees
Bayou Boat Shed|S|t|2.2|3.2|DEP||Boat shed on the shore
South Bluff Post|S|s|1.0|1.0|OP||South-west corner post
Mouth Fuel Depot|S|s|0.6|6.6|FD|d|Burns
Levee Watch|S|s|3.0|7.8|GT||North-west backswamp
West Lake Trench|S|s|1.4|8.8|TR||By the west lake
Channel Sensor|S|s|3.8|3.0|SR|ao|Air only
Mouth Snipers|S|s|1.8|3.0|ZO||Overwatch on the bridge"""),
        dict(op=2, week=1, name="The Oxbow", start=(1600, 5000), prereq=[[1]], fob="Neck Village",
             rows="""Stilt Refinery|F|p|6.4|8.7|NEW1|D1 new w d|Fuel refinery rising out of the oxbow lake
Neck Village|M|p|6.6|7.4|TOWN|li|Village on the oxbow neck; the next FOB
Oxbow Tank Farm|M|t|7.4|8.9|LFD|d|Fuel tanks; big burn
Pipeline Gun Nests|M|t|5.2|9.2|ART|ap|Guns on the pipeline berm; for pilots
Levee Road Checkpoint|M|t|5.4|6.4|DCK|v|Gate on the levee road
Refinery Pier Gate|S|s|6.0|8.0|CK|w|Pier causeway gate: the foot way in
Oxbow AA|S|t|5.8|9.8|AAC||Covers the lake
Pumphouse|S|s|7.6|9.8|PWR|d|Pumps for the refinery
Bayou Bridge South|S|s|4.8|7.6|CK|v|Bridge over the bayou mouth
South Bank Bunkers|S|s|6.2|5.4|BUN||South bank of the river
Lake Shore Trench|S|s|7.0|3.6|TR||By the south lake
South Lake Outpost|S|t|5.6|2.6|OP||Fills the south-centre
Refinery Comms|S|s|8.0|7.8|COM||Intel
Refinery Fuel Barge Pad|S|s|6.8|10.0|FD|d|Burns
Gas Flare Tower|S|s|7.8|10.4|SR|ao|Air only
Oxbow Watch|S|s|5.0|10.2|GT||Sees the refinery's west side
South Bank Depot|S|t|7.2|5.0|DEP||Stores on the south bank"""),
        dict(op=3, week=2, name="Rodian River City", start=(6600, 7400), prereq=[[2]], fob="River City",
             rows="""River City Market Tiers|F|p|9.0|7.6|TOWN|D3 li|The tiered city on the levee bend
City Levee Gate|M|p|8.4|7.2|DCK|v|Walled levee gate (starts closed)
City Bridge|M|t|8.6|8.2|DCK|v|Main vehicle bridge; AI crossing 2 of 4
Council Hall|M|t|9.5|7.4|OP|li|Rescue the Rodian council
South Bank Battery|M|t|7.6|5.6|ART|ap|Guns cover the bridge; for pilots
Rooftop AA|S|t|9.3|7.0|AA||Covers the city
Harbour Quay|S|s|9.4|6.6|LND||River harbour pads
Water Temple Tower|S|s|9.8|8.0|RAD||Tall landmark; intel
Undercity Canal Bunkers|S|s|8.8|7.0|BUN||Canal-side bunkers
South Levee Pillboxes|S|s|8.8|5.8|WB||Flank cover
City Fuel Depot|S|s|10.2|7.2|FD|d|Burns
North Bank Outpost|S|t|9.4|9.2|OP||North bank of the bend
Backswamp Snipers|S|s|10.4|9.6|ZO||Snipers
City Depot|S|t|8.2|6.2|DEP||Stores
City Spire Relay|S|s|10.6|8.0|SR|ao|Air only
City Snipers|S|s|10.0|6.2|ZO||Overwatch on the harbour
North Bank Trench|S|s|8.6|9.6|TR||Covers the bridge's north end"""),
        dict(op=4, week=2, name="South Bluff Quarry", start=(9000, 6200), prereq=[[2, 3]], fob="South Bluff Quarry",
             rows="""South Bluff Quarry|F|p|13.0|1.6|MIN|D6|Stone for the foundry; the south-east's draw
Backswamp Lake Fort|M|p|10.8|3.0|FOR||Fort on the lake's south shore
Bluff Battery|M|t|14.6|2.4|ART|ap|Guns on the bluff edge; for pilots
Quarry Rail Head|M|t|11.6|1.2|LOG|v|Stone loading
Bluff Road Checkpoint|M|t|12.0|4.6|DCK|v|South bluff road
Quarry Barracks|S|t|13.8|0.8|LOG||Quarry crews
Splay Pillboxes|S|s|13.4|5.6|WB||On the crevasse splay
Bluff AA|S|t|15.4|1.2|AA||Covers the south-east
Lake East Bunkers|S|s|11.6|4.2|BUN||East lake shore
Quarry Fuel|S|s|12.4|2.6|FD|d|Burns
Powder Store|S|s|14.2|3.6|DEP|d|Blasting charges; big burn
South-east Watch|S|s|15.4|4.8|GT||Watches the east
Bluff Comms|S|s|10.2|1.2|COM||Intel
Quarry Snipers|S|s|14.0|1.8|ZO||Overwatch
Bluff Sensor|S|s|15.6|0.4|SR|ao|Air only
Quarry Depot|S|t|11.0|2.4|DEP||Stores
Bluff Edge Trench|S|s|9.6|2.2|TR||Fills the south-centre bluff"""),
        dict(op=5, week=3, name="The Weir", start=(10200, 7600), prereq=[[3, 4]], fob="River Weir",
             rows="""River Weir|F|p|12.6|9.8|DAM|D4 d|Weir across the river; AI crossing 3 of 4
Second Oxbow Fort|M|p|10.6|6.5|FOR||Fort inside the second oxbow
Levee Battery East|M|t|11.8|8.6|ART|ap|Guns cover the bends; for pilots
Splay Town|M|t|13.6|8.0|TOWN|li|Small town on the splay
Weir Lock House|M|t|12.2|10.2|PWR|d|Lock machinery
Levee Tunnels East|S|t|12.2|9.0|TUN|tun|Roofed cuts in the levee (library tunnel 1 of 2)
Weir AA|S|t|11.2|7.6|AA||Covers the bends
Weir Fuel|S|s|13.4|9.4|FD|d|Burns
East Levee Bunkers|S|s|14.2|10.2|BUN||East levee
Oxbow Neck Post|S|s|10.0|5.6|OP||South of the oxbow
Lake Pillboxes|S|s|12.6|6.8|WB||By the splay
East Watch|S|s|15.2|9.0|GT||Watches the upper river
Weir Comms|S|s|11.4|10.4|COM||Intel
Weir Sensor|S|s|14.0|7.0|SR|ao|Air only
Weir Depot|S|t|13.6|10.6|DEP||Stores
Splay Snipers|S|s|14.4|8.0|ZO||Overwatch
Oxbow Bunkers|S|s|11.4|6.0|BUN||Second oxbow's south side"""),
        dict(op=6, week=3, name="North Bluffs", start=(9000, 7800), prereq=[[3]], fob="North Bluff Fort",
             rows="""North Bluff Fort|F|p|8.2|13.4|CIT|D5 li|Bluff fort; its guns see the whole floodplain
Bluff Stair Battery|M|t|9.6|13.4|ART|ap|Guns over the floodplain; for pilots
Bluff Face Galleries|M|t|7.4|13.2|TUN|tun|Roofed cuts in the bluff (library tunnel 2 of 2)
Bayou Head Village|M|p|4.6|13.4|TOWN|li|Village at the bayou head
Bayou Bridge|M|t|5.0|12.2|CK|v|Road over the bayou
Logging Camp|S|t|6.0|11.6|DEP||Timber and boats
Backswamp Outposts|S|s|8.6|10.8|OP||On hammocks
North-west Lake Trench|S|s|2.6|10.0|TR||By the west lake
West Bluff AA|S|t|2.4|13.6|AA||Covers the north-west
Bluff Comms|S|s|9.0|14.4|COM||Intel on the foundry
North-west Corner Post|S|s|0.8|14.6|OP||North-west corner
Bayou Snipers|S|s|3.8|12.4|ZO||Snipers
Bluff Fuel|S|s|6.8|14.4|FD|d|Burns
Bluff Watch|S|s|1.4|12.0|GT||Watches the west
Bluff Sensor Mast|S|s|10.8|14.6|SR|ao|Air only
Bluff Depot|S|t|7.4|14.6|DEP||Stores for the fort
North Lake Pillboxes|S|s|3.4|9.6|WB||By the west lake"""),
        dict(op=7, week=4, name="Upper Bends", start=(12600, 9800), prereq=[[5, 6]], fob="Plantation Stilt Town",
             rows="""Plantation Stilt Town|F|p|13.2|11.0|TOWN|li|Stilt town on the bend; the next FOB
Headwater Bridge|M|t|14.6|11.3|DCK|v|Bridge below the foundry; AI crossing 4 of 4
Upper Levee Fort|M|p|11.8|11.6|FOR||North levee fort
Bend Battery|M|t|13.0|12.4|ART|ap|Guns over the bends; for pilots
North Lake Bunkers|M|t|11.8|12.6|BUN||By the north lake
Fuel Barges Pad|S|s|14.8|10.6|FD|d|Burns
Upper AA|S|t|12.6|10.4|AA||Covers the bends
Plantation Depot|S|t|13.8|11.8|DEP||Stores
Levee Snipers|S|s|10.8|11.0|ZO||Snipers
Upper Comms|S|s|12.2|13.4|COM||Intel
East Bank Trench|S|s|15.4|10.4|TR||East bank
Workers' Stilts|S|t|12.4|12.0|OP|li|Worker housing
Upper Sensor|S|s|10.4|12.8|SR|ao|Air only
Upper Fuel Depot|S|s|11.2|12.0|FD|d|Burns
Bend Watch|S|s|14.2|12.6|GT||Sees the terrace
Upper Trench|S|s|10.2|11.4|TR||West flank
Plantation Pillboxes|S|s|13.8|10.2|WB||Covers the south bank"""),
        dict(op=8, week=4, name="Headwater Works", start=(13200, 11000), prereq=[[7]], fob="end of run",
             rows="""Headwater Foundry|F|p|14.4|13.6|NEW2|D2 new cap|The droid foundry; the capstone interior is inside
Assembly Yard|M|p|15.0|12.8|LOG|li|Assembly halls (library interiors)
Terrace Gate Wall|M|t|13.6|12.8|DCK|v|Gate (starts closed)
Foundry Battery|M|t|12.8|14.2|ART|ap|Guns cover the bends; for pilots
Foundry Power Plant|M|t|15.4|14.4|LPWR|d|Power for the foundry and its shield
River Intake|S|s|15.2|11.6|PWR|d|Cooling water
Shield Pylon|S|s|13.4|13.8|SHD|d|Drops the foundry shield
Terrace AA|S|t|15.4|13.4|AA||Covers the terrace
Landing Pad|S|s|14.8|15.2|ELP||Escape pad
Terrace Trench|S|s|13.0|13.2|TR||West flank
Ore Store|S|t|14.0|15.0|DEP|d|Burns
North-east Corner Post|S|s|15.6|15.6|OP||Corner post
Terrace Snipers|S|s|12.4|15.2|ZO||Overwatch
Foundry Comms|S|s|13.2|15.6|COM||Calls the fleet
Foundry Uplink|S|s|11.6|15.0|RDR|ao d|Air only
Terrace Depot West|S|t|12.4|13.6|DEP||Stores
Terrace Pillboxes|S|s|15.6|12.2|WB||East flank"""),
    ],
)

CONCEPTS = {"A": A, "B": B, "C": C}
