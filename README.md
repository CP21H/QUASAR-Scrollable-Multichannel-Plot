# QUASAR-Scrollable-Multichannel-Plot

## How to run
### Dependencies
Python 3.13 used, Python 3.8+ recommended <br>
Pandas must be installed to parse the CSV data <br>
```bash
pip install pandas
```
Plotly must be installed to plot the data <br>
```bash
pip install plotly
```

### Running the Script
```python
python plot.py
```

## Design Choices
### Preliminary Choices
Given that I am relatively unfamiliar with health related terminology, I wanted to first understand the terms being used in the dataset so as to better understand what exactly I am working on. To do this efficiently, I prompted Gemini 2.5 Flash to explain the following terminology: EEG Channels and what the naming schema was, ECG and EOG channels, as well as the significance of the Common Mode. 

### Scaling
EEG vs ECG signal scaling was handled through having two y-axes, `y1` and `y2`, where `y1` is the left axis of EEG channels (µV) and `y2` is the right axis of ECG + CM channels (mV).

### AI Assistance
This project's structure and initial script were developed with the help of ChatGPT, particularly GPT5, ensuring that proper and adequate comments were added as to improve first-time and subsequent readability. 


## Implementation
<details>
  
  <summary>Configuration</summary>
  
  ### Configuration
```python
file_path = "EEG and ECG data_02_raw.csv"  # adjust if needed

# Channels of interest
EEG_CHANNELS = ["Fz","Cz","P3","C3","F3","F4","C4","P4",
                "Fp1","Fp2","T3","T4","T5","T6","O1","O2",
                "F7","F8","A1","A2","Pz"]
ECG_CHANNELS = ["X1:LEOG", "X2:REOG"]
CM_CHANNEL   = ["CM"]
```
`file_path` is specified trivially. Given that there are relevant signals we want to parse specifically out of the dataset, and we have the label of the columns of interest, we can just store them in lists for convenience.

</details>

<details>
  
  <summary>Loading the Data</summary>

  ### Loading the Data
  ```python
  # Skip metadata lines beginning with '#'
  df = pd.read_csv(file_path, comment='#')
  
  # Keep only the columns we care about (ignore X3:, Trigger, etc.)
  wanted_cols = ["Time"] + EEG_CHANNELS + ECG_CHANNELS + CM_CHANNEL
  cols = [c for c in wanted_cols if c in df.columns]
  data = df[cols].copy()
  ```
  `df` is created as a `pandas` dataframe which stores row-column data. Pandas built in `read_csv` is leveraged here to parse through the dataset while ignoring the specified lines starting with `#`, being comments. 
  
  `wanted_cols` just consolidates the columns that we specifically want from the data. `cols` proceeds to filter out any columns that aren't actually in the CSV for some reason so as to prevent crashes. 
  
  A completely new dataframe `data` is then created using the previous `df` but selections only the columns we want and have.

</details>

<details>

  <summary>Plotting the Data</summary>

  ### Plotting the Data
  ```python
  fig = go.Figure()
  ```
  Create an empty Plotly figure such that we can add traces later.
  
  ```python
  # EEG traces on y-axis 'y1'
  for ch in EEG_CHANNELS:
      if ch in data.columns:
          fig.add_trace(go.Scatter(
              x=data["Time"], y=data[ch], name=ch, line=dict(width=1),
              yaxis="y1"
          ))
  ```
  Iterate over the EEG channels provided, checking if it is in the `data` dataframe, then adding the line trace itself, specifying the axes, name of the trace, width of the line and the y-axis to attach to.
  
  ```python
  # ECG + CM on secondary y-axis 'y2'
  for ch in ECG_CHANNELS + CM_CHANNEL:
      if ch in data.columns:
          fig.add_trace(go.Scatter(
              x=data["Time"], y=data[ch], name=ch, line=dict(width=1),
              yaxis="y2"
          ))
  ```
  Iterate over the ECG-CM channels provided, checking if it is in the `data` dataframe, then adding the line trace itself, specifying the axes, name of the trace, width of the line and the y-axis to attach to.
  
  ```python
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
  ```
  Update the layout of the plotly figure to prepare it for user visualization. 
  
</details>

## Results
<p align="center">
  <img width="1889" height="837" alt="image" src="https://github.com/user-attachments/assets/dad69ad4-1d59-4b78-9562-0c1e714897d0" />
  <em>Initial Plot</em>
</p>

<p align="center">
  <img width="1896" height="857" alt="image" src="https://github.com/user-attachments/assets/228681c6-17d0-4181-aba2-66dea5a5dcc9" />
  <em>2 Zoom Result</em>
</p>

<p align="center">
  <img width="1910" height="862" alt="image" src="https://github.com/user-attachments/assets/d55d03f2-ee1b-40fe-8bbd-a0f8a8ec56a9" />
  <em>Slider Zoom Application Result</em>
</p>
