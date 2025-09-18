import subprocess

scripts = [
    "passa_banda/filtro_rlc.py",
    "passa_banda/filtro_rlc2.py",
    "passa_banda/filtro_rlc3.py",
]

processes = [subprocess.Popen(["python3", s]) for s in scripts]

for p in processes:
    p.wait()
