from tensorflow.estimator import LinearClassifier
from tensorflow.train import FtrlOptimizer
from dataset import criteo_partition_fn, criteo_features
import json, datetime

# how do we establish a model baseline
# we want to separate update lag as cleanly as possible.

EXPERIMENT_LOG_FILE = "data/experiment.log"

def log_eval(experiment_id,
             interval_secs,
             partition,
             model_hyperparams,
             data_hyperparams,
             metrics):
    """
    Write intermediate result to file
    :param experiment_id: 
    :param interval_secs: 
    :param partition: 
    :param model_hyperparams: 
    :param data_hyperparams:
    :param metrics: 
    :return: 
    """
    with open(EXPERIMENT_LOG_FILE, "a") as fh:
        fh.write(json.dumps({
          "experiment_id": experiment_id,
          "interval_seconds": interval_secs,
          "partition": partition,
          "hyperparameters": {
              "model": model_hyperparams,
              "data": data_hyperparams
          },
          "metrics": dict((k, float(v)) for k, v in metrics.items())
        }) + "\n")

def run_experiment(
        experiment_id,
        interval_secs,
        model_hyperparams={},
        data_hyperparams=dict(shuffle=False),
        data_fname="data/data.txt",
):
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
    
    :param experiment_id: 
    :param interval_secs: 
    :param model_hyperparams: 
    :param model_dir: 
    :param data_hyperparams: 
    :param data_fname: 
    :return: 
    """
    model = LinearClassifier(
        model_dir=("data/models/%s-%s/" % (experiment_id, str(datetime.datetime.now()))),
        feature_columns=criteo_features,
        optimizer=FtrlOptimizer(**model_hyperparams)
    )

    cur_partition = 0
    for input_fn in criteo_partition_fn(data_fname, interval_secs=interval_secs):
        log_eval(
            experiment_id,
            interval_secs,
            cur_partition,
            model_hyperparams,
            data_hyperparams,
            model.evaluate(input_fn(dict(shuffle=False)))
        )

        model.train(input_fn(data_hyperparams))
        cur_partition+=1
