import subprocess

scripts = [
    "passa_altas/filtro_rc.py",
    "passa_altas/filtro_rc2.py",
    "passa_altas/filtro_rc3.py",
]

processes = [subprocess.Popen(["python3", s]) for s in scripts]

for p in processes:
    p.wait()
