import requests
import datetime


def run_query(query, query_vars, headers):
    """
    Send a query via post request to the graphql endpoint at github.
    Args:
        query: a graphql query
    Returns: A JSON containing the query results
    """
    request = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": query_vars},
        headers=headers,
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(
            f"""
            Query failed to run by returning code of
            {request.status_code}. {query}
            """
        )


# GraphQL vs REST: I chose GraphQL because it's faster than a traditional REST
# query and only returns the data I care about.
# Rather than try to pry results out of a lengthy JSON object,
# just give me what I want and leave the rest out.
# Used the github graphql explorer to figure out what I wanted.
# Got help paginating github api from
# https://github.com/simonw/til/blob/main/github/graphql-pagination-python.md
def construct_query(after_cursor=None):
    """
    Construct a graphql query
    Args:
        after_cursor: the edge cursor used to identify the next page
    Returns: a formatted query <String>
    """
    return """
    query($repository: String!, $owner: String!) {
        repository(name: $repository, owner: $owner) {
            pullRequests(first: 100, after:AFTER, orderBy: {field: UPDATED_AT, direction: DESC}) {
            pageInfo {
                hasNextPage
                endCursor
            }
            edges {
                node {
                author {
                    login
                }
                closedAt
                createdAt
                mergedAt
                updatedAt
                state
                comments {
                    totalCount
                }
                }
            }
            }
        }
    }
    """.replace(
        "AFTER", '"{}"'.format(after_cursor) if after_cursor else "null"
    )


def construct_pr_stats(query_vars, headers):
    """
    Constructs Query, sends request, splits results into lists,
    adds lists to dict.
    Returns: Dict of Lists
    """
    authors = []
    comment_count = []
    closed = 0
    created = 0
    merged = 0
    updated = 0
    undefined = 0

    has_next_page = True
    after_cursor = None
    # Could parameterize days for longer timeline
    start_time = datetime.datetime.now() - datetime.timedelta(days=7)

    while has_next_page:
        # Constructs the query and sends the request
        results = run_query(construct_query(after_cursor), query_vars, headers)

        ## Uncomment for debugging
        # import json
        # print()
        # print(json.dumps(results, indent=4))
        # print()

        for result in results["data"]["repository"]["pullRequests"]["edges"]:
            # convert string value to datetime object
            updated_time = datetime.datetime.strptime(
                result["node"]["updatedAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
            created_time = datetime.datetime.strptime(
                result["node"]["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
            )
            if result["node"]["mergedAt"] is not None:
                merged_time = datetime.datetime.strptime(
                    result["node"]["mergedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )
            if result["node"]["closedAt"] is not None:
                closed_time = datetime.datetime.strptime(
                    result["node"]["closedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )

            # updated_time is the last interaction with a PR
            # if the last interaction with a PR is after
            # the defined start time, update report values
            # else - we've reached the last PR within the
            # defined timeframe, so return the report document.
            if updated_time >= start_time:
                if result["node"]["state"] == "MERGED":
                    if merged_time >= start_time:
                        merged += 1
                    else:
                        updated += 1
                elif result["node"]["state"] == "CLOSED":
                    if closed_time >= start_time:
                        closed += 1
                    else:
                        updated += 1
                elif result["node"]["state"] == "OPEN":
                    if created_time >= start_time:
                        created += 1
                    else:
                        updated += 1
                else:
                    undefined += 1

                authors.append(result["node"]["author"]["login"])
                comment_count.append(result["node"]["comments"]["totalCount"])
            else:
                leaderboard = {}
                for author in authors:
                    leaderboard[author] = authors.count(author)

                return {
                    "leaderboard": sorted(
                        leaderboard, key=leaderboard.get, reverse=True
                    )[:3],
                    "updated": updated,
                    "new": created,
                    "comment_count": sum(comment_count),
                    "closed": closed,
                    "contributor_count": len(set(authors)),
                    "merged": merged,
                    "start_time": start_time,
                    "total_prs": sum(
                        [merged, created, closed, updated, undefined]
                    ),
                }
        # Check for next page and set the after cursor to modify the query
        # before sending the next request
        has_next_page = results["data"]["repository"]["pullRequests"][
            "pageInfo"
        ]["hasNextPage"]
        after_cursor = after_cursor = results["data"]["repository"][
            "pullRequests"
        ]["pageInfo"]["endCursor"]
