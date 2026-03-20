Overview
When a wildfire ignites, emergency managers face an impossible question with incomplete information. Which fires will reach populated areas? How quickly? And which communities should prepare first?

This year's WiDS Global Datathon challenges participants to build survival models that answer these questions using only the earliest signals available. Your task is to predict the probability that a wildfire will threaten an evacuation zone within 12, 24, 48, and 72 hours, drawing on data from just the first five hours after ignition.

The goal is not a single prediction but a calibrated forecast across multiple time horizons. Emergency responders need both urgency rankings (which fires demand immediate attention) and probability estimates they can trust when making high-stakes decisions about evacuations, resource deployment, and public alerts.

Description
Problem
When a wildfire ignites, emergency managers and responders must decide which communities to warn, when to warn them, and where to position scarce resources. Decisions must be made before certainty is available. The response requires both prioritization (which fires are most urgent soon) and calibrated risk estimates (how likely a fire is to threaten evacuation zones within actionable time windows).

This competition turns that operational need into a survival analysis challenge. You will generate calibrated probability forecasts across multiple time horizons to support real-world decisions.

Real-World Context
Many wildfire forecasting approaches reduce the task to a single question. Will this fire become dangerous. Emergency response needs more. Decisions are time-bound and comparative. How soon is a threat likely. How confident should we be. Which incident should move to the front of the queue when crews, aircraft, and messaging capacity are limited.

This competition addresses that gap by framing the task as survival analysis using real early-incident signals. The dataset captures wildfire perimeter dynamics and their spatial relationship to evacuation zones. Features are computed strictly from the first five hours after the initial perimeter observation, t0. The target is the time from t0 plus 5 hours until the fire comes within 5 km of any evacuation zone centroid.

Survival Analysis Framing and Censoring
This is right-censored survival analysis:

If a fire hits within the 72-hour window, event = 1 and time_to_hit_hours is the observed time from t0+5h.
If a fire does not hit within 72 hours, event = 0 and time_to_hit_hours is the last observed time in the window (<= 72).
Participants do not predict a single time. They submit survival probabilities that a hit occurs by 12h, 24h, 48h, and 72h. The strongest solutions will deliver two outcomes at once. They will rank fires correctly by urgency for triage and produce calibrated probabilities that can support threshold-based decisions.

Evaluation
Primary Metric:

Hybrid Score = 0.3 x C-index + 0.7 x (1 - Weighted Brier Score)

C-index (30%)
Measures how well you rank fires by urgency
Higher is better (0.5 to 1.0)
Weighted Brier Score (70%)
Measures calibration at 24h, 48h, 72h
Uses censor-aware evaluation:
Hits: 1 if hit by horizon H, else 0
Censored after H: 0
Censored before H: excluded
Final weighted average: 0.3 x Brier@24h + 0.4 x Brier@48h + 0.3 x Brier@72h
Why 48h Is Weighted Highest
24-48 hours is the strongest operational value zone
48h is emphasized because it balances actionable lead time with decision urgency.
72h is included for extended planning, but it can be less operationally immediate than earlier horizons.
Timeline
January 28, 2026 - Start Date.
April 24, 2026 - Entry Deadline. You must accept the competition rules before this date in order to compete.
April 24, 2026 - Team Merger Deadline. This is the last day participants may join or merge teams.
May 1, 2026 - Final Submission Deadline.
All deadlines are at 11:59 PM UTC on the corresponding day unless otherwise noted. The competition organizers reserve the right to update the contest timeline if they deem it necessary.