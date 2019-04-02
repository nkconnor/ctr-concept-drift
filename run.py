import fire
from train import run_experiment
import json

class Run(object):
    """Simple CLI interface"""

    def experiment(self,
                   experiment_id,
                   interval_secs,
                   model_params,
                   data_params):
        """
        Example usage:
        
        python3.4 run.py experiment \
            --experiment-id=60_mins_reduce_hash \
            --interval-secs=3600 \
            --model-params='{"learning_rate":0.05, "l1_regularization_strength":0.00, "l2_regularization_strength":0.5}' \
            --data-params='{"shuffle":True, "num_epochs":1, "num_threads":2, batch_size:256}'
            
        :param experiment_id: 
        :param interval_secs: 
        :param model_params: 
        :param data_params: 
        :return: 
        """
        run_experiment(
            experiment_id=experiment_id,
            interval_secs=interval_secs,
            model_hyperparams=model_params,
            data_hyperparams=data_params)

if __name__ == '__main__':
    fire.Fire(Run)
