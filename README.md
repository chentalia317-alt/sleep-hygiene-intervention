# 💤 Sleep Hygiene Intervention Study: Data Analysis Repository

This repository contains the cleaned dataset and analysis scripts for my **sleep hygiene intervention experiment**, which examined how different behavioral interventions affect subjective sleepiness (KSS) and sleep duration among young participants aged **18–30**.

The project reflects an end-to-end scientific workflow — from data collection and cleaning to statistical analysis and reproducibility via GitHub.


## Background

Modern young adults often experience poor sleep quality due to irregular schedules and pre-bed electronic device use.  
This study explores how simple, low-cost behavioral interventions can improve circadian alignment and subjective alertness.

## Study Design

- **Participants**  
  Thirty volunteers (aged 18–30) were recruited through online communities.  
  Each participant gave informed consent and received a unique anonymized ID (P001–P030).  

- **Experimental Phases**  
  1. **Baseline (5 days):** Participants maintained their usual routines to establish individual sleep baselines.  
  2. **Intervention A – Fixed Sleep Window (7 days):** Participants followed a consistent bedtime and wake-up schedule.  
  3. **Intervention B – No Device Before Bed (7 days):** Participants avoided using electronic devices within 30 minutes before sleep.

- **Measurements**  
  - **Subjective sleepiness (KSS):** Reported at 10:00 AM, 3:00 PM, and 9:00 PM daily.  
  - **Sleep onset and wake time:** Self-reported and partially verified via wearable devices.  
  - **Task compliance rate:** Daily completion of assigned tasks (0 = not completed, 1 = completed).


## Daily Task Structure

### Intervention A — Fixed Sleep Window
- **on_time_bed:** Go to bed within the designated time window.  
- **no_caffeine:** Avoid caffeine intake after the afternoon.  
- **clean_environment:** Maintain a tidy, cool, and quiet sleep environment.  

### Intervention B — No Device Before Bed
- **no_device:** Refrain from using any electronic devices within 30 minutes before sleep.  
- **reduce_light:** Lower environmental light intensity (after 22:30) before bedtime.  
- **outdoor_light:** Ensure at least 30 minutes of natural daylight exposure after getting up.  

Each task was coded as 0/1 and aggregated to compute a **compliance rate** per participant per phase:  

> **Compliance rate = (Number of tasks completed) / (Total assigned tasks)**

This rate served as a proxy for behavioral adherence and was later examined as a covariate when interpreting KSS and sleep-duration changes.


## Project Structure
sleep-hygiene-intervention/
 ├── data/
│  ├── raw/                         # Unprocessed source data
│  └── cleaned/                     # Cleaned and merged datasets
│      ├── baseline_cleaned_v7.csv
│      ├── intervention_A_cleaned.csv
│      ├── intervention_B_cleaned.csv
│      ├── combined_dataset.csv
│      ├── delta_by_participant.csv
│      ├── delta_kss_boxplot.png
│      ├── delta_sleep_boxplot.png
│      └── results_summary.csv
│
 ├── scripts/
│   ├── combine_data.py              # Data merging and cleaning
│   ├── analyze_data.py              # Descriptive statistics
│   ├── analyze_effects.py           # t-test comparison
│   └── analyze_delta_and_plot.py    # Delta analysis & visualization
│
├── LICENSE                          # MIT License
└── README.md                        # Documentation
## Methods of Data Processing and Analysis

1. **Data Cleaning**  
   - Removed invalid or incomplete records.  
   - Standardized time formats (HH:MM) and corrected cross-midnight entries.  
   - Matched each participant’s baseline and intervention data.

2. **Data Integration**  
   - Combined using `combine_data.py`.  
   - Generated unified dataset: `combined_dataset.csv`.

3. **Statistical Analysis**  
   - Calculated each participant’s mean KSS and sleep duration.  
   - Computed ΔKSS and ΔSleep Duration (Intervention − Baseline).  
   - Conducted independent two-sample *t*-tests between groups A and B (p < 0.05 as significance threshold).  
   - Added **compliance rate** as an exploratory covariate.

4. **Visualization**  
   - Generated boxplots of ΔKSS and ΔSleep Duration using `matplotlib`.  
   - Output files stored in `data/cleaned/`.

5. **Behavioral compliance**

To account for participant adherence to the intervention protocols, a compliance rate was computed for each participant during the 7-day intervention phase.  
Each intervention (A: Fixed Sleep Window, B: No Device Before Bed) consisted of **three daily behavioral tasks**, and completion of each was coded as `1` (completed) or `0` (not completed).  
The compliance rate was calculated as:
$$
\text{Compliance rate} = \frac{\text{# tasks marked 1}}{3 \times \text{days in phase}}
$$
This measure was used to quantify behavioral engagement and interpret variability in sleepiness and sleep duration outcomes.  
For example, **one participant in Group B did not comply with the “no-device before bed” rule on any of the seven days**, leading to a near-zero compliance rate and limited improvement in sleep outcomes.  

## Preliminary Results

| Metric | Group A (Fixed Sleep Window) | Group B (No Device Before Bed) | *p*-value | Interpretation |
|---------|------------------------------|----------------------------------|-----------|----------------|
| ΔKSS (Intervention − Baseline) | −0.09 ± 0.62 | −0.46 ± 1.17 | 0.25 | Not significant |
| ΔSleep Duration (h) | +0.28 ± 0.62 | −0.37 ± 1.17 | 0.40 | Not significant |

> Although differences were not statistically significant, the trend suggested that maintaining a **fixed sleep window** might better stabilize circadian rhythms and reduce subjective sleepiness.

## Future Directions

- Increase sample size to enhance statistical power.  
- Integrate objective physiological data (e.g., HRV, actigraphy).  
- Incorporate **compliance rate** as a covariate in regression modeling.  
- Extend study duration to observe long-term circadian stabilization.  

## License and Ethical Statement

- Licensed under the **MIT License**.  
- All data are anonymized and used solely for educational and research purposes.  
- Analyses and visualizations are fully reproducible with provided scripts.  