def search_web(query, tavily):
    result = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )
    return result["results"]