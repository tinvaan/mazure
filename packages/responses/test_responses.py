# coding: utf-8

from __future__ import absolute_import, print_function, division, unicode_literals

import inspect
import re
import six
from io import BufferedReader, BytesIO

import pytest
import requests
import responses
from requests.exceptions import ConnectionError, HTTPError
from responses import BaseResponse, Response

try:
    from mock import patch, Mock
except ImportError:
    from unittest.mock import patch, Mock  # type: ignore


def assert_reset():
    assert len(responses._default_mock._matches) == 0
    assert len(responses.calls) == 0


def assert_response(resp, body=None, content_type="text/plain"):
    assert resp.status_code == 200
    assert resp.reason == "OK"
    if content_type is not None:
        assert resp.headers["Content-Type"] == content_type
    else:
        assert "Content-Type" not in resp.headers
    assert resp.text == body


def assert_params(resp, expected):
    assert hasattr(resp, "request"), "Missing request"
    assert hasattr(
        resp.request, "params"
    ), "Missing params on request that responses should add"
    assert getattr(resp.request, "params") == expected, "Incorrect parameters"


def test_response():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com", body=b"test")
        resp = requests.get("http://example.com")
        assert_response(resp, "test")
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == "http://example.com/"
        assert responses.calls[0].response.content == b"test"

        resp = requests.get("http://example.com?foo=bar")
        assert_response(resp, "test")
        assert len(responses.calls) == 2
        assert responses.calls[1].request.url == "http://example.com/?foo=bar"
        assert responses.calls[1].response.content == b"test"

    run()
    assert_reset()


def test_response_encoded():
    @responses.activate
    def run():
        # Path contains urlencoded =/()[]
        url = "http://example.org/foo.bar%3D%2F%28%29%5B%5D"
        responses.add(responses.GET, url, body="it works", status=200)
        resp = requests.get(url)
        assert_response(resp, "it works")

    run()
    assert_reset()


def test_response_with_instance():
    @responses.activate
    def run():
        responses.add(
            responses.Response(method=responses.GET, url="http://example.com")
        )
        resp = requests.get("http://example.com")
        assert_response(resp, "")
        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == "http://example.com/"

        resp = requests.get("http://example.com?foo=bar")
        assert_response(resp, "")
        assert len(responses.calls) == 2
        assert responses.calls[1].request.url == "http://example.com/?foo=bar"


@pytest.mark.parametrize(
    "original,replacement",
    [
        ("http://example.com/two", "http://example.com/two"),
        (
            Response(method=responses.GET, url="http://example.com/two"),
            Response(
                method=responses.GET, url="http://example.com/two", body="testtwo"
            ),
        ),
        (
            re.compile(r"http://example\.com/two"),
            re.compile(r"http://example\.com/two"),
        ),
    ],
)
def test_replace(original, replacement):
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com/one", body="test1")

        if isinstance(original, BaseResponse):
            responses.add(original)
        else:
            responses.add(responses.GET, original, body="test2")

        responses.add(responses.GET, "http://example.com/three", body="test3")
        responses.add(
            responses.GET, re.compile(r"http://example\.com/four"), body="test3"
        )

        if isinstance(replacement, BaseResponse):
            responses.replace(replacement)
        else:
            responses.replace(responses.GET, replacement, body="testtwo")

        resp = requests.get("http://example.com/two")
        assert_response(resp, "testtwo")

    run()
    assert_reset()


@pytest.mark.parametrize(
    "original,replacement",
    [
        ("http://example.com/one", re.compile(r"http://example\.com/one")),
        (re.compile(r"http://example\.com/one"), "http://example.com/one"),
    ],
)
def test_replace_error(original, replacement):
    @responses.activate
    def run():
        responses.add(responses.GET, original)
        with pytest.raises(ValueError) as excinfo:
            responses.replace(responses.GET, replacement)
        assert "Response is not registered for URL %s" % replacement in str(
            excinfo.value
        )

    run()
    assert_reset()


def test_replace_response_object_error():
    @responses.activate
    def run():
        responses.add(Response(method=responses.GET, url="http://example.com/one"))
        with pytest.raises(ValueError) as excinfo:
            responses.replace(
                Response(method=responses.GET, url="http://example.com/two")
            )
        assert "Response is not registered for URL http://example.com/two" in str(
            excinfo.value
        )

    run()
    assert_reset()


@pytest.mark.parametrize(
    "original,replacement",
    [
        ("http://example.com/two", "http://example.com/two"),
        (
            Response(method=responses.GET, url="http://example.com/two"),
            Response(
                method=responses.GET, url="http://example.com/two", body="testtwo"
            ),
        ),
        (
            re.compile(r"http://example\.com/two"),
            re.compile(r"http://example\.com/two"),
        ),
    ],
)
def test_upsert_replace(original, replacement):
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com/one", body="test1")

        if isinstance(original, BaseResponse):
            responses.add(original)
        else:
            responses.add(responses.GET, original, body="test2")

        if isinstance(replacement, BaseResponse):
            responses.upsert(replacement)
        else:
            responses.upsert(responses.GET, replacement, body="testtwo")

        resp = requests.get("http://example.com/two")
        assert_response(resp, "testtwo")

    run()
    assert_reset()


