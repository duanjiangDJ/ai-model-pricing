import os, re, glob

TPL = '''"""Independent collector for {name} (official source)."""
import os, sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _THIS)
sys.path.insert(0, os.path.abspath(os.path.join(_THIS, "..")))
from collect.base import fetch_markdown, write_prices  # noqa: E402
from checks.tier0_{pid} import parse  # noqa: E402

URL = "{url}"
PROVIDER_ID = "{pid}"


def collect(ctx):
    now = ctx.get("now")
    text = fetch_markdown(URL)
    updates = parse(text)
    n = len(updates)
    changed = write_prices(PROVIDER_ID, updates, "tier0_{pid}:source", now)
    return {{"changed": changed, "status": "ok", "detail": f"parsed {{n}} models, {{changed}} changed"}}


if __name__ == "__main__":
    import json
    print(json.dumps(collect({{"now": None}}), ensure_ascii=False))
'''

for f in sorted(glob.glob('../checks/tier0_*.py')):
    pid = os.path.basename(f)[6:-3]
    txt = open(f, encoding='utf-8').read()
    m = re.search(r'^URL\s*=\s*"([^"]*)"', txt, re.M)
    if not m or not m.group(1):
        continue  # needs a URL; js_fetch or special-loop providers handled separately
    out = f'collect_{pid}.py'
    open(out, 'w', encoding='utf-8').write(TPL.format(name=pid, pid=pid, url=m.group(1)))
    print('generated', out)
