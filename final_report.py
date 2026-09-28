import zipfile, os

# Verify submission.zip
zip_path = os.path.join(os.getcwd(), "submission.zip")
print("=== Current submission.zip ===")
print(f"Size: {os.path.getsize(zip_path)} bytes")

with zipfile.ZipFile(zip_path, "r") as zf:
    names = zf.namelist()
    print(f"Files: {len(names)}")
    for n in names:
        print(f"  {n}")

    # Verify the fixes
    print("\n=== Fix Verification ===")

    # 1. Check !include path in code_explorer.yaml
    content = zf.read("sub_agents/code_explorer.yaml").decode()
    if "prompts/explorer.md" in content and "../prompts" not in content:
        print("[PASS] !include path fixed: uses prompts/explorer.md (no .. traversal)")
    else:
        print("[FAIL] !include path NOT fixed correctly")

    # 2. Check system.md doesn't have redundant hints
    system_content = zf.read("prompts/system.md").decode()
    if "{hints}" not in system_content:
        print("[PASS] system.md: removed {hints} from template (redundant with harness messages)")
    else:
        print("[FAIL] system.md still has {hints} template variable")

    # 3. Check thinking_budget
    sampling = zf.read("configs/sampling.yaml").decode()
    if "thinking_budget: 2048" in sampling:
        print("[PASS] configs/sampling.yaml: thinking_budget lowered to 2048")
    else:
        print("[FAIL] configs/sampling.yaml: thinking_budget not updated")

    # 4. Check agent.yaml at root
    if "agent.yaml" in names:
        print("[PASS] agent.yaml present at root (zip depth 0)")
    else:
        print("[FAIL] agent.yaml missing from root")

# Workspace state
print("\n=== WORKSPACE STATE ===")
for f in sorted(os.listdir()):
    full = os.path.join(os.getcwd(), f)
    if os.path.isfile(full):
        print(f"  {f} ({os.path.getsize(full)} bytes)")
    elif os.path.isdir(full):
        dirs = [d for d in os.listdir(full) if not d.startswith('.')]
        print(f"  {f}/ ({len(dirs)} items)")

print("\n=== BLOCKERS ===")
print("1. Kaggle CLI: HTTPS requests fail with Schannel SEC_E_NO_CREDENTIALS")
print("2. GitHub API: Same Schannel credential issue")
print("3. curl.exe: Same Schannel credential issue")
print("\nThe submission.zip is ready but cannot be submitted via HTTPS.")

# Cleanup temp files
try:
    os.remove("try_kaggle.py")
    os.remove("kaggle_retry.py")
    os.remove("diag_ssl.py")
    os.remove("kaggle_resubmit.py")
    print("\nCleaned up temp Python files")
except:
    pass