from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier

from model.config.core import config
from model.processing import features as pp

retrasos_pipe = Pipeline(
    [
        ("Gradient Boosting Classifier",
            GradientBoostingClassifier(
                n_estimators=config.model_config.n_estimators,
                max_depth=config.model_config.max_depth,
                max_features=config.model_config.max_features,
                loss=config.model_config.loss,
                learning_rate=config.model_config.learning_rate,
                random_state=config.model_config.random_state
            ),
        ),
    ]
)
