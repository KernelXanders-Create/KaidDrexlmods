"""Op 3 drop 2, approaches A4 pass (HUMAN): op3r3 on pack v8, which carries the 3-M2 W and 3-M4 NW causeways.
The existing trunk from 1-F to 3-M2 now has a dry way over the 3-M2 causeway. A new chain runs from the 3-M4 causeway's far end (3-05) to 3-M4,
so the road leaves 3-M4 on its NW side (AI: how the causeway is put on the net)."""
from op3r3 import *          # noqa: F401,F403
import op3r3
TRUNKS = op3r3.TRUNKS + [[dict(stop=("xyz", (10300.0, 2500.0)), name="3-M4 causeway end", label="3-M4 NW causeway end at 3-05 (approaches A4)"),
                          dict(stop=("site", "3-M4"), through=False, kind="dirt", width=7.0, grade=0.14)]]
