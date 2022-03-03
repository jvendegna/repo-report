from analytics import analytics
import os

def test_analytics_query_results():
    headers = {"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"}
    query_vars = {
        "owner": os.environ.get("REPOSITORY_OWNER"),
        "repository": os.environ.get("REPOSITORY_NAME"),
    }
    results = analytics.construct_pr_stats(query_vars, headers)

    assert isinstance(results, dict)

    return results


def test_results_values():
    results = test_analytics_query_results()
    assert isinstance(results["leaderboard"], list)
    assert isinstance(results["leaderboard"][0], str)
    assert isinstance(results["merged"], int)
