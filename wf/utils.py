### DO NOT CHANGE BELOW

import os
from urllib.parse import urljoin

import requests
from latch.account import Account


def launch_workflow(
    target_wf_id: str,
    params: dict,
) -> None:
    Account.current()
    token = os.environ["FLYTE_INTERNAL_EXECUTION_ID"]
    nucleus_endpoint = os.environ["LATCH_AUTHENTICATION_ENDPOINT"]
    workspace_id = Account.current().id

    headers = {
        "Authorization": f"Latch-Execution-Token {token}",
    }

    data = {
        "account_id": workspace_id,
        "launcher_id": workspace_id,
        "workflow_id": target_wf_id,
        "params": params,
    }

    response = requests.post(
        urljoin(nucleus_endpoint, "/api/create-execution"),
        headers=headers,
        json=data,
    )
    print(f"Launched workflow {target_wf_id}: {response.json()}")


### DO NOT CHANGE ABOVE
