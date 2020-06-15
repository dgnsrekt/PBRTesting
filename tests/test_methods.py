# test_methods
import pytest
import hashlib
import sys
from hypothesis import given, Phase, example, settings
import hypothesis.strategies as st
from pbrtesting import methods
from decouple import config
from pytest_regressions import data_regression

TEST_SAMPLES = config("TEST_SAMPLES", cast=int, default=100)

SETTINGS_PARAMETERS = {
    "max_examples": TEST_SAMPLES,
    "derandomize": True,
    "phases": [Phase.explicit, Phase.generate, Phase.reuse],
    "print_blob": True,
}


def hash_function(input):
    input = str(input)
    m = hashlib.sha1()
    m.update(input.encode())
    return m.hexdigest()


def get_regression_path(*args, path):
    arg_hash = hash_function(str(args))
    return f"{path}/{arg_hash}"


def get_hash_results(results):
    return hash_function(results)


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@settings(**SETTINGS_PARAMETERS)
@given(st.integers(), st.integers())
@example(x=555, y=666)
@example(x=777, y=888)
def test_ints_are_commutative(data_regression, x, y):
    results = methods.ints_are_commutative(x, y)
    assert results == True

    function_name = sys._getframe(2).f_code.co_name

    regresion_path = get_regression_path(x, y, path=function_name)
    results_hash = get_hash_results(results)

    data_regression.check(results_hash, regresion_path)


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@settings(**SETTINGS_PARAMETERS)
@given(x=st.integers(), y=st.integers())
def test_ints_cancel(data_regression, x, y):
    results = methods.ints_cancel(x, y)
    assert results == True

    function_name = sys._getframe(2).f_code.co_name

    regresion_path = get_regression_path(x, y, path=function_name)
    results_hash = get_hash_results(results)

    data_regression.check(results_hash, regresion_path)


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@settings(**SETTINGS_PARAMETERS)
@given(st.lists(st.integers()))
def test_reversing_twice_gives_same_list(data_regression, xs):
    results = methods.reversing_twice_gives_same_list(xs)
    assert results == True

    function_name = sys._getframe(2).f_code.co_name

    regresion_path = get_regression_path(xs, path=function_name)
    results_hash = get_hash_results(results)

    data_regression.check(results_hash, regresion_path)


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@settings(**SETTINGS_PARAMETERS)
@given(st.tuples(st.booleans(), st.text()))
def test_look_tuples_work_too(data_regression, t):
    results = methods.generated_tuples_work(t)
    assert results == True

    function_name = sys._getframe(2).f_code.co_name

    regresion_path = get_regression_path(t, path=function_name)
    results_hash = get_hash_results(results)

    data_regression.check(results_hash, regresion_path)