@pytest.mark.parametrize(
    "original,replacement",
    [
        ("http://example.com/two", "http://example.com/two"),
        (
            Response(method=responses.GET, url="http://example.com/two"),
            Response(
                method=responses.GET, url="http://example.com/two", body="testtwo"
            ),
        ),
        (
            re.compile(r"http://example\.com/two"),
            re.compile(r"http://example\.com/two"),
        ),
    ],
)
def test_upsert_add(original, replacement):
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com/one", body="test1")

        if isinstance(replacement, BaseResponse):
            responses.upsert(replacement)
        else:
            responses.upsert(responses.GET, replacement, body="testtwo")

        resp = requests.get("http://example.com/two")
        assert_response(resp, "testtwo")

    run()
    assert_reset()


def test_remove():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com/zero")
        responses.add(responses.GET, "http://example.com/one")
        responses.add(responses.GET, "http://example.com/two")
        responses.add(responses.GET, re.compile(r"http://example\.com/three"))
        responses.add(responses.GET, re.compile(r"http://example\.com/four"))
        re.purge()
        responses.remove(responses.GET, "http://example.com/two")
        responses.remove(Response(method=responses.GET, url="http://example.com/zero"))
        responses.remove(responses.GET, re.compile(r"http://example\.com/four"))

        with pytest.raises(ConnectionError):
            requests.get("http://example.com/zero")
        requests.get("http://example.com/one")
        with pytest.raises(ConnectionError):
            requests.get("http://example.com/two")
        requests.get("http://example.com/three")
        with pytest.raises(ConnectionError):
            requests.get("http://example.com/four")

    run()
    assert_reset()


@pytest.mark.parametrize(
    "args1,kwargs1,args2,kwargs2,expected",
    [
        ((responses.GET, "a"), {}, (responses.GET, "a"), {}, True),
        ((responses.GET, "a"), {}, (responses.GET, "b"), {}, False),
        ((responses.GET, "a"), {}, (responses.POST, "a"), {}, False),
        (
            (responses.GET, "a"),
            {"match_querystring": True},
            (responses.GET, "a"),
            {},
            True,
        ),
    ],
)
def test_response_equality(args1, kwargs1, args2, kwargs2, expected):
    o1 = BaseResponse(*args1, **kwargs1)
    o2 = BaseResponse(*args2, **kwargs2)
    assert (o1 == o2) is expected
    assert (o1 != o2) is not expected


def test_response_equality_different_objects():
    o1 = BaseResponse(method=responses.GET, url="a")
    o2 = "str"
    assert (o1 == o2) is False
    assert (o1 != o2) is True


def test_connection_error():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com")

        with pytest.raises(ConnectionError):
            requests.get("http://example.com/foo")

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == "http://example.com/foo"
        assert type(responses.calls[0].response) is ConnectionError
        assert responses.calls[0].response.request

    run()
    assert_reset()


def test_match_querystring():
    @responses.activate
    def run():
        url = "http://example.com?test=1&foo=bar"
        responses.add(responses.GET, url, match_querystring=True, body=b"test")
        resp = requests.get("http://example.com?test=1&foo=bar")
        assert_response(resp, "test")
        resp = requests.get("http://example.com?foo=bar&test=1")
        assert_response(resp, "test")
        resp = requests.get("http://example.com/?foo=bar&test=1")
        assert_response(resp, "test")

    run()
    assert_reset()


def test_match_empty_querystring():
    @responses.activate
    def run():
        responses.add(
            responses.GET, "http://example.com", body=b"test", match_querystring=True
        )
        resp = requests.get("http://example.com")
        assert_response(resp, "test")
        resp = requests.get("http://example.com/")
        assert_response(resp, "test")
        with pytest.raises(ConnectionError):
            requests.get("http://example.com?query=foo")

    run()
    assert_reset()


def test_match_querystring_error():
    @responses.activate
    def run():
        responses.add(
            responses.GET, "http://example.com/?test=1", match_querystring=True
        )

        with pytest.raises(ConnectionError):
            requests.get("http://example.com/foo/?test=2")

    run()
    assert_reset()


