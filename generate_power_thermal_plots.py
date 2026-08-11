import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Configure Matplotlib for publication quality
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.major.width'] = 1.2
plt.rcParams['ytick.major.width'] = 1.2
plt.rcParams['xtick.minor.width'] = 0.8
plt.rcParams['ytick.minor.width'] = 0.8
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True

data_dir = r"c:\Users\kwopd\OneDrive\Desktop\Electrical software\data"
artifact_dir = r"C:\Users\kwopd\.gemini\antigravity\brain\31256a28-7c5e-4711-be3c-9bc4e8513182"

def load_and_preprocess(filepath):
    df = pd.read_csv(filepath)
    time_col = 'Elapsed_s' if 'Elapsed_s' in df.columns else ('Time_s' if 'Time_s' in df.columns else None)
    if time_col is None:
        return None
        
    mask = (df['Voltage_V'] > 1.0) & (df['Current_A'] > 0.05)
    active = df[mask].copy()
    if active.empty:
        return None
        
    t0 = active[time_col].iloc[0]
    active['t_zero'] = active[time_col] - t0
    active['Power_W'] = active['Voltage_V'] * active['Current_A']
    
    # Cumulative Energy (kJ)
    t_sec = active['t_zero'].values
    p_watt = active['Power_W'].values
    energy_j = np.zeros(len(t_sec))
    if len(t_sec) > 1:
        dt = np.diff(t_sec)
        p_mid = 0.5 * (p_watt[:-1] + p_watt[1:])
        energy_j[1:] = np.cumsum(p_mid * dt)
    active['Energy_kJ'] = energy_j / 1000.0
    
    return active

# Regimes configuration
regimes = {
    'sub_tg': {
        'label': r'$T_g - 20^\circ\text{C}$ (Sub-$T_g$)',
        'dir': os.path.join(data_dir, '20degreesBelowTg'),
        'color': '#005AB5',
        'rep_file': 'log20degreesLess_19Jan2026_TX4BS2.csv' # TX4BS2
    },
    'tg': {
        'label': r'$T_g$ (At $T_g$)',
        'dir': os.path.join(data_dir, 'Tg'),
        'color': '#DC2626',
        'rep_file': 'log_25Jan2026_TX4BS8.csv'
    },
    'super_tg': {
        'label': r'$T_g + 20^\circ\text{C}$ (Super-$T_g$)',
        'dir': os.path.join(data_dir, '20degreesAboveTg'),
        'color': '#059669',
        'rep_file': 'log_25Jan2026_TX4BS10.csv'
    }
}

# ==============================================================================
# COMPOSITE FIGURE: Power Dissipation & Thermal Threshold Kinetics
# ==============================================================================
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12.5, 9.5), dpi=300)

# Load representative data
rep_dfs = {}
for reg_key, reg_data in regimes.items():
    fpath = os.path.join(reg_data['dir'], reg_data['rep_file'])
    df_rep = load_and_preprocess(fpath)
    if df_rep is not None:
        rep_dfs[reg_key] = df_rep

# (a) Power Dissipation P(t) over Time
for reg_key, reg_data in regimes.items():
    if reg_key in rep_dfs:
        df = rep_dfs[reg_key]
        ax1.plot(df['t_zero'], df['Power_W'], label=reg_data['label'], color=reg_data['color'], lw=2.2)

ax1.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=11, fontweight='bold')
ax1.set_ylabel(r'Electrical Power Dissipation, $P$ (W)', fontsize=11, fontweight='bold')
ax1.set_title(r'(a) Electrical Power Dissipation Profile', fontsize=11, fontweight='bold', loc='left', pad=8)
ax1.grid(True, linestyle=':', color='#CCCCCC', alpha=0.8)
ax1.legend(frameon=True, edgecolor='#333333', facecolor='white', framealpha=0.95, fontsize=9.5, loc='upper right')
ax1.set_xlim(0, 160)
ax1.set_ylim(0, 180)

# (b) Cumulative Energy Dissipation E(t) over Time
for reg_key, reg_data in regimes.items():
    if reg_key in rep_dfs:
        df = rep_dfs[reg_key]
        ax2.plot(df['t_zero'], df['Energy_kJ'], label=reg_data['label'], color=reg_data['color'], lw=2.2)

ax2.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=11, fontweight='bold')
ax2.set_ylabel(r'Cumulative Dissipated Energy, $E$ (kJ)', fontsize=11, fontweight='bold')
ax2.set_title(r'(b) Cumulative Energy Input', fontsize=11, fontweight='bold', loc='left', pad=8)
ax2.grid(True, linestyle=':', color='#CCCCCC', alpha=0.8)
ax2.legend(frameon=True, edgecolor='#333333', facecolor='white', framealpha=0.95, fontsize=9.5, loc='upper left')
ax2.set_xlim(0, 160)

