import os
import pytest
import httpx
from unittest.mock import MagicMock, patch
from server import mcp, _fetch_search_results, search, google_search, google_shopping, google_jobs, youtube_search


@pytest.mark.asyncio
async def test_list_tools():
    tools = await mcp.list_tools()
    tool_names = [t.name for t in tools]
    assert len(tools) == 5
    assert tool_names == [
        "search",
        "google_search",
        "google_shopping",
        "google_jobs",
        "youtube_search",
    ]


@pytest.mark.asyncio
async def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("SEARCHAPI_API_KEY", raising=False)
    res = await _fetch_search_results("google", "test")
    assert res == {"error": "SEARCHAPI_API_KEY environment variable is not set"}


@pytest.mark.asyncio
async def test_successful_fetch(monkeypatch):
    monkeypatch.setenv("SEARCHAPI_API_KEY", "test-key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"organic_results": [{"title": "Python"}]}

    with patch("httpx.AsyncClient.get", return_value=mock_response) as mock_get:
        res = await google_search("python")
        assert res == {"organic_results": [{"title": "Python"}]}
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["headers"] == {"Authorization": "Bearer test-key"}
        assert kwargs["params"] == {"engine": "google", "q": "python"}


@pytest.mark.asyncio
async def test_non_200_response(monkeypatch):
    monkeypatch.setenv("SEARCHAPI_API_KEY", "test-key")

    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        res = await search("google", "python")
        assert res == {
            "error": "API request failed with status code 401: Unauthorized"
        }


@pytest.mark.asyncio
async def test_exception_handling(monkeypatch):
    monkeypatch.setenv("SEARCHAPI_API_KEY", "test-key")

    with patch("httpx.AsyncClient.get", side_effect=httpx.RequestError("Network error")):
        res = await google_jobs("developer")
        assert res == {
            "error": "An error occurred while calling SearchApi: Network error"
        }