def test_match_querystring_regex():
    @responses.activate
    def run():
        """Note that `match_querystring` value shouldn't matter when passing a
        regular expression"""

        responses.add(
            responses.GET,
            re.compile(r"http://example\.com/foo/\?test=1"),
            body="test1",
            match_querystring=True,
        )

        resp = requests.get("http://example.com/foo/?test=1")
        assert_response(resp, "test1")

        responses.add(
            responses.GET,
            re.compile(r"http://example\.com/foo/\?test=2"),
            body="test2",
            match_querystring=False,
        )

        resp = requests.get("http://example.com/foo/?test=2")
        assert_response(resp, "test2")

    run()
    assert_reset()


def test_match_querystring_error_regex():
    @responses.activate
    def run():
        """Note that `match_querystring` value shouldn't matter when passing a
        regular expression"""

        responses.add(
            responses.GET,
            re.compile(r"http://example\.com/foo/\?test=1"),
            match_querystring=True,
        )

        with pytest.raises(ConnectionError):
            requests.get("http://example.com/foo/?test=3")

        responses.add(
            responses.GET,
            re.compile(r"http://example\.com/foo/\?test=2"),
            match_querystring=False,
        )

        with pytest.raises(ConnectionError):
            requests.get("http://example.com/foo/?test=4")

    run()
    assert_reset()


def test_match_querystring_auto_activates():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com?test=1", body=b"test")
        resp = requests.get("http://example.com?test=1")
        assert_response(resp, "test")
        with pytest.raises(ConnectionError):
            requests.get("http://example.com/?test=2")

    run()
    assert_reset()


def test_match_querystring_missing_key():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com?foo=1&bar=2", body=b"test")
        with pytest.raises(ConnectionError):
            requests.get("http://example.com/?foo=1&baz=2")

        with pytest.raises(ConnectionError):
            requests.get("http://example.com/?bar=2&fez=1")

    run()
    assert_reset()


def test_accept_string_body():
    @responses.activate
    def run():
        url = "http://example.com/"
        responses.add(responses.GET, url, body="test")
        resp = requests.get(url)
        assert_response(resp, "test")

    run()
    assert_reset()


def test_accept_json_body():
    @responses.activate
    def run():
        content_type = "application/json"

        url = "http://example.com/"
        responses.add(responses.GET, url, json={"message": "success"})
        resp = requests.get(url)
        assert_response(resp, '{"message": "success"}', content_type)

        url = "http://example.com/1/"
        responses.add(responses.GET, url, json=[])
        resp = requests.get(url)
        assert_response(resp, "[]", content_type)

    run()
    assert_reset()


def test_no_content_type():
    @responses.activate
    def run():
        url = "http://example.com/"
        responses.add(responses.GET, url, body="test", content_type=None)
        resp = requests.get(url)
        assert_response(resp, "test", content_type=None)

    run()
    assert_reset()


def test_arbitrary_status_code():
    @responses.activate
    def run():
        url = "http://example.com/"
        responses.add(responses.GET, url, body="test", status=419)
        resp = requests.get(url)
        assert resp.status_code == 419
        assert resp.reason is None

    run()
    assert_reset()


def test_throw_connection_error_explicit():
    @responses.activate
    def run():
        url = "http://example.com"
        exception = HTTPError("HTTP Error")
        responses.add(responses.GET, url, exception)

        with pytest.raises(HTTPError) as HE:
            requests.get(url)

        assert str(HE.value) == "HTTP Error"

    run()
    assert_reset()


def test_callback():
    body = b"test callback"
    status = 400
    reason = "Bad Request"
    headers = {
        "foo": "bar",
        "Content-Type": "application/json",
        "Content-Length": "13",
    }
    url = "http://example.com/"

    def request_callback(request):
        return (status, headers, body)

    @responses.activate
    def run():
        responses.add_callback(responses.GET, url, request_callback)
        resp = requests.get(url)
        assert resp.text == "test callback"
        assert resp.status_code == status
        assert resp.reason == reason
        assert "bar" == resp.headers.get("foo")
        assert "application/json" == resp.headers.get("Content-Type")
        assert "13" == resp.headers.get("Content-Length")

    run()
    assert_reset()


def test_callback_exception_result():
    result = Exception()
    url = "http://example.com/"

    def request_callback(request):
        return result

    @responses.activate
    def run():
        responses.add_callback(responses.GET, url, request_callback)

        with pytest.raises(Exception) as e:
            requests.get(url)

        assert e.value is result

    run()
    assert_reset()


def test_callback_exception_body():
    body = Exception()
    url = "http://example.com/"

    def request_callback(request):
        return (200, {}, body)

    @responses.activate
    def run():
        responses.add_callback(responses.GET, url, request_callback)

        with pytest.raises(Exception) as e:
            requests.get(url)

        assert e.value is body

    run()
    assert_reset()


def test_callback_no_content_type():
    body = b"test callback"
    status = 400
    reason = "Bad Request"
    headers = {"foo": "bar"}
    url = "http://example.com/"

    def request_callback(request):
        return (status, headers, body)

    @responses.activate
    def run():
        responses.add_callback(responses.GET, url, request_callback, content_type=None)
        resp = requests.get(url)
        assert resp.text == "test callback"
        assert resp.status_code == status
        assert resp.reason == reason
        assert "foo" in resp.headers
        assert "Content-Type" not in resp.headers

    run()
    assert_reset()


