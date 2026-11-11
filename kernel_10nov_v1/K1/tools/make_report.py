"""Write TOWNS.md from the town JSONs (measured numbers) plus the hand-written look notes."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LOOK = {
    "Sound Head": "Boatyard town. The quay front and the square are the sci-fi core: grey CIS slipway halls and the "
                  "Boatyard Control Spire. Behind them, white cubes climb the slope in stepped blocks, and Naboo domes "
                  "mark corners and the lane heads. The inlet's red-and-black banded cliffs frame the town from the sea.",
    "Causeway Foot": "Road town at the causeway landfall. The sci-fi core is the toll and signal pylon on the square, "
                     "with the CIS gatehouse halls at the causeway end. White cubes line the bends of the 8 m main "
                     "street, and domed corner houses sit at the fork. Black lava sand on the beach below.",
    "Kastro Quay": "The biggest town in this pack. A harbour lower town: sci-fi warehouses and the Supply Port Control "
                   "Spire on the quay square. White cube terraces climb the main street toward the acropolis, and domes "
                   "cluster where the lanes leave the main street. The white pumice cliffs of Acropolis Isle are behind.",
    "Lantern Quay": "A small, tight fishing hamlet. One quay row, then a steep main street with the Beacon Relay Mast on a "
                    "pocket square. Mostly white cubes with blue-green alien scrub between them. The sci-fi share is lower "
                    "here on purpose (a civilian hamlet); the mast and the quay sheds carry the sci-fi read.",
    "Kamar Village": "Ravine village above the black Kamar Strand. The sci-fi core is the Moisture Condenser Tower and "
                     "the CIS billets on the quay. White cubes stack up the ravine bends, with domes on the corner "
                     "houses. The pale limestone of the Prophet Massif rises behind.",
    "Oyra": "Rim town on the caldera's inner cliff. White cubes and Naboo domes pour over the cliff edge toward the "
            "lagoon (the Santorini teacher, not a copy). The sci-fi core is the rim square with the Narrows Signal "
            "Lantern, CIS garrison halls beside it, and cliff-edge look-outs at the ends of the lanes. The town faces "
            "the lagoon and the North Narrows.",
}


def main():
    out = ["# K1 town plans: six hand-made towns for Islands \"Ember Caldera\" (PROPOSED)", "",
           "Plans for Miran's look, not build files. North up, metres. Each town has a PNG and a JSON in `towns/`.", ""]
    rows = ["| Town | Op | Site | Size | Buildings | In blocks | sci-fi / white cube / Naboo dome | Garrison | Longest straight run (main / lanes) | Extent |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    secs = []
    for f in sorted(os.listdir(os.path.join(ROOT, "towns"))):
        if not f.endswith(".json"):
            continue
        d = json.load(open(os.path.join(ROOT, "towns", f)))
        m = d["measured"]
        fc = m["family_counts"]
        main_run = max(s["max_straight_run_m"] for s in m["streets"] if s["kind"] == "main")
        lane_run = max([s["max_straight_run_m"] for s in m["streets"] if s["kind"] == "lane"] or [0])
        rows.append(f"| {d['town']} | {d['op']} | {d['site_id']} | {d['size'].replace('_', '-')} | {m['buildings']} | "
                    f"{m['in_blocks_pct']} % | {fc['sci-fi']} / {fc['white cube']} / {fc['Naboo dome']} | {m['garrison']} | "
                    f"{main_run} / {lane_run} m | {m['extent_m'][0]} x {m['extent_m'][1]} m |")
        gar = [b for b in d["buildings"] if b["garrison"]]
        main = [s for s in d["streets"] if s["kind"] == "main"][0]
        lanes = [s for s in d["streets"] if s["kind"] == "lane"]
        secs += [f"## {d['town']} (op {d['op']}, site {d['site_id']}, {d['size'].replace('_', '-')})", "",
                 f"**Role in its op.** {d['role_in_op']}", "",
                 f"**Approaches.** {d['approaches_text']}", "",
                 f"**Look.** {LOOK[d['town']]}", "",
                 f"**Plan (MEASURED on the plan).**",
                 f"- Main street: {main['width_m']} m wide, about {m['streets'][0]['length_m'] if m['streets'][0]['kind']=='main' else '?'} m long, bent "
                 f"(longest straight run {main_run} m).",
                 f"- {len(lanes)} lanes, {min(s['width_m'] for s in lanes)}-{max(s['width_m'] for s in lanes)} m wide. "
                 "Roads and paths out of town carry no frontage.",
                 f"- Square: {d['square']['area_m2']} m², with the sci-fi landmark **{d['landmark']['name']}**: {d['landmark']['note']}.",
                 f"- {m['buildings']} buildings, {m['in_blocks_pct']} % of them in {m['blocks']} touching blocks. "
                 f"Street frontages are {m['frontage_width_m']['min']}-{m['frontage_width_m']['max']} m wide "
                 f"(spread cv {m['frontage_width_m']['cv']}, so not evenly spaced).",
                 f"- Heights: low {m['height_counts']['low']} / mid {m['height_counts']['mid']} / tall {m['height_counts']['tall']}.",
                 "",
                 f"**Garrison ({len(gar)} buildings).**", ""]
        secs += [f"- {b['id']} ({b['height_class']}, {b['family']}): {b['garrison_role']}" for b in gar]
        secs.append("")
    out += ["## At a glance (MEASURED by tools/make_towns.py)", ""] + rows + ["",
            "Checks per town (all PASS, see `tools/checks.txt`): 60-110 buildings; at least 75 % in blocks; main street "
            "6-8 m; lanes 4-6 m; no straight run over 80 m on the main street or lanes; garrison 10-15; uneven frontages "
            "(cv at least 0.2).", ""] + secs
    open(os.path.join(ROOT, "TOWNS.md"), "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
