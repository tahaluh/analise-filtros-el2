import subprocess

scripts = [
    "passa_baixas/filtro_rl.py",
    "passa_baixas/filtro_rl2.py",
    "passa_baixas/filtro_rl3.py",
]

processes = [subprocess.Popen(["python3", s]) for s in scripts]

for p in processes:
    p.wait()
