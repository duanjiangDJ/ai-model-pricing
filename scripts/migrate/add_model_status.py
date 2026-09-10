"""One-shot migration: materialise the implicit "online" model status.

Historically `status` was optional and absent meant "live". Audit/schema now treat it as
explicit, so fill every missing status with "online". Existing (offline/online) untouched.
"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROVIDERS = os.path.join(ROOT, "data", "feed", "providers")


def main():
    n = 0
    touched = 0
    for path in sorted(glob.glob(os.path.join(PROVIDERS, "*.json"))):
        d = json.load(open(path))
        changed = False
        for m in d.get("models", []):
            if "status" not in m:
                m["status"] = "online"
                n += 1
                changed = True
        if changed:
            with open(path, "w") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write("\n")
            touched += 1
    print(f"filled status=online for {n} models across {touched} files")


if __name__ == "__main__":
    main()
