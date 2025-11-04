# Background: Sleep Intervention Study

## 1. Introduction

Human physiology follows rhythmic patterns that govern everything from hormone release to cognitive alertness. Among them, the **circadian system** coordinates the balance between sleep and wakefulness. When this internal clock drifts—through irregular schedules, inconsistent light exposure, or social jet lag—cognitive performance and emotional regulation can both decline.

This project examines how simple, behavior-based interventions might strengthen circadian alignment and improve daily alertness. The idea draws on recent studies of **glymphatic clearance** and the link between **circadian rhythms and brain metabolism**, focusing on whether small, consistent habits can produce measurable improvements in rhythmic stability.

---

## 2. Hypothesis and Objectives

**Hypothesis:**  
Behavioral adjustments that reinforce circadian regularity will lead to steadier daytime alertness, as reflected in *Karolinska Sleepiness Scale (KSS)* scores and wearable data.

**Objectives:**  
1. Measure variation in subjective alertness throughout the day using KSS.  
2. Compare baseline and post-intervention data under two conditions (A/B).  
3. Visualize changes in alertness distribution across time of day.  
4. Develop a reproducible, open-source workflow for behavioral physiology analysis.

---

## 3. Methods Overview

Data were collected using a **within-subject design** over multiple sessions.  
Participants (n = 30) recorded hourly KSS scores and wearable metrics during baseline and intervention phases.

**Procedure:**
- **Baseline:** normal lifestyle conditions.  
- **Intervention A:** fixed sleep and wake times.  
- **Intervention B:** reduced screen exposure and increased morning light.  
- Data processed in Python (`pandas`, `numpy`, `matplotlib`).  
- Automated reporting through a custom Quarkdown-based pipeline integrated with GitHub Actions.

---

## 4. Results Summary

Preliminary results indicate smaller day-to-day fluctuations in KSS scores after interventions, with a clearer diurnal pattern under Intervention A.  
These trends suggest improved alignment between behavioral schedule and internal circadian rhythm.

---

## 5. Discussion

The data support earlier findings that **consistent routines promote circadian stability**.  
Although modest in scale, this experiment demonstrates that behavioral rhythms can be modeled and quantified with open-source computational tools.  
Limitations include a small sample and reliance on self-reported measures; expanding the dataset and incorporating markers like core-body temperature or melatonin onset would strengthen future work.

---

## 6. Reproducibility Statement

All data and analysis scripts are openly available:  
- **GitHub:** [https://github.com/chentalia317-alt/sleep-hygiene-intervention]  
- **OSF:** [https://osf.io/5s6me/overview]

The repository includes cleaned datasets, Python notebooks, and automatically generated Quarkdown reports (`report.html`, `dashboard.html`).  
This documentation is intended to support **transparency, reproducibility, and educational reuse** in behavioral rhythm research.

---

## 7. Reference

- Xie, L., Kang, H., Xu, Q., Chen, M. J., Liao, Y., Thiyagarajan, M., ... & Nedergaard, M. (2013). Sleep drives metabolite clearance from the adult brain. science, 342(6156), 373-377.
- Roenneberg, T., Pilz, L. K., Zerbini, G., & Winnebeck, E. C. (2019). Chronotype and social jetlag: a (self-) critical review. Biology, 8(3), 54.
---

*Authored by [[Talia Chen](https://github.com/chentalia317-alt)] (2025). Independent research on circadian rhythm and behavioral physiology conducted during high school.*
