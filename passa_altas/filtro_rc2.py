import schemdraw
import schemdraw.elements as elm
import numpy as np
import matplotlib.pyplot as plt

# Valores do filtro  (segunda variação)
R_value = 2e3   # 2 kΩ
C_value = 4e-6  # 4 μF

# Frequência de corte
f_c = 1 / (2 * np.pi * R_value * C_value)  # Hz
w_c = 2 * np.pi * f_c                      # rad/s

# Desenho do circuito RC Passa-Alta
d = schemdraw.Drawing()
d += elm.Label().label("Filtro Passa-Alta RC (2ª Variação)", fontsize=16, loc='top').at((3,4))
d += elm.SourceV().up().label('Vin', loc='left')
d += elm.Dot()
d += elm.Capacitor().right().label(f'C = {C_value*1e6:.1f}µF', loc='top')
d += elm.Dot()
d += elm.Line().right().length(d.unit*1.5)
d += elm.Dot().label('+', loc='bottom')
d += elm.Line().left().length(d.unit*1.5)
d += elm.Resistor().down().label(f'R = {R_value/1e3:.1f}kΩ', loc='bottom')
d += elm.Dot()
d += elm.Line().right().length(d.unit*1.5)
d += elm.Dot().label('Vout\n\n\n-', loc='top')
d += elm.Line().left().length(d.unit*2.5)
d.draw()

# Simulação da resposta em frequência
f = np.logspace(1, 5, 1000)   # Hz
w = 2 * np.pi * f             # rad/s

# Módulo linear
mag_linear = (w*R_value*C_value) / np.sqrt(1 + (w*R_value*C_value)**2)

# Fase em graus
phase = np.arctan(1/(w*R_value*C_value)) * (180/np.pi)

# Plot dos gráficos de módulo e fase
plt.figure(figsize=(8,6))

# Módulo |H(jω)|
plt.subplot(2,1,1)
plt.semilogx(w, mag_linear, label='|H(jω)|')
plt.axvline(w_c, color='r', linestyle='--', label=f'Frequência de corte = {w_c:.1f} rad/s')
plt.title("Resposta em Frequência - Filtro Passa-Alta RC (2ª Variação)")
plt.ylabel("|H(jω)|")
plt.grid(True, which="both", ls="--")
plt.legend()

# Fase ∠H(jω)
plt.subplot(2,1,2)
plt.semilogx(w, phase, label='Fase H(jω)')
plt.axvline(w_c, color='r', linestyle='--', label=f'Frequência de corte = {w_c:.1f} rad/s')
plt.xlabel("Frequência Angular ω [rad/s]")
plt.ylabel("Fase [graus]")
plt.grid(True, which="both", ls="--")
plt.legend()

plt.tight_layout()
plt.show()
