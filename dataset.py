import math, csv
from tensorflow.feature_column import categorical_column_with_hash_bucket, \
    categorical_column_with_identity, crossed_column

from tensorflow.estimator.inputs import pandas_input_fn
import pandas as pd

CRITEO_MAX_SECONDS = 5270499

"""
We should FCs editable as an experiment parameter. But,
basically we have [c1...cn, i1...in, c1c2...cn-1cn, c1i1...cnin];
where c1, cnin hash size ~ 1e6 and i1 max value 10000.
 
I haven't examined the integer columns to determine if some are numeric. 
Also, do not know the max value to use. It'd be easy to compute.
"""
categorical_names = ['c1','c2','c3','c4','c5','c6','c7','c8','c9']
integer_names = ['i1','i2','i3','i4','i5','i6','i7','i8']

criteo_features = list(map(
    lambda n: categorical_column_with_hash_bucket(
        n, hash_bucket_size=1e6
    ), categorical_names))

criteo_features += list(map(
    lambda n: categorical_column_with_identity(
        n, num_buckets=10000, default_value=0
    ), integer_names
))

def cross_all_columns():
    all = categorical_names + integer_names
    fcs = []
    fck = {}
    # probably way cleaner way to do this
    # set key indicating pairs have been crossed
    # if not crossed, append to fcs, and set true
    for n1 in all:
        for n2 in all:
            k1 = "%s%s" % (n1, n2)
            k2 = "%s%s" % (n2, n1)
            if fck.get(k1) is None and fck.get(k2) is None:
                fcs.append(crossed_column([n1, n2], 1e6))
                fck[k1] = True
                fck[k2] = True

    return fcs


criteo_features += cross_all_columns()


def criteo_partition_fn(filename, interval_secs):
    """
    Criteo Columns:
    Click Time Conversion Time 8 Integers, 9 Categoricals
    :return: Dataset duration / lag_seconds input partition fns
    """
    index = 0
    Xint = []
    Xcat = []
    y = []

    with open(filename) as fh:
        tsv = csv.reader(fh, delimiter="\t")
        line_number = 0
        for row in tsv:
            current_partition = int(math.floor(int(row[0]) / interval_secs))
            if index < current_partition:
                dfi = pd.DataFrame.from_records(Xint, columns=integer_names)
                ### if interperted numerically
                ### dfi = dfi.fillna(dfi.mean())
                ## shift everything by 2, N/A=1
                dfi = dfi.fillna(int(-1))
                dfi += 2
                dfi = dfi.astype(int)
                dfc = pd.DataFrame.from_records(Xcat, columns=categorical_names)
                dfy = pd.Series(y)
                Xint = []
                Xcat = []
                y = []
                yield lambda options: pandas_input_fn(
                    pd.concat(objs=[dfi,dfc], axis=1),
                    dfy,
                    **options
                )

                #print("index: %s, current_partition: %s, line: %s, rowts: %s, rowts2: %s" % (index, current_partition, line_number, row[0], row[1]))

            Xint.append(list(map(lambda x: None if x == '' else int(x), row[2:10])))
            Xcat.append(row[10:19])
            y.append(row[1] != '')
            index = current_partition
            line_number += 1


if __name__ == "__main__":
    i = 0
    interval_secs = 500000
    max_sb = int(math.ceil(CRITEO_MAX_SECONDS / interval_secs))
    for fun in criteo_partition_fn("data/data.txt", interval_secs):
        print("i: %s, interval: %s, max_should_be: %s" % (i, interval_secs, max_sb))
        i += 1
