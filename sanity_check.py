import sys
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def compile_all_py(root: Path):
    errors = []
    for p in root.rglob('*.py'):
        # skip virtualenv and hidden folders
        if any(part.startswith('.') or part in ('venv', '__pycache__') for part in p.parts):
            continue
        try:
            py_compile.compile(str(p), doraise=True)
        except py_compile.PyCompileError as e:
            errors.append((p, str(e)))
    return errors

if __name__ == '__main__':
    errs = compile_all_py(ROOT)
    if not errs:
        print('Sanity check passed: all .py files compile.')
        sys.exit(0)
    print('Sanity check found compile errors:')
    for p, msg in errs:
        print(f'- {p}: {msg}')
    sys.exit(2)