# Extract Thermal Threshold Data for Tg and Super-Tg experiments
thresholds = [30, 40, 50, 60, 70, 80]

thermal_runs = {
    r'$T_g - 20^\circ\text{C}$ (Sample TX4BS2)': {'file': os.path.join(data_dir, '20degreesBelowTg', 'log20degreesLess_19Jan2026_TX4BS2.csv'), 'color': '#005AB5', 'marker': 'v'},
    r'$T_g$ (Sample TX4BS7)': {'file': os.path.join(data_dir, 'Tg', 'log_25Jan2026_TX4BS7.csv'), 'color': '#EF4444', 'marker': 'o'},
    r'$T_g$ (Sample TX4BS8)': {'file': os.path.join(data_dir, 'Tg', 'log_25Jan2026_TX4BS8.csv'), 'color': '#DC2626', 'marker': 's'},
    r'$T_g$ (Sample TX4BS9)': {'file': os.path.join(data_dir, 'Tg', 'log_25Jan2026_TX4BS9.csv'), 'color': '#991B1B', 'marker': '^'},
    r'$T_g + 20^\circ\text{C}$ (Sample TX4BS10)': {'file': os.path.join(data_dir, '20degreesAboveTg', 'log_25Jan2026_TX4BS10.csv'), 'color': '#059669', 'marker': 'D'}
}

# (c) Time Required to Reach Prescribed Thermal Thresholds
for run_name, run_info in thermal_runs.items():
    df = load_and_preprocess(run_info['file'])
    if df is not None and 'Temp_Ch1_C' in df.columns:
        t_req = []
        e_req = []
        thresh_reached = []
        for th in thresholds:
            match = df[df['Temp_Ch1_C'] >= th]
            if not match.empty:
                t_req.append(match['t_zero'].iloc[0])
                e_req.append(match['Energy_kJ'].iloc[0])
                thresh_reached.append(th)
        
        ax3.plot(thresh_reached, t_req, label=run_name, color=run_info['color'], marker=run_info['marker'], ms=7, lw=2.0)
        ax4.plot(thresh_reached, e_req, label=run_name, color=run_info['color'], marker=run_info['marker'], ms=7, lw=2.0)

# Panel (c) formatting
ax3.set_xlabel(r'Prescribed Thermal Threshold, $T_{\text{target}}$ ($^\circ\text{C}$)', fontsize=11, fontweight='bold')
ax3.set_ylabel(r'Time Required to Reach Threshold, $t_{\text{req}}$ (s)', fontsize=11, fontweight='bold')
ax3.set_title(r'(c) Time Required to Reach Thermal Thresholds', fontsize=11, fontweight='bold', loc='left', pad=8)
ax3.grid(True, linestyle=':', color='#CCCCCC', alpha=0.8)
ax3.legend(frameon=True, edgecolor='#333333', facecolor='white', framealpha=0.95, fontsize=9.0, loc='upper left')
ax3.set_xticks(thresholds)

# Panel (d) formatting
ax4.set_xlabel(r'Prescribed Thermal Threshold, $T_{\text{target}}$ ($^\circ\text{C}$)', fontsize=11, fontweight='bold')
ax4.set_ylabel(r'Cumulative Dissipated Energy, $E_{\text{req}}$ (kJ)', fontsize=11, fontweight='bold')
ax4.set_title(r'(d) Energy Required to Reach Thermal Thresholds', fontsize=11, fontweight='bold', loc='left', pad=8)
ax4.grid(True, linestyle=':', color='#CCCCCC', alpha=0.8)
ax4.legend(frameon=True, edgecolor='#333333', facecolor='white', framealpha=0.95, fontsize=9.0, loc='upper left')
ax4.set_xticks(thresholds)

plt.tight_layout()

# Save Figures
fig_png_ws = os.path.join(data_dir, "power_dissipation_thermal_thresholds_fig.png")
fig_pdf_ws = os.path.join(data_dir, "power_dissipation_thermal_thresholds_fig.pdf")
fig_png_art = os.path.join(artifact_dir, "power_dissipation_thermal_thresholds_fig.png")
fig_pdf_art = os.path.join(artifact_dir, "power_dissipation_thermal_thresholds_fig.pdf")

fig.savefig(fig_png_ws, dpi=300, bbox_inches='tight')
fig.savefig(fig_pdf_ws, dpi=300, bbox_inches='tight')
fig.savefig(fig_png_art, dpi=300, bbox_inches='tight')
fig.savefig(fig_pdf_art, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"Power Dissipation & Thermal Threshold Figure updated with TX4BS2 saved to:\n  {fig_png_ws}\n  {fig_pdf_ws}")
