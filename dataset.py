import math, csv
import tensorflow as tf
from tensorflow.estimator.inputs import pandas_input_fn
import pandas as pd

CRITEO_MAX_SECONDS = 5270499


criteo_features = [
      tf.feature_column.categorical_column_with_identity('i1', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_identity('i2', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_identity('i3', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_identity('i4', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_identity('i5', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_identity('i6', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_identity('i7', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_identity('i8', num_buckets=10000, default_value=0)
    , tf.feature_column.categorical_column_with_hash_bucket('c1', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c2', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c3', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c4', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c5', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c6', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c7', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c8', hash_bucket_size=1e6)
    , tf.feature_column.categorical_column_with_hash_bucket('c9', hash_bucket_size=1e6)
]

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
                dfi = pd.DataFrame.from_records(Xint, columns=['i1','i2','i3','i4','i5','i6','i7','i8'])
                ### if interperted numerically
                ### dfi = dfi.fillna(dfi.mean())
                ## shift everything by 2, N/A=1
                dfi = dfi.fillna(int(-1))
                dfi += 2
                dfi = dfi.astype(int)
                dfc = pd.DataFrame.from_records(Xcat, columns=['c1','c2','c3','c4','c5','c6','c7','c8','c9'])

                yield lambda options: pandas_input_fn(
                    pd.concat(objs=[dfi,dfc], axis=1),
                    pd.Series(y),
                    **options
                )
                Xint = []
                Xcat = []
                y = []
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
