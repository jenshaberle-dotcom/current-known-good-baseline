"""Execute RCC-selected CKGB validation suites from trusted main policy."""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys
from pathlib import Path

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()

def verify(plan, policy, *, source_sha, base_sha):
    expected={"schema_version","repository","source_sha","base_sha","policy_sha","policy_digest","policy_version","runtime_fingerprint","action","suite_ids","selection_reasons","omissions","execution_digest","plan_digest"}
    if not isinstance(plan,dict) or set(plan)!=expected or plan["schema_version"]!="rcc.validation_test_plan.v1": raise ValueError("test_plan_shape_invalid")
    if digest({k:v for k,v in plan.items() if k!="plan_digest"})!=plan["plan_digest"]: raise ValueError("test_plan_digest_invalid")
    identity=("repository","source_sha","base_sha","policy_sha","policy_digest","runtime_fingerprint","suite_ids")
    if digest({k:plan[k] for k in identity})!=plan["execution_digest"]: raise ValueError("test_execution_digest_invalid")
    if plan["source_sha"]!=source_sha or plan["base_sha"]!=base_sha or plan["policy_sha"]!=base_sha: raise ValueError("test_plan_source_mismatch")
    if any(not re.fullmatch(r"[0-9a-f]{40}",plan[k]) for k in ("source_sha","base_sha","policy_sha")): raise ValueError("test_plan_source_invalid")
    if policy["repository"]!=plan["repository"] or digest(policy)!=plan["policy_digest"] or policy["version"]!=plan["policy_version"]: raise ValueError("test_plan_policy_mismatch")
    action=policy["actions"].get(plan["action"]); ids=plan["suite_ids"]
    if not action or not isinstance(ids,list) or not ids or len(ids)!=len(set(ids)) or any(k not in policy["suites"] for k in ids) or not set(action["required"]).issubset(ids): raise ValueError("test_plan_required_suite_missing")
    for i,k in enumerate(ids):
        if not set(policy["suites"][k]["requires"]).issubset(ids[:i]): raise ValueError("test_plan_dependency_missing_or_out_of_order")
    return [cmd for k in ids for cmd in policy["suites"][k]["commands"]]

def main():
    raw=os.environ["RCC_TEST_PLAN"]
    if len(raw.encode())>4096: raise ValueError("test_plan_too_large")
    plan=json.loads(raw); trusted=plan["policy_sha"]
    if not re.fullmatch(r"[0-9a-f]{40}",trusted): raise ValueError("test_policy_sha_invalid")
    source=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    if source!=os.environ["SOURCE_SHA"]: raise ValueError("test_source_mismatch")
    if plan["runtime_fingerprint"]!=os.environ["RCC_TEST_RUNTIME_FINGERPRINT"]: raise ValueError("test_runtime_identity_mismatch")
    policy=json.loads(subprocess.check_output(["git","show",f"{trusted}:.rcc/test-management.json"],text=True))
    commands=verify(plan,policy,source_sha=source,base_sha=trusted)
    for command in commands:
        if not isinstance(command,list) or not command or command[0]!="{python}": raise ValueError("trusted_test_command_invalid")
        subprocess.run([sys.executable,*command[1:]],check=True)
    receipt={"schema_version":"rcc.validation_test_receipt.v1","source_sha":source,"base_sha":trusted,"plan_digest":plan["plan_digest"],"execution_digest":plan["execution_digest"],"suite_ids":plan["suite_ids"],"status":"PASS"}
    out=Path("artifacts/validation-test-receipt.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    print(json.dumps(receipt,sort_keys=True))
if __name__=="__main__": main()