def test_callback_content_type_dict():
    def request_callback(request):
        return (
            200,
            {"Content-Type": "application/json"},
            b"foo",
        )

    @responses.activate
    def run():
        responses.add_callback("GET", "http://mockhost/.foo", callback=request_callback)
        resp = requests.get("http://mockhost/.foo")
        assert resp.text == "foo"
        assert resp.headers["content-type"] == "application/json"

    run()
    assert_reset()


def test_callback_content_type_tuple():
    def request_callback(request):
        return (
            200,
            [("Content-Type", "application/json")],
            b"foo",
        )

    @responses.activate
    def run():
        responses.add_callback("GET", "http://mockhost/.foo", callback=request_callback)
        resp = requests.get("http://mockhost/.foo")
        assert resp.text == "foo"
        assert resp.headers["content-type"] == "application/json"

    run()
    assert_reset()


def test_regular_expression_url():
    @responses.activate
    def run():
        url = re.compile(r"https?://(.*\.)?example.com")
        responses.add(responses.GET, url, body=b"test")

        resp = requests.get("http://example.com")
        assert_response(resp, "test")

        resp = requests.get("https://example.com")
        assert_response(resp, "test")

        resp = requests.get("https://uk.example.com")
        assert_response(resp, "test")

        with pytest.raises(ConnectionError):
            requests.get("https://uk.exaaample.com")

    run()
    assert_reset()


def test_custom_adapter():
    @responses.activate
    def run():
        url = "http://example.com"
        responses.add(responses.GET, url, body=b"test")

        calls = [0]

        class DummyAdapter(requests.adapters.HTTPAdapter):
            def send(self, *a, **k):
                calls[0] += 1
                return super(DummyAdapter, self).send(*a, **k)

        # Test that the adapter is actually used
        session = requests.Session()
        session.mount("http://", DummyAdapter())

        resp = session.get(url, allow_redirects=False)
        assert calls[0] == 1

        # Test that the response is still correctly emulated
        session = requests.Session()
        session.mount("http://", DummyAdapter())

        resp = session.get(url)
        assert_response(resp, "test")

    run()


def test_responses_as_context_manager():
    def run():
        with responses.mock:
            responses.add(responses.GET, "http://example.com", body=b"test")
            resp = requests.get("http://example.com")
            assert_response(resp, "test")
            assert len(responses.calls) == 1
            assert responses.calls[0].request.url == "http://example.com/"
            assert responses.calls[0].response.content == b"test"

            resp = requests.get("http://example.com?foo=bar")
            assert_response(resp, "test")
            assert len(responses.calls) == 2
            assert responses.calls[1].request.url == "http://example.com/?foo=bar"
            assert responses.calls[1].response.content == b"test"

    run()
    assert_reset()


def test_activate_doesnt_change_signature():
    def test_function(a, b=None):
        return (a, b)

    decorated_test_function = responses.activate(test_function)
    if hasattr(inspect, "signature"):
        assert inspect.signature(test_function) == inspect.signature(
            decorated_test_function
        )
    else:
        assert inspect.getargspec(test_function) == inspect.getargspec(
            decorated_test_function
        )
    assert decorated_test_function(1, 2) == test_function(1, 2)
    assert decorated_test_function(3) == test_function(3)


def test_activate_mock_interaction():
    @patch("sys.stdout")
    def test_function(mock_stdout):
        return mock_stdout

    decorated_test_function = responses.activate(test_function)
    if hasattr(inspect, "signature"):
        assert inspect.signature(test_function) == inspect.signature(
            decorated_test_function
        )
    else:
        assert inspect.getargspec(test_function) == inspect.getargspec(
            decorated_test_function
        )

    value = test_function()
    assert isinstance(value, Mock)

    value = decorated_test_function()
    assert isinstance(value, Mock)


@pytest.mark.skipif(six.PY2, reason="Cannot run in python2")
def test_activate_doesnt_change_signature_with_return_type():
    def test_function(a, b=None):
        return (a, b)

    # Add type annotations as they are syntax errors in py2.
    # Use a class to test for import errors in evaled code.
    test_function.__annotations__["return"] = Mock
    test_function.__annotations__["a"] = Mock

    decorated_test_function = responses.activate(test_function)
    if hasattr(inspect, "signature"):
        assert inspect.signature(test_function) == inspect.signature(
            decorated_test_function
        )
    else:
        assert inspect.getargspec(test_function) == inspect.getargspec(
            decorated_test_function
        )
    assert decorated_test_function(1, 2) == test_function(1, 2)
    assert decorated_test_function(3) == test_function(3)


