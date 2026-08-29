#!/usr/bin/env python3
import argparse, json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STOP = set("""a an and are as at be been being but by can could did do does for from had has have having how if in into is it its may might more most must need needs of on or our should so than that the their them then there these they this those to want we what when where which while who will with would you your business company firm organization team work make making help provide build building support approach analysis framework method plan process question issue result output decision day days week weeks month months quarter year years one two three first next last large small role employee people time new current existing possible specific different across within without after before already only just about around versus vs top major material limited request requested name clear action added adding appear case choose create evidence feel informal intervention lower metric outcome person plausible pre recommendation tied""".split())
CANON = {
    "organizational":"organization", "organisation":"organization", "org":"organization",
    "pricing":"price", "prices":"price", "profitable":"profit", "profitability":"profit", "profits":"profit",
    "financial":"finance", "finances":"finance", "operational":"operation", "operations":"operation",
    "customers":"customer", "clients":"customer", "client":"customer", "employees":"employee", "people":"employee",
    "capabilities":"capability", "competencies":"competence", "strategic":"strategy", "strategies":"strategy",
    "markets":"market", "products":"product", "services":"service", "risks":"risk", "risky":"risk",
    "costs":"cost", "revenues":"revenue", "margins":"margin", "sales":"sale", "teams":"team", "systems":"system", "controls":"control",
    "acquisitions":"acquisition", "acquire":"acquisition", "acquiring":"acquisition",
    "technologies":"technology", "digital":"technology", "cybersecurity":"cyber", "security":"cyber",
    "liquidity":"cash", "cashflow":"cash", "workflows":"workflow", "transformation":"change", "changing":"change", "changes":"change",
    "approval":"approve", "approvals":"approve", "approved":"approve", "approver":"approve", "approvers":"approve",
    "delegated":"delegate", "delegating":"delegate", "delegation":"delegate",
    "owner":"ownership", "owners":"ownership", "owns":"ownership", "owned":"ownership",
    "accountable":"accountability", "accountabilities":"accountability",
    "rebaseline":"baseline", "rebaselined":"baseline", "rebaselining":"baseline",
    "delayed":"delay", "delays":"delay", "lateness":"late",
    "decarbonization":"carbon", "decarbonize":"carbon", "decarbonizing":"carbon", "emissions":"emission",
    "electrification":"electric", "electrify":"electric", "electrifying":"electric",
    "productize":"product", "productized":"product", "productizing":"product",
    "mandate":"change", "mandates":"change", "adoption":"adopt", "adopting":"adopt", "users":"adopt", "usage":"adopt", "uses":"adopt",
    "delivery":"deliver", "delivering":"deliver", "delivered":"deliver", "forecasting":"forecast", "forecasts":"forecast", "forecasted":"forecast",
    "promised":"forecast", "promise":"forecast", "promises":"forecast", "planning":"plan", "diagnosis":"diagnose", "diagnostic":"diagnose",
    "prioritization":"prioritize", "prioritise":"prioritize", "governance":"govern", "governing":"govern",
    "measurement":"measure", "measuring":"measure", "implementation":"implement", "implementing":"implement",
    "designing":"design", "designs":"design", "growth":"grow", "growing":"grow", "turnaround":"recovery",
    "recovering":"recovery", "restructure":"recovery", "restructuring":"recovery", "churned":"churn", "churning":"churn",
    "retention":"retain", "retained":"retain", "retaining":"retain", "activation":"activate", "activated":"activate", "onboarding":"activate",
    "headcount":"capacity", "staffing":"capacity", "constraints":"constraint", "constrained":"constraint", "bottlenecks":"bottleneck",
    "diligence":"diligence", "due":"diligence", "merger":"ma", "artificial":"ai", "intelligence":"ai"
}

def tokens(value):
    text = " ".join(map(str, value)) if isinstance(value, list) else str(value or "")
    out = set()
    for word in re.findall(r"[a-z]+", text.lower().replace("&", " and ")):
        word = CANON.get(word, word)
        if word in STOP or len(word) < 2:
            continue
        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"
        elif word.endswith("s") and len(word) > 4 and not word.endswith("ss"):
            word = word[:-1]
        word = CANON.get(word, word)
        if word not in STOP:
            out.add(word)
    return out

def read_json(path):
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value

def load_index(path):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("index must be a non-empty JSON array")
    return rows

