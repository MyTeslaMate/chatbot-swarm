# agents/base_agents.py
from swarm import Agent

# Import utilities
from utils.db import *
from utils.print import *
from utils.kubernetes import *

# Import services
from services.stripe_service import *
from services.grafana_service import *
from services.docs_service import *
from services.notification_service import *

# Import agent functions and create transfer functions
def transfer_to_user_center_agent():
    return user_interface_agent

def transfer_to_help_center():
    return help_center_agent

def transfer_to_stripe_agent():
    return stripe_agent

def transfer_to_grafana_agent():
    return grafana_agent

def transfer_to_db_agent():
    return db_agent

def transfer_to_kube_agent():
    return kubectl_agent

def transfer_to_query():
    return query_agent

def transfer_to_apologize():
    return apologize_agent


user_interface_agent = Agent(
    name="User Interface Agent",
    instructions="""
        You are a user interface agent that handles all interactions with the user.
        Call this agent for general questions and when no other agent is correct for the user query. 
        When you welcome user only, show all your agents and capabilities.
        Users can go back to you when they write words like: menu, go back, go user center.
    """,
    functions=[
        transfer_to_help_center,
        transfer_to_stripe_agent,
        transfer_to_db_agent,
        transfer_to_grafana_agent,
        transfer_to_kube_agent
    ]
)

DATA_DESCRIPTION = """
The Postgre database contains an app dataset split into two tables:

1. Table: users:
 This table contains details about users, including their id, name, email, grafana_org_id.
 Columns: id, created_at, name, email, grafana_org_id, tesla_id.

2. Table: services:
 This table provides services owned by users including id, user_id and status.
 Columns: id, name, created_at, user_id, status.

"""

db_agent = Agent(
    name="Db Agent",
    instructions=f"""You are a database reading bot that can answer users' questions using information from a database. \n
    {DATA_DESCRIPTION} \n
    Given the user's question, decide whether the question can be answered using the information in the database. \n
    Return a JSON with two keys, 'reasoning' and 'can_answer', and no preamble or explanation.
    Return one of the following JSON:
    {{"reasoning": "I can find a user based solely on an email address because email column on user table contains it.", "can_answer":true}}
    {{"reasoning": "I can find the services of customer because user_id column is linked with id column of customer.", "can_answer":true}}
    {{"reasoning": "I can find active service because status column is 1.", "can_answer":true}}
    {{"reasoning": "I can aggregate on id to count users or services.", "can_answer":true}}
    {{"reasoning": "I can filter by date with the created_at field.", "can_answer":true}}
    {{"reasoning": "I can find customers because they are users with a grafana_org_id.", "can_answer":true}}
    {{"reasoning": "I can find teslas because they are users with a tesla_id.", "can_answer":true}}
    
    If the question can be answered, hand it over to the Query agent.
    If it's not possible, pass the task to the Apologize agent and explain why you can't.
    You must always pass the task to another agent.""",
    functions=[transfer_to_query, transfer_to_apologize],
    #parallel_tool_calls=False, # one query at time
)

query_agent = Agent(
    name="Query Agent",
    instructions=f"""You are a database reading bot that can answer users' questions using information from a database. \n
    {DATA_DESCRIPTION} \n
    In the previous step, a plan has been prepared. Use the plan to create a SQL query and call the database.
    Show the result of this call.
    You must always pass the task the user center agent.
    """,
    functions=[query_db, transfer_to_stripe_agent, transfer_to_user_center_agent],
    parallel_tool_calls=False, # one query at time
)

apologize_agent = Agent(
    name="Apologize Agent",
    instructions="""Apologize and explain to the user why you cannot complete the task.
 Display the failed query if you can.
    """,
    functions=[transfer_to_query, transfer_to_user_center_agent]
)

help_center_agent = Agent(
    name="Help Center Agent",
    instructions="You are a Teslamate and Myteslamate agent who deals with questions about these products.",
    functions=[query_docs, submit_ticket, send_email, transfer_to_user_center_agent]
)

stripe_agent = Agent(
    name="Stripe Agent",
    instructions="""
        You are a Stripe help center agent who deals with questions about customers, subscription status, payment, billing etc.
        
        Important only for stripe_cancel and stripe_refund functions: ask to confirm with "yes" before run!
    """,
    functions=[stripe_query, stripe_payments_list, stripe_cancel, stripe_refund, transfer_to_user_center_agent],
)

grafana_agent = Agent(
    name="Grafana Agent",
    instructions="""You are a Grafana help center agent who deals with questions about users, dashboards etc.

    Always ask if you need to pass the task to user center agent or stripe agent.
    """,
    functions=[grafana_query, transfer_to_user_center_agent],
)

kubectl_agent = Agent(
    name="Kubectl Agent",
    instructions="""You are a kubectl reading bot that can answer users' questions using information from a kubernetes. \n
    In the previous step, a plan has been prepared. Use the plan to create a kubectl command and call the command. 
    The command ALWAYS begin by "kubectl ".
    
    Please send is_sync parameter as boolean only for update_sync_policy.
    Please always confirm before run restore_db and update_grafana.
    """,
    functions=[kubectl, get_app, update_sync_policy, restore_db, update_grafana, transfer_to_user_center_agent]
)
