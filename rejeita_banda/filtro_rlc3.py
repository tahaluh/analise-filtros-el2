import schemdraw
import schemdraw.elements as elm
import numpy as np
import matplotlib.pyplot as plt

# Valores do filtro
R_value = 1.5e3   # 1.5 kΩ
L_value = 25e-3 # 25 mH
C_value = 2e-6  # 2 µF

# Frequências de corte (rad/s)
wc1 = -R_value/(2*L_value) + np.sqrt((R_value/(2*L_value))**2 + 1/(L_value*C_value))
wc2 =  R_value/(2*L_value) + np.sqrt((R_value/(2*L_value))**2 + 1/(L_value*C_value))

# Frequência de ressonância
w0 = 1 / np.sqrt(L_value * C_value)

# Desenho do circuito RLC série Rejeita-Banda
d = schemdraw.Drawing()
d += elm.Label().label("Filtro Rejeita-Banda RLC Série", fontsize=16, loc='top').at((2,7))
d += elm.Line().up().length(d.unit*0.5)
d += elm.SourceV().up().label('Vin', loc='top')
d += elm.Line().up().length(d.unit*0.5)
d += elm.Dot()
d += elm.Resistor().right().label(f'R = {R_value/1e3:.1f} kΩ', loc='top')
d += elm.Dot()
d += elm.Line().right().length(d.unit*0.5)
d += elm.Dot().label('+', loc='bottom')
d += elm.Line().left().length(d.unit*0.5)
d += elm.Inductor().down().label(f'L = {L_value*1e3:.1f} mH', loc='top')
d += elm.Dot()
d += elm.Capacitor().down().label(f'C = {C_value*1e6:.1f} µF', loc='top')
d += elm.Dot()
d += elm.Line().right().length(d.unit*0.5)
d += elm.Dot().label('Vout\n\n\n\n\n\n-', loc='top')
d += elm.Line().left().length(d.unit*1.5)
d.draw()

# Simulação da resposta em frequência
f = np.logspace(1, 5, 1000)   # Hz
w = 2 * np.pi * f             # rad/s

# Módulo linear
mag_linear = np.abs((1 - w**2 * L_value * C_value) / 
                    np.sqrt((1 - w**2 * L_value * C_value)**2 + (w * R_value * C_value)**2))

# Fase em graus
phase = -np.arctan2(w * R_value * C_value, 1 - w**2 * L_value * C_value) * (180/np.pi)

# Plot dos gráficos
plt.figure(figsize=(8,6))

# Módulo |H(jω)|
plt.subplot(2,1,1)
plt.semilogx(w, mag_linear, label='|H(jω)|')
plt.axvline(wc1, color='r', linestyle='--', label=f'ωc1 = {wc1:.1f} rad/s')
plt.axvline(wc2, color='r', linestyle='--', label=f'ωc2 = {wc2:.1f} rad/s')
plt.axvline(w0, color='g', linestyle='--', label=f'ω0 = {w0:.1f} rad/s')
plt.title("Resposta em Frequência - Filtro Rejeita-Banda RLC Série")
plt.ylabel("|H(jω)|")
plt.grid(True, which="both", ls="--")
plt.legend()

# Fase ∠H(jω)
plt.subplot(2,1,2)
plt.semilogx(w, phase, label='Fase H(jω)')
plt.axvline(wc1, color='r', linestyle='--', label=f'ωc1 = {wc1:.1f} rad/s')
plt.axvline(wc2, color='r', linestyle='--', label=f'ωc2 = {wc2:.1f} rad/s')
plt.axvline(w0, color='g', linestyle='--', label=f'ω0 = {w0:.1f} rad/s')
plt.xlabel("Frequência Angular ω [rad/s]")
plt.ylabel("Fase [graus]")
plt.grid(True, which="both", ls="--")
plt.legend()

plt.tight_layout()
plt.show()
