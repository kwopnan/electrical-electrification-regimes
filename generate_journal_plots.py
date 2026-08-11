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
    """Loads CSV file, detects PSU active phase, zeros time axis, and calculates resistance/power."""
    df = pd.read_csv(filepath)
    time_col = 'Elapsed_s' if 'Elapsed_s' in df.columns else ('Time_s' if 'Time_s' in df.columns else None)
    if time_col is None:
        return None
        
    # Active electrification filter: Voltage > 1V and Current > 0.05A
    mask = (df['Voltage_V'] > 1.0) & (df['Current_A'] > 0.05)
    active = df[mask].copy()
    if active.empty:
        return None
        
    t0 = active[time_col].iloc[0]
    active['t_zero'] = active[time_col] - t0
    active['R_ohm'] = active['Voltage_V'] / active['Current_A']
    active['R_norm'] = active['R_ohm'] / active['R_ohm'].iloc[0]
    active['Power_W'] = active['Voltage_V'] * active['Current_A']
    
    return active

# Regimes configuration
regimes = {
    'sub_tg': {
        'label': r'$T_g - 20^\circ\text{C}$ (Sub-$T_g$)',
        'dir': os.path.join(data_dir, '20degreesBelowTg'),
        'color': '#005AB5',       # Royal Blue
        'light_color': '#90CAF9', # Light Blue
        'rep_file': 'log20degreesLess_19Jan2026_TX4BS1.csv'
    },
    'tg': {
        'label': r'$T_g$ (At $T_g$)',
        'dir': os.path.join(data_dir, 'Tg'),
        'color': '#DC2626',       # Crimson Red
        'light_color': '#FCA5A5', # Light Red
        'rep_file': 'log_25Jan2026_TX4BS8.csv'
    },
    'super_tg': {
        'label': r'$T_g + 20^\circ\text{C}$ (Super-$T_g$)',
        'dir': os.path.join(data_dir, '20degreesAboveTg'),
        'color': '#059669',       # Emerald Green
        'light_color': '#A7F3D0', # Light Green
        'rep_file': 'log_25Jan2026_TX4BS10.csv'
    }
}

# ==============================================================================
# FIGURE 1: Primary Journal Figure (2 Panels: R(t) and R(t)/R0)
# ==============================================================================
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), dpi=300)

for reg_key, reg_data in regimes.items():
    csv_files = glob.glob(os.path.join(reg_data['dir'], '*.csv'))
    
    # First plot all individual runs with light/thin lines for reproducibility
    for f in sorted(csv_files):
        fname = os.path.basename(f)
        if fname == reg_data['rep_file']:
            continue
        df_run = load_and_preprocess(f)
        if df_run is not None:
            ax1.plot(df_run['t_zero'], df_run['R_ohm'], color=reg_data['light_color'], lw=1.0, alpha=0.75, ls='--')
            ax2.plot(df_run['t_zero'], df_run['R_norm'], color=reg_data['light_color'], lw=1.0, alpha=0.75, ls='--')

# Now plot representative runs with thick solid lines
for reg_key, reg_data in regimes.items():
    rep_path = os.path.join(reg_data['dir'], reg_data['rep_file'])
    df_rep = load_and_preprocess(rep_path)
    if df_rep is not None:
        ax1.plot(df_rep['t_zero'], df_rep['R_ohm'], label=reg_data['label'], color=reg_data['color'], lw=2.4)
        ax2.plot(df_rep['t_zero'], df_rep['R_norm'], label=reg_data['label'], color=reg_data['color'], lw=2.4)

# Formatting Panel (a)
ax1.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=11, fontweight='bold')
ax1.set_ylabel(r'Electrical Resistance, $R$ ($\Omega$)', fontsize=11, fontweight='bold')
ax1.set_title(r'(a) Absolute Electrical Resistance', fontsize=11, fontweight='bold', loc='left', pad=10)
ax1.grid(True, which='major', linestyle=':', color='#CCCCCC', alpha=0.8)
ax1.set_xlim(0, 160)
ax1.set_ylim(0, 8.0)
ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax1.legend(frameon=True, edgecolor='#333333', facecolor='white', framealpha=0.95, fontsize=9.5, loc='upper right')

# Formatting Panel (b)
ax2.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=11, fontweight='bold')
ax2.set_ylabel(r'Normalized Resistance, $R / R_0$', fontsize=11, fontweight='bold')
ax2.set_title(r'(b) Normalized Resistance Decay', fontsize=11, fontweight='bold', loc='left', pad=10)
ax2.grid(True, which='major', linestyle=':', color='#CCCCCC', alpha=0.8)
ax2.set_xlim(0, 160)
ax2.set_ylim(0, 1.05)
ax2.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
ax2.legend(frameon=True, edgecolor='#333333', facecolor='white', framealpha=0.95, fontsize=9.5, loc='upper right')

plt.tight_layout()

