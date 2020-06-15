# test_api.py
import pytest
import requests
import hashlib
import sys
from hypothesis import given, Phase, example, settings
import hypothesis.strategies as st
from pbrtesting import methods
from decouple import config
from pytest_regressions import data_regression
import schemathesis

TEST_SAMPLES = config("TEST_SAMPLES", cast=int, default=100)

SETTINGS_PARAMETERS = {
    "max_examples": TEST_SAMPLES,
    "derandomize": True,
    "phases": [Phase.explicit, Phase.generate, Phase.reuse],
    "print_blob": True,
}

EXPLICIT_SETTING_PARAMETERS = {"phases": [Phase.explicit]}

PORT = config("PORT")


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


schema = schemathesis.from_uri(f"http://127.0.0.1:{PORT}/openapi.json")


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@schema.parametrize()
def test_no_server_errors_one(case):
    # `requests` will make an appropriate call under the hood
    response = case.call()  # use `call_wsgi` if you used `schemathesis.from_wsgi`
    # You could use built-in checks
    case.validate_response(response)
    # Or assert the response manually
    assert response.status_code < 500


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@schema.parametrize()
def test_no_server_errors_two(case):
    kwargs = case.as_requests_kwargs()
    response = requests.request(**kwargs)
    assert response.status_code < 500


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@schema.parametrize(method="GET", endpoint="/echo")
def test_no_server_errors_echo(case):
    kwargs = case.as_requests_kwargs()
    response = requests.request(**kwargs)
    assert response.status_code < 500


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@schema.parametrize(method="GET", endpoint="/item")
def test_no_server_errors_item(case):
    kwargs = case.as_requests_kwargs()
    response = requests.request(**kwargs)
    assert response.status_code < 500


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@settings(**SETTINGS_PARAMETERS)
@schema.parametrize(method="post", endpoint="/item")
def test_no_server_errors_item(data_regression, case):
    kwargs = case.as_requests_kwargs()
    response = requests.request(**kwargs)
    assert response.status_code == 200

    results = response.content

    function_name = sys._getframe(2).f_code.co_name

    regresion_path = get_regression_path(kwargs, path=function_name)
    results_hash = get_hash_results(results)

    data_regression.check(results_hash, regresion_path)


root_endpoint = schema["/"]["GET"].as_strategy()
echo_endpoint = schema["/echo/{name}"]["GET"].as_strategy()
item_get_endpoint = schema["/item/{item_name}"]["GET"].as_strategy()
item_post_endpoint = schema["/item/{item_name}"]["POST"].as_strategy()


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@given(case=root_endpoint)
def test_root(case):
    response = case.call()
    assert response.status_code < 500


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@settings(**SETTINGS_PARAMETERS)
@given(case=echo_endpoint)
def test_echo(data_regression, case):
    kwargs = case.as_requests_kwargs()
    response = requests.request(**kwargs)
    assert response.status_code == 200
    results = response.content

    function_name = sys._getframe(2).f_code.co_name

    regresion_path = get_regression_path(kwargs, path=function_name)
    results_hash = get_hash_results(results)

    data_regression.check(results_hash, regresion_path)


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@settings(**SETTINGS_PARAMETERS)
@given(case=item_get_endpoint)
def test_get_item(data_regression, case):
    kwargs = case.as_requests_kwargs()
    response = requests.request(**kwargs)
    assert response.status_code == 200
    results = response.json()
    results.pop("price")

    function_name = sys._getframe(2).f_code.co_name

    regresion_path = get_regression_path(kwargs, path=function_name)
    results_hash = get_hash_results(results)

    data_regression.check(results_hash, regresion_path)


@pytest.mark.flaky(reruns=TEST_SAMPLES)
@given(case=item_get_endpoint)
def test_post_item(case):
    response = case.call()
    assert response.status_code < 500
