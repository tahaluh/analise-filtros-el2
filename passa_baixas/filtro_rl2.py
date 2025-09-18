import schemdraw
import schemdraw.elements as elm
import numpy as np
import matplotlib.pyplot as plt
# aumentar R (mantendo L)
# curva desliza para a esquerda (diminui fc), inclinação idem.
# A impedância de entrada aumenta, mas o indutor não muda.
# Menos energia magnética armazenada ⇒ pode afetar resposta transitória.

# Valores do filtro RL
# Objetivo: Subwoofer passa-baixas com frequência de corte em 100 Hz
R_value = 40       # 40 Ω
L_value = 6.37e-3 # 6.37 mH

# Frequência de corte
f_c = R_value / (2 * np.pi * L_value)  # Hz
w_c = 2 * np.pi * f_c                  # rad/s

# Desenho do circuito RL Passa-Baixa
d = schemdraw.Drawing()
d += elm.Label().label("Filtro Passa-Baixa RL (2ª Variação)", fontsize=16, loc='top').at((2,4))
d += elm.SourceV().up().label('Vin', loc='left')
d += elm.Dot()
d += elm.Inductor().right().label(f'L = {L_value*1e3:.2f} mH', loc='top')
d += elm.Dot()
d += elm.Line().right().length(d.unit*1.5)
d += elm.Dot().label('+', loc='bottom')
d += elm.Line().left().length(d.unit*1.5)
d += elm.Resistor().down().label(f'R = {R_value:.1f} Ω', loc='bottom')
d += elm.Dot()
d += elm.Line().right().length(d.unit*1.5)
d += elm.Dot().label('Vout\n\n\n-', loc='top')
d += elm.Line().left().length(d.unit*2.5)
d.draw()

# Simulação da resposta em frequência
f = np.logspace(1, 5, 1000)   # Hz (10 Hz a 100 kHz)
w = 2 * np.pi * f             # rad/s

# Função de transferência H(jω)
mag_linear = R_value / np.sqrt(R_value**2 + (w*L_value)**2)
mag_db = 20 * np.log10(mag_linear)
phase = -np.arctan(w*L_value / R_value) * (180/np.pi)

# --- Plot em função da frequência angular (rad/s) ---
plt.figure(figsize=(9,7))

plt.subplot(2,1,1)
plt.semilogx(w, mag_linear, label='|H(jω)| (linear)')
plt.axvline(w_c, color='r', linestyle='--', label=f'ωc = {w_c:.1f} rad/s')
plt.title("Resposta em Frequência - Filtro Passa-Baixa RL (2ª Variação) (ω)")
plt.ylabel("|H(jω)|")
plt.grid(True, which="both", ls="--")
plt.legend()

plt.subplot(2,1,2)
plt.semilogx(w, phase, label='Fase H(jω)')
plt.axvline(w_c, color='r', linestyle='--')
plt.xlabel("Frequência Angular ω [rad/s]")
plt.ylabel("∠H(jω) [graus]")
plt.grid(True, which="both", ls="--")
plt.legend()

plt.tight_layout()
plt.show()

# --- Plot em função da frequência (Hz) ---
plt.figure(figsize=(9,7))

plt.subplot(2,1,1)
plt.semilogx(f, mag_db, label='|H(jω)| [dB]')
plt.axvline(f_c, color='r', linestyle='--', label=f'fc = {f_c:.1f} Hz')
plt.title("Resposta em Frequência - Filtro Passa-Baixa RL (2ª Variação) (Hz)")
plt.ylabel("Magnitude [dB]")
plt.grid(True, which="both", ls="--")
plt.legend()

plt.subplot(2,1,2)
plt.semilogx(f, phase, label='Fase H(jω)')
plt.axvline(f_c, color='r', linestyle='--')
plt.xlabel("Frequência [Hz]")
plt.ylabel("∠H(jω) [graus]")
plt.grid(True, which="both", ls="--")
plt.legend()

plt.tight_layout()
plt.show()
