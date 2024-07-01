import logging

import pytest
from sklearn import datasets
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import GridSearchCV
from sklearn.multiclass import (
    OneVsOneClassifier,
    OneVsRestClassifier,
    OutputCodeClassifier,
)
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

from blocks.pipeline import BlockPipeline, make_block_pipeline

IRIS = datasets.load_iris()


class Adder(TransformerMixin, BaseEstimator):
    def __init__(self, value):
        self._value = value

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X + self._value

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)

    def __repr__(self):
        return f"Adder(value={self._value})"


def custom_log_callback(output, execution_time, **kwargs):
    """My custom `log_callback` function

    Parameters
    ----------
    output : tuple(
            numpy.ndarray or pandas.DataFrame
            :class:estimator or :class:transformer
        )
        The output of the step and a step in the pipeline.
    execution_time : float
        The execution time of the step.
    """
    logger = logging.getLogger(__name__)
    step_result, step = output
    logger.info(f"[{step}] shape={step_result.shape} " f"nbytes={step_result.nbytes} time={execution_time}")


@pytest.fixture
def named_steps():
    return [
        ("add_1", Adder(value=1)),
        ("add_10", Adder(value=10)),
        ("add_100", Adder(value=100)),
        ("add_1000", Adder(value=1000)),
    ]


@pytest.fixture
def nameless_steps():
    return (Adder(value=1), Adder(value=10), Adder(value=100), Adder(value=1000))


@pytest.fixture
def repeated_steps():
    return (StandardScaler(), StandardScaler())


@pytest.mark.filterwarnings("ignore: The default of the `iid`")  # 0.22
@pytest.mark.filterwarnings("ignore: You should specify a value")  # 0.22
@pytest.mark.parametrize("cls", [OneVsRestClassifier, OneVsOneClassifier, OutputCodeClassifier])
def test_classifier_gridsearch(cls):
    pipe = BlockPipeline([("ovrc", cls(LinearSVC(random_state=0, tol=0.1)))])
    Cs = [0.1, 0.5, 0.8]
    cv = GridSearchCV(pipe, param_grid={"ovrc__estimator__C": Cs})
    cv.fit(IRIS.data, IRIS.target)
    best_C = cv.best_estimator_.get_params()["ovrc__estimator__C"]
    assert best_C in Cs


def test_no_logs_when_log_callback_is_None(caplog, named_steps):
    pipe = BlockPipeline(named_steps, log_callback=None)
    caplog.clear()
    with caplog.at_level(logging.INFO):
        pipe.fit(IRIS.data, IRIS.target)
    assert not caplog.text, f"Log should be empty: {caplog.text}"




def test_nbytes_in_logs_when_log_callback_is_custom(caplog, named_steps):
    pipe = BlockPipeline(named_steps, log_callback=custom_log_callback)
    caplog.clear()
    with caplog.at_level(logging.INFO):
        pipe.fit(IRIS.data, IRIS.target)
    assert caplog.text, f"Log should be none empty: {caplog.text}"
    assert "nbytes=" in caplog.text, f'"nbytes=" should be in: {caplog.text}'
    assert caplog.text.count("nbytes=") == (
        len(pipe.steps) - 1
    ), f'"nbytes=" should be {len(pipe.steps) - 1} times in {caplog.text}'


def test_different_name_for_repeated_step(nameless_steps):
    ss_twice_pipeline = make_block_pipeline(*nameless_steps)
    assert ss_twice_pipeline.steps[0][0] != ss_twice_pipeline.steps[1][0]
