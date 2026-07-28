import json
import pandas as pd
import numpy as np

with open('15946.json', 'r') as f:
    raw_data = json.load(f)

df = pd.json_normalize(raw_data)


# StatsBomb goal center coordinates
goal_x = 120.0
goal_y = 40.0


# Helper function to extract and calculate distance safely
def calculate_distance(loc):
  # Check if the location exists and has at least [x, y] coordinates
  if isinstance(loc, list) and len(loc) >= 2:
    x, y = loc[0], loc[1]
    # Pythagorean theorem: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return np.sqrt((goal_x - x) ** 2 + (goal_y - y) ** 2)
  return np.nan


# Apply the function to create a new column
df['distance_from_goal'] = df['location'].apply(calculate_distance)
set_piece_df = df[df['play_pattern.id'] == 2]
set_piece_df.to_csv('set_piece_events.csv', index=False)
# Example: Check the distance for the goals you filtered earlier