def test_activate_doesnt_change_signature_for_method():
    class TestCase(object):
        def test_function(self, a, b=None):
            return (self, a, b)

        decorated_test_function = responses.activate(test_function)

    test_case = TestCase()
    assert test_case.decorated_test_function(1, 2) == test_case.test_function(1, 2)
    assert test_case.decorated_test_function(3) == test_case.test_function(3)


def test_response_cookies():
    body = b"test callback"
    status = 200
    headers = {"set-cookie": "session_id=12345; a=b; c=d"}
    url = "http://example.com/"

    def request_callback(request):
        return (status, headers, body)

    @responses.activate
    def run():
        responses.add_callback(responses.GET, url, request_callback)
        resp = requests.get(url)
        assert resp.text == "test callback"
        assert resp.status_code == status
        assert "session_id" in resp.cookies
        assert resp.cookies["session_id"] == "12345"
        assert set(resp.cookies.keys()) == set(["session_id"])

    run()
    assert_reset()


def test_response_secure_cookies():
    body = b"test callback"
    status = 200
    headers = {"set-cookie": "session_id=12345; a=b; c=d; secure"}
    url = "http://example.com/"

    def request_callback(request):
        return (status, headers, body)

    @responses.activate
    def run():
        responses.add_callback(responses.GET, url, request_callback)
        resp = requests.get(url)
        assert resp.text == "test callback"
        assert resp.status_code == status
        assert "session_id" in resp.cookies
        assert resp.cookies["session_id"] == "12345"
        assert set(resp.cookies.keys()) == set(["session_id"])

    run()
    assert_reset()


def test_response_cookies_multiple():
    body = b"test callback"
    status = 200
    headers = [
        ("set-cookie", "1P_JAR=2019-12-31-23; path=/; domain=.example.com; HttpOnly"),
        ("set-cookie", "NID=some=value; path=/; domain=.example.com; secure"),
    ]
    url = "http://example.com/"

    def request_callback(request):
        return (status, headers, body)

    @responses.activate
    def run():
        responses.add_callback(responses.GET, url, request_callback)
        resp = requests.get(url)
        assert resp.text == "test callback"
        assert resp.status_code == status
        assert set(resp.cookies.keys()) == set(["1P_JAR", "NID"])
        assert resp.cookies["1P_JAR"] == "2019-12-31-23"
        assert resp.cookies["NID"] == "some=value"

    run()
    assert_reset()


def test_response_callback():
    """adds a callback to decorate the response, then checks it"""

    def run():
        def response_callback(resp):
            resp._is_mocked = True
            return resp

        with responses.RequestsMock(response_callback=response_callback) as m:
            m.add(responses.GET, "http://example.com", body=b"test")
            resp = requests.get("http://example.com")
            assert resp.text == "test"
            assert hasattr(resp, "_is_mocked")
            assert getattr(resp, "_is_mocked") is True

    run()
    assert_reset()


def test_response_filebody():
    """ Adds the possibility to use actual (binary) files as responses """

    def run():
        with responses.RequestsMock() as m:
            with open("README.rst", "r") as out:
                m.add(responses.GET, "http://example.com", body=out.read(), stream=True)
                resp = requests.get("http://example.com")
            with open("README.rst", "r") as out:
                assert resp.text == out.read()


def test_assert_all_requests_are_fired():
    def request_callback(request):
        raise BaseException()

    def run():
        with pytest.raises(AssertionError) as excinfo:
            with responses.RequestsMock(assert_all_requests_are_fired=True) as m:
                m.add(responses.GET, "http://example.com", body=b"test")
        assert "http://example.com" in str(excinfo.value)
        assert responses.GET in str(excinfo.value)

        # check that assert_all_requests_are_fired default to True
        with pytest.raises(AssertionError):
            with responses.RequestsMock() as m:
                m.add(responses.GET, "http://example.com", body=b"test")

        # check that assert_all_requests_are_fired doesn't swallow exceptions
        with pytest.raises(ValueError):
            with responses.RequestsMock() as m:
                m.add(responses.GET, "http://example.com", body=b"test")
                raise ValueError()

        # check that assert_all_requests_are_fired=True doesn't remove urls
        with responses.RequestsMock(assert_all_requests_are_fired=True) as m:
            m.add(responses.GET, "http://example.com", body=b"test")
            assert len(m._matches) == 1
            requests.get("http://example.com")
            assert len(m._matches) == 1

        # check that assert_all_requests_are_fired=True counts mocked errors
        with responses.RequestsMock(assert_all_requests_are_fired=True) as m:
            m.add(responses.GET, "http://example.com", body=Exception())
            assert len(m._matches) == 1
            with pytest.raises(Exception):
                requests.get("http://example.com")
            assert len(m._matches) == 1

        with responses.RequestsMock(assert_all_requests_are_fired=True) as m:
            m.add_callback(responses.GET, "http://example.com", request_callback)
            assert len(m._matches) == 1
            with pytest.raises(BaseException):
                requests.get("http://example.com")
            assert len(m._matches) == 1

    run()
    assert_reset()


