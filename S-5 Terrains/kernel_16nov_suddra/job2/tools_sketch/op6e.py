"""Op 6 drop 2, approaches A4 pass (HUMAN): op6d on pack v8, which carries the 6-M1 W causeway and its cut.
A chain runs from the causeway's far end, 1,400 m out toward 6-04, to 6-M1, so the road leaves 6-M1 on its W side (AI: how the causeway is put on the net)."""
from op6d import *          # noqa: F401,F403
TRUNKS = [[dict(stop=("xyz", (9010.8, 10573.6)), name="6-M1 causeway end", label="6-M1 W causeway end toward 6-04 (approaches A4)"),
           dict(stop=("site", "6-M1"), through=False, kind="dirt", width=7.0, grade=0.14)]]
