import schemdraw
import schemdraw.elements as elm
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# Parâmetros fixos (BW ~ 10 kHz)
# ===============================
R_value = 15.8        # ohms   (BW ≈ R/(2πL))
L_value = 250e-6      # 250 µH

# Escolha da estação AM (kHz) — só mudar aqui
station_kHz = 1110.0  # ex.: 1340 (Correio), 1280 (Sanhauá), 1110 (Tabajara)

# Calcula C para sintonizar exatamente station_kHz
f0_target = station_kHz * 1e3
C_value = 1.0 / ((2*np.pi*f0_target)**2 * L_value)
print(f"C para {station_kHz:.0f} kHz = {C_value*1e12:.2f} pF")

# -------------------------------
# Cálculos de f0, fc1, fc2
# -------------------------------
wc1 = -R_value/(2*L_value) + np.sqrt((R_value/(2*L_value))**2 + 1/(L_value*C_value))
wc2 =  R_value/(2*L_value) + np.sqrt((R_value/(2*L_value))**2 + 1/(L_value*C_value))

w0  = 1 / np.sqrt(L_value * C_value)
f0  = w0 / (2*np.pi)
fc1 = wc1 / (2*np.pi)
fc2 = wc2 / (2*np.pi)

print(f"fc1 = {fc1/1e6:.4f} MHz, fc2 = {fc2/1e6:.4f} MHz, f0 = {f0/1e6:.4f} MHz")

# -------------------------------
# Desenho do circuito (labels ok)
# -------------------------------
d = schemdraw.Drawing()
d += elm.Label().label(f"Passa-Banda — Tabajara AM", fontsize=16, loc='top').at((3,4))
d += elm.SourceV().up().label('Vin', loc='left')
d += elm.Dot()
d += elm.Inductor().right().label(f'L = {L_value*1e6:.0f} µH',  loc='top')        # 250 µH
d += elm.Dot()
d += elm.Capacitor().right().label(f'C = {C_value*1e12:.1f} pF', loc='top')        # calculado p/ estação
d += elm.Dot()
d += elm.Line().right().length(d.unit*0.5)
d += elm.Dot().label('+', loc='bottom')
d += elm.Line().left().length(d.unit*0.5)
d += elm.Resistor().down().label(f'R = {R_value:.1f} Ω',        loc='top')         # 15.8 Ω
d += elm.Dot()
d += elm.Line().right().length(d.unit*0.5)
d += elm.Dot().label('Vout\n\n\n-', loc='top')
d += elm.Line().left().length(d.unit*2.5)
d.draw()

# -------------------------------
# Faixa de análise em torno da estação
# (±5 larguras de banda ao redor de f0)
# -------------------------------
BW = fc2 - fc1
f_min = max(1e3, f0 - 5*BW)
f_max = f0 + 5*BW
f = np.logspace(np.log10(f_min), np.log10(f_max), 2000)
w = 2 * np.pi * f

# -------------------------------
# Função de transferência (saída no R)
# -------------------------------
mag_linear = (w * R_value * C_value) / np.sqrt((1 - (w**2) * L_value * C_value)**2 +
                                               (w * R_value * C_value)**2)
mag_db = 20 * np.log10(mag_linear)
phase = 90 - np.degrees(np.arctan2(w * R_value * C_value, 1 - (w**2) * L_value * C_value))

# ===============================
# Eixos em MHz e Mrad/s (Opção A)
# ===============================
f_MHz   = f   / 1e6
fc1_MHz = fc1 / 1e6
fc2_MHz = fc2 / 1e6
f0_MHz  = f0  / 1e6

w_Mrad   = w   / 1e6
wc1_Mrad = wc1 / 1e6
wc2_Mrad = wc2 / 1e6
w0_Mrad  = w0  / 1e6

# --- Plot em função de ω (Mrad/s) ---
plt.figure(figsize=(9,7))

ax1 = plt.subplot(2,1,1)
ax1.semilogx(w_Mrad, mag_linear, label='|H(jω)| (linear)')
ax1.axvline(wc1_Mrad, linestyle='--', label=f'ωc1 = {wc1_Mrad:.2f} Mrad/s')
ax1.axvline(wc2_Mrad, linestyle='--', label=f'ωc2 = {wc2_Mrad:.2f} Mrad/s')
ax1.axvline(w0_Mrad,  linestyle='--', label=f'ω0  = {w0_Mrad:.2f} Mrad/s')
ax1.set_title(f"Magnitude — AM {station_kHz:.0f} kHz (ω)")
ax1.set_ylabel("|H(jω)|")
ax1.grid(True, which="both", ls="--")
ax1.legend()

ax2 = plt.subplot(2,1,2)
ax2.semilogx(w_Mrad, phase, label='Fase H(jω)')
ax2.axvline(wc1_Mrad, linestyle='--')
ax2.axvline(wc2_Mrad, linestyle='--')
ax2.axvline(w0_Mrad,  linestyle='--')
ax2.set_title(f"Fase — AM {station_kHz:.0f} kHz (ω)")
ax2.set_xlabel("Frequência Angular ω [Mrad/s]")
ax2.set_ylabel("∠H(jω) [graus]")
ax2.grid(True, which="both", ls="--")
ax2.legend()

plt.tight_layout()
plt.show()

# --- Plot em função de f (MHz) ---
plt.figure(figsize=(9,7))

ax3 = plt.subplot(2,1,1)
ax3.semilogx(f_MHz, mag_db, label='|H(jω)| [dB]')
ax3.axvline(fc1_MHz, linestyle='--', label=f'fc1 = {fc1_MHz:.4f} MHz')
ax3.axvline(fc2_MHz, linestyle='--', label=f'fc2 = {fc2_MHz:.4f} MHz')
ax3.axvline(f0_MHz,  linestyle='--', label=f'f0  = {f0_MHz:.4f} MHz')
ax3.set_title(f"Magnitude — AM {station_kHz:.0f} kHz (f)")
ax3.set_ylabel("Magnitude [dB]")
ax3.grid(True, which="both", ls="--")
ax3.legend()

ax4 = plt.subplot(2,1,2)
ax4.semilogx(f_MHz, phase, label='Fase H(jω)')
ax4.axvline(fc1_MHz, linestyle='--')
ax4.axvline(fc2_MHz, linestyle='--')
ax4.axvline(f0_MHz,  linestyle='--')
ax4.set_title(f"Fase — AM {station_kHz:.0f} kHz (f)")
ax4.set_xlabel("Frequência [MHz]")
ax4.set_ylabel("∠H(jω) [graus]")
ax4.grid(True, which="both", ls="--")
ax4.legend()

plt.tight_layout()
plt.show()
