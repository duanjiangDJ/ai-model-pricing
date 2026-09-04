import os, re, glob

TPL = '''"""Independent collector for {name} (official source)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))
from collect.utils import fetch_markdown, write_prices  # noqa: E402
from checks.tier{tier}_{pid} import parse  # noqa: E402

URL = "{url}"
PROVIDER_ID = "{pid}"


def collect(ctx):
    now = ctx.get("now")
    text = fetch_markdown(URL)
    updates = parse(text)
    n = len(updates)
    changed = write_prices(PROVIDER_ID, updates, "tier{tier}_{pid}:source", now)
    return {{"changed": changed, "status": "ok", "detail": f"parsed {{n}} models, {{changed}} changed"}}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({{"now": None}}), ensure_ascii=False))
'''

seen = set()
for f in sorted(glob.glob('../checks/tier[01]_*.py')):
    base = os.path.basename(f)[:-3]
    mm = re.match(r'^tier([01])_(.+)$', base)
    if not mm:
        continue
    tier, pid = mm.group(1), mm.group(2)
    txt = open(f, encoding='utf-8').read()
    url = re.search(r'^URL\s*=\s*"([^"]*)"', txt, re.M)
    has_parse = bool(re.search(r'^def parse[^(]*\(', txt, re.M))
    if not (url and url.group(1) and has_parse):
        continue  # no URL or no parse -> not auto-collectable this way
    if pid in seen:
        continue
    seen.add(pid)
    out = f'collect_{pid}.py'
    open(out, 'w', encoding='utf-8').write(TPL.format(name=pid, pid=pid, url=url.group(1), tier=tier))
    print('generated', out)
