import zipfile, os, sys

submission_dir = os.path.join(os.getcwd(), "submission")
zip_path = os.path.join(os.getcwd(), "submission.zip")

if os.path.exists(zip_path):
    os.remove(zip_path)
    print("Removed old submission.zip")

files = []
for root, dirs, fnames in os.walk(submission_dir):
    for fn in sorted(fnames):
        fp = os.path.join(root, fn)
        arcname = os.path.relpath(fp, submission_dir)
        files.append((fp, arcname))

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for fp, arcname in sorted(files, key=lambda x: x[1]):
        zf.write(fp, arcname)
        print(f"  Added: {arcname} ({os.path.getsize(fp)} bytes)")

print(f"\nsubmission.zip: {os.path.getsize(zip_path)} bytes, {len(files)} files")

with zipfile.ZipFile(zip_path, "r") as zf:
    names = zf.namelist()
    print(f"\nVerification:")
    for n in names:
        print(f"  {n}")

    has_agent_yaml = "agent.yaml" in names
    print(f"\nagent.yaml at root: {has_agent_yaml}")

    explorer_content = zf.read("sub_agents/code_explorer.yaml").decode()
    assert "prompts/explorer.md" in explorer_content, "FAIL: !include path not fixed"
    assert "../prompts" not in explorer_content, "FAIL: .. still in path"
    print("!include path fixed: OK")

    system_content = zf.read("prompts/system.md").decode()
    assert "{hints}" not in system_content, "FAIL: {hints} still in system prompt"
    print("System prompt trimmed: OK")

    sampling = zf.read("configs/sampling.yaml").decode()
    assert "thinking_budget: 2048" in sampling, "FAIL: thinking_budget not updated"
    print("Thinking budget lowered: OK")

print("\nAll checks passed!")