def test_allow_redirects_samehost():
    redirecting_url = "http://example.com"
    final_url_path = "/1"
    final_url = "{0}{1}".format(redirecting_url, final_url_path)
    url_re = re.compile(r"^http://example.com(/)?(\d+)?$")

    def request_callback(request):
        # endpoint of chained redirect
        if request.url.endswith(final_url_path):
            return 200, (), b"test"

        # otherwise redirect to an integer path
        else:
            if request.url.endswith("/0"):
                n = 1
            else:
                n = 0
            redirect_headers = {"location": "/{0!s}".format(n)}
            return 301, redirect_headers, None

    def run():
        # setup redirect
        with responses.mock:
            responses.add_callback(responses.GET, url_re, request_callback)
            resp_no_redirects = requests.get(redirecting_url, allow_redirects=False)
            assert resp_no_redirects.status_code == 301
            assert len(responses.calls) == 1  # 1x300
            assert responses.calls[0][1].status_code == 301
        assert_reset()

        with responses.mock:
            responses.add_callback(responses.GET, url_re, request_callback)
            resp_yes_redirects = requests.get(redirecting_url, allow_redirects=True)
            assert len(responses.calls) == 3  # 2x300 + 1x200
            assert len(resp_yes_redirects.history) == 2
            assert resp_yes_redirects.status_code == 200
            assert final_url == resp_yes_redirects.url
            status_codes = [call[1].status_code for call in responses.calls]
            assert status_codes == [301, 301, 200]
        assert_reset()

    run()
    assert_reset()


def test_handles_unicode_querystring():
    url = "http://example.com/test?type=2&ie=utf8&query=汉字"

    @responses.activate
    def run():
        responses.add(responses.GET, url, body="test", match_querystring=True)

        resp = requests.get(url)

        assert_response(resp, "test")

    run()
    assert_reset()


def test_handles_unicode_url():
    url = "http://www.संजाल.भारत/hi/वेबसाइट-डिजाइन"

    @responses.activate
    def run():
        responses.add(responses.GET, url, body="test")

        resp = requests.get(url)

        assert_response(resp, "test")

    run()
    assert_reset()


def test_handles_unicode_body():
    url = "http://example.com/test"

    @responses.activate
    def run():
        responses.add(responses.GET, url, body="михољско лето")

        resp = requests.get(url)

        assert_response(resp, "михољско лето", content_type="text/plain; charset=utf-8")

    run()
    assert_reset()


def test_handles_buffered_reader_body():
    url = "http://example.com/test"

    @responses.activate
    def run():
        responses.add(responses.GET, url, body=BufferedReader(BytesIO(b"test")))  # type: ignore

        resp = requests.get(url)

        assert_response(resp, "test")

    run()
    assert_reset()


def test_headers():
    @responses.activate
    def run():
        responses.add(
            responses.GET, "http://example.com", body="", headers={"X-Test": "foo"}
        )
        resp = requests.get("http://example.com")
        assert resp.headers["X-Test"] == "foo"

    run()
    assert_reset()


def test_legacy_adding_headers():
    @responses.activate
    def run():
        responses.add(
            responses.GET,
            "http://example.com",
            body="",
            adding_headers={"X-Test": "foo"},
        )
        resp = requests.get("http://example.com")
        assert resp.headers["X-Test"] == "foo"

    run()
    assert_reset()


def test_multiple_responses():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com", body="test")
        responses.add(responses.GET, "http://example.com", body="rest")

        resp = requests.get("http://example.com")
        assert_response(resp, "test")
        resp = requests.get("http://example.com")
        assert_response(resp, "rest")
        # After all responses are used, last response should be repeated
        resp = requests.get("http://example.com")
        assert_response(resp, "rest")

    run()
    assert_reset()


def test_multiple_urls():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com/one", body="one")
        responses.add(responses.GET, "http://example.com/two", body="two")

        resp = requests.get("http://example.com/two")
        assert_response(resp, "two")
        resp = requests.get("http://example.com/one")
        assert_response(resp, "one")

    run()
    assert_reset()


def test_multiple_methods():
    @responses.activate
    def run():
        responses.add(responses.GET, "http://example.com/one", body="gotcha")
        responses.add(responses.POST, "http://example.com/one", body="posted")

        resp = requests.get("http://example.com/one")
        assert_response(resp, "gotcha")
        resp = requests.post("http://example.com/one")
        assert_response(resp, "posted")

    run()
    assert_reset()


