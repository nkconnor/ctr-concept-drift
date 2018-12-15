from pandas.io.json import json_normalize
import pandas as pd
import json

def read_experiment_df(log_name):
    with open(log_name) as fh:
        records = list(map(json.loads, fh))

    df = pd.DataFrame.from_dict(json_normalize(records))
    df['time'] = df['interval_seconds'] * df['partition']  # for comparison
    return df
