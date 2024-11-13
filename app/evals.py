# main.py
import sys
from pathlib import Path
import pytest


# Ajoute le répertoire racine du projet au chemin Python
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from swarm import Swarm
from agents.base_agents import kubectl_agent, stripe_agent, grafana_agent, db_agent

client = Swarm()

def run_and_get_tool_calls(agent, query, get="tool_calls"):
    """Helper function to run a query with an agent and return the specified attribute from response messages."""
    message = {"role": "user", "content": query}
    response = client.run(agent=agent, messages=[message], execute_tools=False)
    print(response.messages[-1])
    return response.messages[-1].get(get)

def run_and_get(agent, query):
    """Helper function to run a query with an agent and return the specified attribute from response messages."""
    message = {"role": "user", "content": query}
    response = client.run(agent=agent, messages=[message], execute_tools=False)
    return response.messages[-1]

# Configuration de tests
test_cases = [
    {"agent": kubectl_agent, "query": "get pods count", "expected_function": "kubectl"},
    {"agent": kubectl_agent, "query": "get app chatbot", "expected_function": "get_app", "expected_arguments": '{"app_name":"chatbot"}'},
    {"agent": kubectl_agent, "query": "unsync app chatbot", "expected_function": "update_sync_policy", "expected_arguments": '{"app_name":"chatbot","is_sync":"false"}'},
    {"agent": stripe_agent, "query": "get user test@test.com", "expected_function": "stripe_query", "expected_arguments": '{"email":"test@test.com"}'},
    {"agent": stripe_agent, "query": "get payments of customer id 1234RTY78", "expected_function": "stripe_payments_list", "expected_arguments": '{"customer_id":"1234RTY78"}'},
    {"agent": grafana_agent, "query": "show user test@test.com in grafana", "expected_function": "grafana_query", "expected_arguments": '{"email":"test@test.com"}'},
]

@pytest.mark.parametrize("case", test_cases)
def test_tool_calls(case):
    """Test tool calls based on provided cases in `test_cases`."""
    tool_calls = run_and_get_tool_calls(case["agent"], case["query"])
    
    assert tool_calls and len(tool_calls) == 1
    assert tool_calls[0]["function"]["name"] == case["expected_function"]
    
    if "expected_arguments" in case:
        assert tool_calls[0]["function"]["arguments"] == case["expected_arguments"]

@pytest.mark.parametrize(
    "query",
    [
        "cancel the subscription xxxxxx",
        "refund payment with charge id xxxxxx",
    ],
)
def test_confirm_content(query):
    """Test to confirm specific content in response messages."""
    content = run_and_get_tool_calls(stripe_agent, query, "content")
    assert "confirm" in content.lower() or "xxxxxx" in content

@pytest.mark.parametrize(
    "query",
    [
        "find user test@test.com",
        "count all users in db",
        "count all customers since today",
        "count all teslas since today",
        "find services from test@test.com"
    ],
)
def test_db_transfer_queries(query):
    """Test db_agent calls to ensure the 'transfer_to_query' function is used."""
    res = run_and_get(db_agent, query)
    content = res.get("content")
    tool_calls = res.get("tool_calls")
    assert (content and content.find('"can_answer":true')) or (tool_calls and len(tool_calls) == 1 and tool_calls[0]["function"]["name"] == "transfer_to_query")
