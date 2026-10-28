from pathlib import Path
import re
root = Path(__file__).resolve().parent.parent / "skills"
expected=['visual-design-architect','interactive-deck-studio','isometric-interface-builder','visual-quality-auditor']
errors=[]
for name in expected:
 p=root/name/'SKILL.md'
 if not p.exists(): errors.append(f'Missing: {p}'); continue
 raw=p.read_text(encoding='utf-8')
 if not raw.startswith('---\n'):errors.append(f'Invalid frontmatter: {name}');continue
 m=re.match(r'---\n(.*?)\n---\n',raw,re.S)
 if not m:errors.append(f'Missing frontmatter end: {name}');continue
 fm=m.group(1)
 if f'name: {name}' not in fm or 'description:' not in fm:errors.append(f'Missing metadata: {name}')
 if len(name)>64:errors.append(f'Long name: {name}')
 print(f'OK {name}: {len(raw.splitlines())} lines')
for path in root.rglob('SKILL.md'):
 if path.parent.name not in expected:errors.append(f'Unexpected skill: {path}')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print('PASS: estructura y metadatos básicos presentes')
