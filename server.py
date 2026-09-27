import os
from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("searchapi")

SEARCH_API_URL = "https://www.searchapi.io/api/v1/search"


async def _fetch_search_results(
    engine: str,
    query: str,
    num: Optional[int] = None,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
) -> dict[str, Any]:
    api_key = os.getenv("SEARCHAPI_API_KEY")
    if not api_key:
        return {"error": "SEARCHAPI_API_KEY environment variable is not set"}

    headers = {"Authorization": f"Bearer {api_key}"}
    params: dict[str, Any] = {
        "engine": engine,
        "q": query,
        "num": num,
        "location": location,
        "gl": gl,
        "hl": hl,
    }
    # Remove parameters that are None
    filtered_params = {k: v for k, v in params.items() if v is not None}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                SEARCH_API_URL, headers=headers, params=filtered_params
            )
            if response.status_code != 200:
                return {
                    "error": f"API request failed with status code {response.status_code}: {response.text}"
                }
            return response.json()
    except Exception as e:
        return {"error": f"An error occurred while calling SearchApi: {str(e)}"}


@mcp.tool()
async def search(
    engine: str,
    query: str,
    num: Optional[int] = None,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
) -> dict[str, Any]:
    """Perform a search query using any SearchApi.io engine.

    Args:
        engine: Search engine name (e.g. 'google', 'bing', 'google_scholar').
        query: Search query string.
        num: Number of search results to return.
        location: Location for search results (e.g. 'New York, United States').
        gl: Country parameter for search results (2-letter country code, e.g. 'us').
        hl: Language parameter for search results (2-letter language code, e.g. 'en').
    """
    return await _fetch_search_results(
        engine=engine, query=query, num=num, location=location, gl=gl, hl=hl
    )


@mcp.tool()
async def google_search(
    query: str,
    num: Optional[int] = None,
    location: Optional[str] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
) -> dict[str, Any]:
    """Perform a Google Web search using SearchApi.io.

    Args:
        query: Search query string.
        num: Number of search results to return.
        location: Location for search results (e.g. 'New York, United States').
        gl: Country parameter for search results (2-letter country code, e.g. 'us').
        hl: Language parameter for search results (2-letter language code, e.g. 'en').
    """
    return await _fetch_search_results(
        engine="google", query=query, num=num, location=location, gl=gl, hl=hl
    )


@mcp.tool()
async def google_shopping(
    query: str,
    num: Optional[int] = None,
    gl: Optional[str] = None,
    hl: Optional[str] = None,
) -> dict[str, Any]:
    """Perform a Google Shopping search using SearchApi.io.

    Args:
        query: Search query string.
        num: Number of search results to return.
        gl: Country parameter for search results (2-letter country code, e.g. 'us').
        hl: Language parameter for search results (2-letter language code, e.g. 'en').
    """
    return await _fetch_search_results(
        engine="google_shopping", query=query, num=num, gl=gl, hl=hl
    )


@mcp.tool()
async def google_jobs(
    query: str,
    location: Optional[str] = None,
    hl: Optional[str] = None,
) -> dict[str, Any]:
    """Perform a Google Jobs search using SearchApi.io.

    Args:
        query: Search query string.
        location: Location for job search (e.g. 'New York, NY').
        hl: Language parameter for search results (2-letter language code, e.g. 'en').
    """
    return await _fetch_search_results(
        engine="google_jobs", query=query, location=location, hl=hl
    )


@mcp.tool()
async def youtube_search(
    query: str,
    hl: Optional[str] = None,
    gl: Optional[str] = None,
) -> dict[str, Any]:
    """Perform a YouTube video search using SearchApi.io.

    Args:
        query: Search query string.
        hl: Language parameter for search results (2-letter language code, e.g. 'en').
        gl: Country parameter for search results (2-letter country code, e.g. 'us').
    """
    return await _fetch_search_results(
        engine="youtube", query=query, hl=hl, gl=gl
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
