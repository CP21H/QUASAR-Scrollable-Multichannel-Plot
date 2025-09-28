import pandas as pd
import plotly.graph_objects as go

# ---------- CONFIG ----------
file_path = "EEG and ECG data_02_raw.csv"  # adjust if needed

# Channels of interest
EEG_CHANNELS = ["Fz","Cz","P3","C3","F3","F4","C4","P4",
                "Fp1","Fp2","T3","T4","T5","T6","O1","O2",
                "F7","F8","A1","A2","Pz"]
ECG_CHANNELS = ["X1:LEOG", "X2:REOG"]
CM_CHANNEL   = ["CM"]

# ---------- LOAD DATA ----------
# Skip metadata lines beginning with '#'
df = pd.read_csv(file_path, comment='#')

# Keep only the columns we care about (ignore X3:, Trigger, etc.)
wanted_cols = ["Time"] + EEG_CHANNELS + ECG_CHANNELS + CM_CHANNEL
cols = [c for c in wanted_cols if c in df.columns]
data = df[cols].copy()

# ---------- BUILD FIGURE ----------
fig = go.Figure()

# EEG traces on y-axis 'y1'
for ch in EEG_CHANNELS:
    if ch in data.columns:
        fig.add_trace(go.Scatter(
            x=data["Time"], y=data[ch], name=ch, line=dict(width=1),
            yaxis="y1"
        ))

# ECG + CM on secondary y-axis 'y2'
for ch in ECG_CHANNELS + CM_CHANNEL:
    if ch in data.columns:
        fig.add_trace(go.Scatter(
            x=data["Time"], y=data[ch], name=ch, line=dict(width=1),
            yaxis="y2"
        ))

fig.update_layout(
    title="EEG & ECG Time-Series",
    xaxis=dict(title="Time (s)",
               rangeslider=dict(visible=True),  # enables scroll/zoom slider
               type="linear"),
    yaxis=dict(title="EEG (µV)"),
    yaxis2=dict(title="ECG / CM (mV)",
                overlaying="y", side="right"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="right", x=1)
)

fig.show()
