import subprocess

scripts = [
    "rejeita_banda/filtro_rlc.py",
    "rejeita_banda/filtro_rlc2.py",
    "rejeita_banda/filtro_rlc3.py",
    "rejeita_banda/filtro_rlc4.py",
]

processes = [subprocess.Popen(["python3", s]) for s in scripts]

for p in processes:
    p.wait()