def test_passthru(httpserver):
    httpserver.serve_content("OK", headers={"Content-Type": "text/plain"})

    @responses.activate
    def run():
        responses.add_passthru(httpserver.url)
        responses.add(responses.GET, "{}/one".format(httpserver.url), body="one")
        responses.add(responses.GET, "http://example.com/two", body="two")

        resp = requests.get("http://example.com/two")
        assert_response(resp, "two")
        resp = requests.get("{}/one".format(httpserver.url))
        assert_response(resp, "OK")
        resp = requests.get(httpserver.url)
        assert_response(resp, "OK")

    run()
    assert_reset()


def test_passthru_regex(httpserver):
    httpserver.serve_content("OK", headers={"Content-Type": "text/plain"})

    @responses.activate
    def run():
        responses.add_passthru(re.compile("{}/\\w+".format(httpserver.url)))
        responses.add(responses.GET, "{}/one".format(httpserver.url), body="one")
        responses.add(responses.GET, "http://example.com/two", body="two")

        resp = requests.get("http://example.com/two")
        assert_response(resp, "two")
        resp = requests.get("{}/one".format(httpserver.url))
        assert_response(resp, "OK")
        resp = requests.get("{}/two".format(httpserver.url))
        assert_response(resp, "OK")
        resp = requests.get("{}/three".format(httpserver.url))
        assert_response(resp, "OK")

    run()
    assert_reset()


def test_passthru_inside_callback(httpserver):
    httpserver.serve_content("OK", headers={"Content-Type": "text/plain"})

    def callback(request):
        if request.path_url == "/two":
            responses.add_passthru(request.url)
            resp = requests.get(request.url)
            return (resp.status_code, dict(resp.headers), resp.content)
        return (200, {"Content-Type": "text/plain"}, request.path_url[1:])

    @responses.activate
    def run():
        responses.add_callback(
            responses.GET,
            re.compile("{}/\\w+".format(httpserver.url)),
            callback=callback,
            content_type="text/plain",
        )

        resp = requests.get("{}/one".format(httpserver.url))
        assert_response(resp, "one")
        resp = requests.get("{}/two".format(httpserver.url))
        assert_response(resp, "OK")

    run()
    assert_reset()


def test_method_named_param():
    @responses.activate
    def run():
        responses.add(method=responses.GET, url="http://example.com", body="OK")
        resp = requests.get("http://example.com")
        assert_response(resp, "OK")

    run()
    assert_reset()


def test_passthru_unicode():
    @responses.activate
    def run():
        with responses.RequestsMock() as m:
            url = "http://موقع.وزارة-الاتصالات.مصر/"
            clean_url = "http://xn--4gbrim.xn----ymcbaaajlc6dj7bxne2c.xn--wgbh1c/"
            m.add_passthru(url)
            assert m.passthru_prefixes[0] == clean_url

    run()
    assert_reset()


def test_custom_target(monkeypatch):
    requests_mock = responses.RequestsMock(target="something.else")
    std_mock_mock = responses.std_mock.MagicMock()
    patch_mock = std_mock_mock.patch
    monkeypatch.setattr(responses, "std_mock", std_mock_mock)
    requests_mock.start()
    assert len(patch_mock.call_args_list) == 1
    assert patch_mock.call_args[1]["target"] == "something.else"


def _quote(s):
    return responses.quote(responses._ensure_str(s))


def test_cookies_from_headers():
    text = "こんにちは/世界"
    quoted_text = _quote(text)
    expected = {"x": "a", "y": quoted_text}
    headers = {"set-cookie": "; ".join(k + "=" + v for k, v in expected.items())}
    cookiejar = responses._cookies_from_headers(headers)
    for k, v in cookiejar.items():
        assert isinstance(v, str)
        assert v == expected[k]


@pytest.mark.parametrize(
    "url",
    (
        "http://example.com",
        "http://example.com/some/path",
        "http://example.com/other/path/",
    ),
)
def test_request_param(url):
    @responses.activate
    def run():
        params = {"hello": "world", "example": "params"}
        responses.add(
            method=responses.GET,
            url="{0}?hello=world".format(url),
            body="test",
            match_querystring=False,
        )
        resp = requests.get(url, params=params)
        assert_response(resp, "test")
        assert_params(resp, params)

        resp = requests.get(url)
        assert_response(resp, "test")
        assert_params(resp, {})

    run()
    assert_reset()


def test_request_param_with_multiple_values_for_the_same_key():
    @responses.activate
    def run():
        url = "http://example.com"
        params = {"key1": ["one", "two"], "key2": "three"}
        responses.add(
            method=responses.GET,
            url=url,
            body="test",
        )
        resp = requests.get(url, params=params)
        assert_response(resp, "test")
        assert_params(resp, params)

    run()
    assert_reset()


