"""Pad half-sizes (hx, hy) in metres per composition.
KNOWN: Kernel's built pad of the same composition (Thirra ops 1-2 pads, 11 Nov C pack). ASSUMED: no built pad; the basis is stated."""
KNOWN = {
 "CIS Basic Trenchline with GPs": (57.0, 30.2), "CIS Comms Array with GPs": (20.1, 46.3), "CIS Depot (Fixed) with GPs (D)": (67.1, 124.1),
 "CIS Double Pcannon Checkpoint with GPs": (35.5, 25.5), "CIS Elevated Landing Pad Construction with GPs": (60.6, 39.5),
 "CIS Fuel Depot with GPs": (43.6, 32.3), "CIS Heavy Gun Position + AA (UD)": (29.9, 40.8), "CIS Landing Position with GPs": (44.5, 67.0),
 "CIS Large Fuel Depot with GPs": (123.8, 130.6), "CIS Medium AA Base with GPs": (98.5, 96.4), "CIS Metal Trench Line with GPs": (21.7, 75.1),
 "CIS Mini Fortress with GPs": (77.1, 72.4), "CIS Mixed AA Platform with GPs": (47.9, 43.6), "CIS Powerbank Facility with GPs": (96.0, 82.9),
 "CIS Small Checkpoint with GPs": (28.4, 34.4), "CIS Small Rectangle FOB with GPs": (45.1, 29.1), "CIS Turbolaser Tower with GPs": (27.5, 30.1),
}
ASSUMED = {
 "CIS Mining Complex with GPs": (80.0, 80.0, "ASSUMED: 160 x 160 m"),
 "flare-stack field": (40.0, 40.0, "ASSUMED: 80 x 80 m of stacks"),
 "CIS Flower Fortress with GPs": (70.0, 70.0, "ASSUMED: larger than the CIS Flower Tower (93 x 88 m built)"),
 "CIS Large Power Facility with GPs": (96.0, 82.9, "ASSUMED: as the CIS Powerbank Facility (built)"),
 "CIS Medium Logistics Base with GPs": (60.0, 50.0, "ASSUMED: 120 x 100 m"),
 "[Burnzy] CIS Arti-base + Flower Tower 2": (70.0, 60.0, "ASSUMED: the Small Artillery Base (128 x 63 m built) beside a Flower Tower 2 (93 x 101 m built), as one 140 x 120 m pad"),
 "Small Wall with Bunker": (20.0, 12.0, "ASSUMED: 40 x 24 m"),
 "Zavala CIS Outpost with GPs": (30.0, 30.0, "ASSUMED: 60 x 60 m"),
 "Giant Radar Dish": (40.0, 40.0, "ASSUMED: 80 x 80 m"),
 "Claus - Small Radar": (15.0, 15.0, "ASSUMED: 30 x 30 m"),
 "TKTA Checkpoint Fixed (Mono)": (30.0, 20.0, "ASSUMED: 60 x 40 m"),
 "CIS Big Radio Tower with GPs": (15.0, 15.0, "ASSUMED: 30 x 30 m"),
 "Tukata Turret Bunker": (15.0, 15.0, "ASSUMED: 30 x 30 m"),
 "Medium Covered AA Base with GPs": (98.5, 96.4, "ASSUMED: as the CIS Medium AA Base (built)"),
 "CIS Vehicle Depot with GPs (D)": (60.0, 60.0, "ASSUMED: 120 x 120 m"),
 "town outline (about 80 buildings)": (125.0, 125.0, "ASSUMED: a 250 x 250 m town outline (Causeway Foot scale)"),
}
def size(comp):
    if comp in KNOWN: return KNOWN[comp][0], KNOWN[comp][1], f"KNOWN (built): your built pad of {comp} on Thirra (11 Nov C pack), {2*KNOWN[comp][0]:.0f} x {2*KNOWN[comp][1]:.0f} m"
    hx, hy, ev = ASSUMED[comp]; return hx, hy, ev

def sites(spec, R):
    """spec: list of (site id, [comps, main first], search radius). Members get ids <site>.2, .3 ... at the main's design point."""
    out = []
    for sid, comps, rad in spec:
        for k, c in enumerate(comps):
            hx, hy, ev = size(c); i = sid if k == 0 else f"{sid}.{k + 1}"
            out.append((i, R[sid]["name"] + ("" if k == 0 else f" (member {k + 1})"), c, hx, hy, ev, None if k == 0 else (R[sid]["x"], R[sid]["y"]), rad, False))
    return out
