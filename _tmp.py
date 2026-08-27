import re
import sys

sys.path.insert(0, "scripts")
sys.path.insert(0, "scripts/checks")
from toolbox import http_get, to_text
import tier0_zai as z

t = to_text(http_get(z.URL, timeout=60))
secs = z.SECTION_RE.findall(t)
print("sections:", len(secs))
for s in secs:
    print("--- section head:", s[:60].replace("\n", " | "))
for sec in secs:
    if "per 1M tokens" not in sec:
        continue
    rows = z.ROW_RE.findall(sec)
    print("rows found:", len(rows))
    for r in rows[:5]:
        print("  ", r)
    if "GLM-5.2" in sec:
        i = sec.find("GLM-5.2")
        print("  GLM-5.2 context:", sec[i:i + 160].replace("\n", " | "))
