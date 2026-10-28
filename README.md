# Electrical Electrification Experiments Across Temperature Regimes

This repository contains measured electrical resistance data, processing scripts, and journal-ready figures for representative electrification experiments conducted across three distinct thermal regimes:
1. **$T_g - 20^\circ\text{C}$ (Sub-$T_g$)**
2. **$T_g$ (At Glass Transition Temperature)**
3. **$T_g + 20^\circ\text{C}$ (Super-$T_g$)**

---

## 📌 Repository Structure

```
.
├── 20degreesBelowTg/              # Experimental CSV & XLSX logs for Sub-Tg regime
├── Tg/                            # Experimental CSV logs for Tg regime
├── 20degreesAboveTg/               # Experimental CSV logs for Super-Tg regime
├── generate_journal_plots.py      # Main Python script to process data and generate publication plots
├── electrification_resistance_journal_fig.png  # 2-Panel Primary Journal Figure (300 DPI)
├── electrification_resistance_journal_fig.pdf  # Vector PDF Primary Figure for journal submission
├── electrification_multimetric_journal_fig.png # 4-Panel Supplementary Figure
├── electrification_multimetric_journal_fig.pdf # Vector PDF Supplementary Figure
└── README.md                      # Project documentation
```

---

## ⚡ Key Methodology & Results

- **Time Synchronization ($t = 0\text{ s}$)**: The start of active electrification is synchronized to $t = 0\text{ s}$ by detecting power supply output activation ($V > 1.0\text{ V}, I > 0.05\text{ A}$).
- **Ohm's Law Calculation**: Electrical resistance $R(t) = \frac{V(t)}{I(t)}$ is calculated dynamically during active power supply output.
- **Resistance Decay Profile**: Electrical resistance drops monotonically from initial values ($R_0 \approx 5.5 - 6.8\,\Omega$) to a lower asymptote ($R_\infty \approx 1.7 - 1.86\,\Omega$).

### Representative Runs Summary

| Regime | Representative File | Active Duration | $R_0$ ($\Omega$) | $R_\infty$ ($\Omega$) | Peak Temp ($^\circ\text{C}$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$T_g - 20^\circ\text{C}$ (Sub-$T_g$)** | `20degreesBelowTg/log20degreesLess_19Jan2026_TX4BS1.csv` | 153.5 s | 6.21 | 1.86 | ~41.8 |
| **$T_g$ (At $T_g$)** | `Tg/log_25Jan2026_TX4BS8.csv` | 115.0 s | 5.57 | 1.74 | ~86.5 |
| **$T_g + 20^\circ\text{C}$ (Super-$T_g$)** | `20degreesAboveTg/log_25Jan2026_TX4BS10.csv` | 57.8 s | 6.75 | 1.72 | ~76.4 |

---

## 🚀 How to Run

Ensure Python 3.x is installed with `pandas`, `numpy`, `matplotlib`, and `openpyxl`:

```bash
pip install pandas numpy matplotlib openpyxl
python generate_journal_plots.py
```

---

## 🛡️ Laboratory safety documentation

- `/home/runner/work/electrical-electrification-regimes/electrical-electrification-regimes/LAB_RISK_ASSESSMENT_SOP.md` — Risk assessment, safe operating procedure, and pre-energised commissioning/approval checklist for heated CFRP electrification testing.