def route(brief, rows):
    needed = {"problem","decision","context","constraints","desired_output","practice_areas","reasoning_jobs"}
    missing = sorted(needed - set(brief))
    if missing:
        raise ValueError("missing brief fields: " + ", ".join(missing))
    list_fields = ("constraints","practice_areas","reasoning_jobs")
    if not all(isinstance(brief[field], list) for field in list_fields):
        raise ValueError("constraints, practice_areas, and reasoning_jobs must be arrays")
    if not all(isinstance(value, str) for field in list_fields for value in brief[field]):
        raise ValueError("constraints, practice_areas, and reasoning_jobs must contain strings")
    for field, key in (("practice_areas","a"), ("reasoning_jobs","j")):
        unknown = sorted(set(brief[field]) - {value for row in rows for value in row[key]})
        if unknown:
            raise ValueError("unknown " + field + ": " + ", ".join(unknown))
    query = tokens([brief["problem"], brief["decision"], brief["context"], brief["desired_output"], *brief["constraints"]])
    areas, jobs = set(brief["practice_areas"]), set(brief["reasoning_jobs"])
    docs = [tokens([row["n"], row["q"]]) for row in rows]
    counts = {}
    for doc in docs:
        for word in doc:
            counts[word] = counts.get(word, 0) + 1
    idf = {word: math.log((len(rows)+1)/(count+1))+1 for word, count in counts.items()}
    scored = []
    for row, doc in zip(rows, docs):
        overlap = query & doc
        key = query & tokens(row["k"])
        score = .55 * sum(idf.get(word, 1) for word in overlap)
        score += 1.2 * sum(idf.get(word, 1) for word in key) + .3 * row.get("p", 1)
        for pos, area in enumerate(row["a"]):
            if area in areas:
                score += 4 if pos == 0 else 1.5
        for pos, job in enumerate(row["j"]):
            if job in jobs:
                score += 4 if pos == 0 else 1.25
        warnings = []
        for phrase in row["x"]:
            avoid = tokens(phrase)
            if len(avoid) >= 3 and len(query & avoid) >= 3 and len(query & avoid) / len(avoid) >= .65:
                score -= 5
                warnings.append("avoid condition matched")
        matched = sorted(overlap, key=lambda word: (-idf.get(word, 1), word))[:5]
        scored.append({"row":row, "score":score, "matched":matched, "warnings":warnings})
    chosen = []
    while scored and len(chosen) < 6:
        for item in scored:
            row = item["row"]
            item["pick"] = item["score"] - (1.5 if any(old["row"]["f"] == row["f"] and old["row"]["j"][0] == row["j"][0] for old in chosen) else 0)
        item = sorted(scored, key=lambda value: (-value["pick"], -value["row"].get("p", 1), value["row"]["i"]))[0]
        scored.remove(item); chosen.append(item)
    methods = []
    for item in chosen:
        row = item["row"]
        fit_parts = [area for area in row["a"] if area in areas] + [job for job in row["j"] if job in jobs] + item["matched"][:3]
        method = {"id":row["i"], "name":row["n"], "fit":", ".join(dict.fromkeys(fit_parts)), "method_path":"methods/"+row["i"]+".md"}
        if item["warnings"]:
            method["warning"] = item["warnings"][0]
        methods.append(method)
    return {"methods":methods}

def validate_plan(plan, rows, methods_dir):
    errors, warnings = [], []
    required = ["case_summary","selected_methods","assumptions","missing_inputs","expected_output"]
    for field in required:
        if field not in plan:
            errors.append("missing " + field)
    if "case_summary" in plan and not str(plan["case_summary"]).strip():
        errors.append("case_summary must be non-empty")
    if "expected_output" in plan and not str(plan["expected_output"]).strip():
        errors.append("expected_output must be non-empty")
    for field in ("assumptions", "missing_inputs"):
        if field in plan and not isinstance(plan[field], list):
            errors.append(field + " must be an array")
    selected = plan.get("selected_methods")
    if not isinstance(selected, list) or not 1 <= len(selected) <= 5:
        errors.append("selected_methods must contain 1-5 methods")
        selected = []
    by_id = {row["i"]:row for row in rows}
    ids, sequences = [], []
    for pos, item in enumerate(selected):
        if not isinstance(item, dict) or set(item) != {"id","role","sequence"}:
            errors.append(f"selected_methods[{pos}] must contain only id, role, sequence")
            continue
        mid = item["id"]
        if not isinstance(mid, str) or mid not in by_id:
            errors.append(f"unknown method: {mid}")
        elif not (methods_dir / (mid+".md")).is_file():
            errors.append(f"missing method file: {mid}")
        if not isinstance(item["role"], str) or not item["role"].strip():
            errors.append(f"empty role: {mid}")
        if not isinstance(item["sequence"], int) or isinstance(item["sequence"], bool):
            errors.append(f"invalid sequence: {mid}")
        else:
            sequences.append(item["sequence"])
        if isinstance(mid, str):
            ids.append(mid)
    if len(set(ids)) != len(ids):
        errors.append("method ids must be unique")
    if sequences and sorted(sequences) != list(range(1, len(selected)+1)):
        errors.append("sequences must be 1..N")
    if len(selected) >= 4 and not str(plan.get("breadth_justification", "")).strip():
        errors.append("breadth_justification required for 4-5 methods")
    positions = {item.get("id"):item.get("sequence") for item in selected if isinstance(item, dict) and isinstance(item.get("id"), str)}
    for i, left in enumerate(ids):
        if left not in by_id:
            continue
        for right in ids[i+1:]:
            if right in by_id and (right in by_id[left].get("c", []) or left in by_id[right].get("c", [])):
                errors.append(f"conflicting methods: {left}, {right}")
    overrides = plan.get("sequence_overrides", [])
    if not isinstance(overrides, list):
        errors.append("sequence_overrides must be an array"); overrides = []
    for before in ids:
        if before not in by_id:
            continue
        for after in by_id[before].get("b", []):
            if after in positions and positions.get(before, 0) > positions.get(after, 0):
                matches = [item for item in overrides if isinstance(item, dict) and item.get("before_id") == before and item.get("after_id") == after and str(item.get("justification", "")).strip()]
                if len(matches) != 1:
                    errors.append(f"reversed order requires override: {before} -> {after}")
    for i, left in enumerate(ids):
        if left not in by_id:
            continue
        for right in ids[i+1:]:
            if right in by_id and by_id[left]["f"] == by_id[right]["f"] and by_id[left]["j"][0] == by_id[right]["j"][0]:
                warnings.append(f"possible redundancy: {left}, {right}")
    return {"ok":not errors, "errors":errors, "warnings":warnings}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["route","plan"])
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        data, rows = read_json(args.input), load_index(ROOT / "registry" / "index.json")
        result = route(data, rows) if args.command == "route" else validate_plan(data, rows, ROOT / "methods")
        print(json.dumps(result, separators=(",",":")))
        return 0 if result.get("ok", True) else 1
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("error: " + str(error), file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main())
