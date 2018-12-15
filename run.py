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
            --experiment-id=30_mins \
            --interval-secs=1800 \
            --model-params='{"learning_rate":0.1, "l1_regularization_strength":0.5, "l2_regularization_strength":0.5}' \
            --data-params='{"shuffle":False, "num_epochs":1}'
            
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

       ##      model_hyperparams=dict(
       ##          learning_rate=0.1,
       ##          l1_regularization_strength=0.5,
       ##          l2_regularization_strength=0.5
       ##      ),
       ##      data_hyperparams=dict(
       ##          shuffle=False,
       ##          epochs=2
       ##      )
       ##  )

if __name__ == '__main__':
    fire.Fire(Run)