@pytest.mark.parametrize(
    "url", ("http://example.com", "http://example.com?hello=world")
)
def test_assert_call_count(url):
    @responses.activate
    def run():
        responses.add(responses.GET, url)
        responses.add(responses.GET, "http://example1.com")

        assert responses.assert_call_count(url, 0) is True

        with pytest.raises(AssertionError) as excinfo:
            responses.assert_call_count(url, 2)
        assert "Expected URL '{0}' to be called 2 times. Called 0 times.".format(
            url
        ) in str(excinfo.value)

        requests.get(url)
        assert responses.assert_call_count(url, 1) is True

        requests.get("http://example1.com")
        assert responses.assert_call_count(url, 1) is True

        requests.get(url)
        with pytest.raises(AssertionError) as excinfo:
            responses.assert_call_count(url, 3)
        assert "Expected URL '{0}' to be called 3 times. Called 2 times.".format(
            url
        ) in str(excinfo.value)

    run()
    assert_reset()


def test_request_matches_post_params():
    @responses.activate
    def run():
        responses.add(
            method=responses.POST,
            url="http://example.com/",
            body="one",
            match=[
                responses.json_params_matcher(
                    {"page": {"name": "first", "type": "json"}}
                )
            ],
        )
        responses.add(
            method=responses.POST,
            url="http://example.com/",
            body="two",
            match=[
                responses.urlencoded_params_matcher(
                    {"page": "second", "type": "urlencoded"}
                )
            ],
        )

        resp = requests.request(
            "POST",
            "http://example.com/",
            headers={"Content-Type": "x-www-form-urlencoded"},
            data={"page": "second", "type": "urlencoded"},
        )
        assert_response(resp, "two")

        resp = requests.request(
            "POST",
            "http://example.com/",
            headers={"Content-Type": "application/json"},
            json={"page": {"name": "first", "type": "json"}},
        )
        assert_response(resp, "one")

    run()
    assert_reset()


def test_request_matches_empty_body():
    @responses.activate
    def run():
        responses.add(
            method=responses.POST,
            url="http://example.com/",
            body="one",
            match=[responses.json_params_matcher(None)],
        )

        responses.add(
            method=responses.POST,
            url="http://example.com/",
            body="two",
            match=[responses.urlencoded_params_matcher(None)],
        )

        resp = requests.request("POST", "http://example.com/")
        assert_response(resp, "one")

        resp = requests.request(
            "POST",
            "http://example.com/",
            headers={"Content-Type": "x-www-form-urlencoded"},
        )
        assert_response(resp, "two")

    run()
    assert_reset()


def test_fail_request_error():
    @responses.activate
    def run():
        responses.add("POST", "http://example1.com")
        responses.add("GET", "http://example.com")
        responses.add(
            "POST",
            "http://example.com",
            match=[responses.urlencoded_params_matcher({"foo": "bar"})],
        )

        with pytest.raises(ConnectionError) as excinfo:
            requests.post("http://example.com", data={"id": "bad"})
        msg = str(excinfo.value)
        assert "- POST http://example1.com/ URL does not match" in msg
        assert "- GET http://example.com/ Method does not match" in msg
        assert "- POST http://example.com/ Parameters do not match" in msg

    run()
    assert_reset()


@pytest.mark.parametrize(
    "response_params, expected_representation",
    [
        (
            {"method": responses.GET, "url": "http://example.com/"},
            (
                "<Response(url='http://example.com/' status=200 "
                "content_type='text/plain' headers='null')>"
            ),
        ),
        (
            {
                "method": responses.POST,
                "url": "http://another-domain.com/",
                "content_type": "application/json",
                "status": 404,
            },
            (
                "<Response(url='http://another-domain.com/' status=404 "
                "content_type='application/json' headers='null')>"
            ),
        ),
        (
            {
                "method": responses.PUT,
                "url": "http://abcd.com/",
                "content_type": "text/html",
                "status": 500,
                "headers": {"X-Test": "foo"},
                "body": {"it_wont_be": "considered"},
            },
            (
                "<Response(url='http://abcd.com/' status=500 "
                "content_type='text/html' headers='{\"X-Test\": \"foo\"}')>"
            ),
        ),
    ],
)
def test_response_representations(response_params, expected_representation):
    response = Response(**response_params)

    assert str(response) == expected_representation
    assert repr(response) == expected_representation


def test_mocked_responses_list_registered():
    @responses.activate
    def run():
        first_response = Response(
            responses.GET,
            "http://example.com/",
            body="",
            headers={"X-Test": "foo"},
            status=404,
        )
        second_response = Response(
            responses.GET, "http://example.com/", body="", headers={"X-Test": "foo"}
        )
        third_response = Response(
            responses.POST,
            "http://anotherdomain.com/",
        )
        responses.add(first_response)
        responses.add(second_response)
        responses.add(third_response)

        mocks_list = responses.registered()

        assert mocks_list == responses.mock._matches
        assert mocks_list == [first_response, second_response, third_response]

    run()
    assert_reset()
