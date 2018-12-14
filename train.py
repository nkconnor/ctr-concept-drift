import tensorflow as tf
from tensorflow.python.estimator.canned.linear import LinearRegressor
from tensorflow.train import FtrlOptimizer
from dataset import criteo_partition_fn

# how do we establish a model baseline
# we want to separate update lag as cleanly as possible.

features = [
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

def run_experiment(experiment_id, interval_secs):
    """
     we can partition the data by lag_seconds
     e.g. lag_seconds = 60 * 60 * 24 = 1 day
     [ day n ] [ day n+1 ] [ day n+2 ] .. n-->i
     then iteratively train/evaluate
     for i in n:
        train (day n)
          evaluate (day n+1) 
        train day (n+1)
          evaluate day(n+2)
          
    we will observe cumulative AUC, log loss, accuracy, ..      
    
    :param interval_seconds: 
    :return: 
    """

    model = LinearRegressor(
        model_dir="data/models/%s/" % (experiment_id),
        feature_columns=features,
        optimizer=FtrlOptimizer(learning_rate=0.1,
                                l1_regularization_strength=0.5,
                                l2_regularization_strength=0.5,
                                )
    )

    data_fn = criteo_partition_fn("data/data.txt", interval_secs=interval_secs)

    base_train = next(data_fn)
    model.train(base_train)

    i = 0
    for data in data_fn:
        if i > 10:
            break

        model.evaluate(data)
        model.train(data)
        i += 1


run_experiment(
    "600_seconds",
    60 * 5 * 2
) # 5mins