# Save Figure 1
fig1_png_ws = os.path.join(data_dir, "electrification_resistance_journal_fig.png")
fig1_pdf_ws = os.path.join(data_dir, "electrification_resistance_journal_fig.pdf")
fig1_png_art = os.path.join(artifact_dir, "electrification_resistance_journal_fig.png")
fig1_pdf_art = os.path.join(artifact_dir, "electrification_resistance_journal_fig.pdf")

fig1.savefig(fig1_png_ws, dpi=300, bbox_inches='tight')
fig1.savefig(fig1_pdf_ws, dpi=300, bbox_inches='tight')
fig1.savefig(fig1_png_art, dpi=300, bbox_inches='tight')
fig1.savefig(fig1_pdf_art, dpi=300, bbox_inches='tight')
plt.close(fig1)

print(f"Primary Journal Figure saved to:\n  {fig1_png_ws}\n  {fig1_pdf_ws}")

# ==============================================================================
# FIGURE 2: Multi-Metric Composite Figure (4 Panels: R(t), R/R0, Temp(t), Power(t))
# ==============================================================================
fig2, ((ax_a, ax_b), (ax_c, ax_d)) = plt.subplots(2, 2, figsize=(12, 9), dpi=300)

for reg_key, reg_data in regimes.items():
    rep_path = os.path.join(reg_data['dir'], reg_data['rep_file'])
    df_rep = load_and_preprocess(rep_path)
    if df_rep is None:
        continue

    # (a) Resistance
    ax_a.plot(df_rep['t_zero'], df_rep['R_ohm'], label=reg_data['label'], color=reg_data['color'], lw=2.2)
    # (b) Normalized Resistance
    ax_b.plot(df_rep['t_zero'], df_rep['R_norm'], label=reg_data['label'], color=reg_data['color'], lw=2.2)
    # (c) Temperature (Ch1 thermocouple)
    if 'Temp_Ch1_C' in df_rep.columns:
        ax_c.plot(df_rep['t_zero'], df_rep['Temp_Ch1_C'], label=reg_data['label'], color=reg_data['color'], lw=2.2)
    # (d) Power
    ax_d.plot(df_rep['t_zero'], df_rep['Power_W'], label=reg_data['label'], color=reg_data['color'], lw=2.2)

# Panel (a)
ax_a.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=10, fontweight='bold')
ax_a.set_ylabel(r'Electrical Resistance, $R$ ($\Omega$)', fontsize=10, fontweight='bold')
ax_a.set_title(r'(a) Absolute Electrical Resistance', fontsize=10.5, fontweight='bold', loc='left')
ax_a.grid(True, linestyle=':', alpha=0.7)
ax_a.legend(frameon=True, fontsize=9, loc='upper right')

# Panel (b)
ax_b.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=10, fontweight='bold')
ax_b.set_ylabel(r'Normalized Resistance, $R / R_0$', fontsize=10, fontweight='bold')
ax_b.set_title(r'(b) Relative Resistance Decay', fontsize=10.5, fontweight='bold', loc='left')
ax_b.grid(True, linestyle=':', alpha=0.7)
ax_b.legend(frameon=True, fontsize=9, loc='upper right')

# Panel (c)
ax_c.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=10, fontweight='bold')
ax_c.set_ylabel(r'Specimen Temperature, $T$ ($^\circ\text{C}$)', fontsize=10, fontweight='bold')
ax_c.set_title(r'(c) Temperature Response (Thermocouple Ch. 1)', fontsize=10.5, fontweight='bold', loc='left')
ax_c.grid(True, linestyle=':', alpha=0.7)
ax_c.legend(frameon=True, fontsize=9, loc='lower right')

# Panel (d)
ax_d.set_xlabel(r'Electrification Time, $t$ (s)', fontsize=10, fontweight='bold')
ax_d.set_ylabel(r'Joule Heating Power, $P$ (W)', fontsize=10, fontweight='bold')
ax_d.set_title(r'(d) Electrical Power Input', fontsize=10.5, fontweight='bold', loc='left')
ax_d.grid(True, linestyle=':', alpha=0.7)
ax_d.legend(frameon=True, fontsize=9, loc='upper right')

plt.tight_layout()

fig2_png_ws = os.path.join(data_dir, "electrification_multimetric_journal_fig.png")
fig2_pdf_ws = os.path.join(data_dir, "electrification_multimetric_journal_fig.pdf")
fig2_png_art = os.path.join(artifact_dir, "electrification_multimetric_journal_fig.png")
fig2_pdf_art = os.path.join(artifact_dir, "electrification_multimetric_journal_fig.pdf")

fig2.savefig(fig2_png_ws, dpi=300, bbox_inches='tight')
fig2.savefig(fig2_pdf_ws, dpi=300, bbox_inches='tight')
fig2.savefig(fig2_png_art, dpi=300, bbox_inches='tight')
fig2.savefig(fig2_pdf_art, dpi=300, bbox_inches='tight')
plt.close(fig2)

print(f"Supplementary Multi-Metric Figure saved to:\n  {fig2_png_ws}\n  {fig2_pdf_ws}")
