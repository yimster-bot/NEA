import json
import pandas as pd
import numpy as np

with open('15956.json', 'r') as f:
    raw_data = json.load(f)

df = pd.json_normalize(raw_data)
df = df.sort_values('index').reset_index(drop=True)  # ensure chronological order

# StatsBomb goal center coordinates
goal_x = 120.0
goal_y = 40.0


def calculate_distance(loc):
  if isinstance(loc, list) and len(loc) >= 2:
    x, y = loc[0], loc[1]
    return np.sqrt((goal_x - x) ** 2 + (goal_y - y) ** 2)
  return np.nan


df['distance_from_goal'] = df['location'].apply(calculate_distance)
set_piece_df = df[df['play_pattern.id'] == 2]

# --- check delivery types on passes immediately preceding shots ---
shots = df[df['type.name'] == 'Shot'].copy()

# Only shots that had a delivering pass at all
shots_with_key_pass = shots[shots['shot.key_pass_id'].notna()]

# Look up each key pass by its event id
key_pass_ids = shots_with_key_pass['shot.key_pass_id']
passes_before_shots = df[df['id'].isin(key_pass_ids)]

print(passes_before_shots['pass.technique.name'].unique())
print(passes_before_shots['pass.technique.name'].isna().sum(), "passes had no technique field")

set_piece_df.to_csv('set_piece_events.csv', index=False)
