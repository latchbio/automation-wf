import os
from re import A
from typing import Set
import uuid
from urllib.parse import urljoin

import requests
from latch.account import Account
from latch.resources.tasks import small_task
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch.registry.project import Project
from latch.registry.table import Table


def launch_workflow(
    wf_id: str,
    input_directory: LatchDir,
    output_directory: LatchOutputDir,
) -> None:
    token = os.environ["FLYTE_INTERNAL_EXECUTION_ID"]
    nucleus_endpoint = os.environ["LATCH_AUTHENTICATION_ENDPOINT"]
    workspace_id = Account.current().id

    headers = {
        "Authorization": f"Latch-Execution-Token {token}",
    }

    data = {
        "account_id": workspace_id,
        "launcher_id": workspace_id,
        "workflow_id": wf_id,
        "params": {
            "input_directory": {
                "scalar": {
                    "blob": {
                        "metadata": {"type": {"dimensionality": "MULTIPART"}},
                        "uri": input_directory.remote_path,
                    }
                }
            },
            "output_directory": {
                "scalar": {
                    "blob": {
                        "metadata": {"type": {"dimensionality": "MULTIPART"}},
                        "uri": output_directory.remote_path,
                    }
                }
            },
        },
    }

    response = requests.post(
        urljoin(nucleus_endpoint, "/api/create-execution"),
        headers=headers,
        json=data,
    )
    print(f"Launched workflow {wf_id}: {response.json()}")


@small_task
def automation_task(input_directory: LatchDir, wf_id: str, table_id: str) -> None:
    automation_table = Table(table_id)

    if automation_table.get_columns().get("Resolved directories", None) is None:
        with automation_table.update() as automation_table_updater:
            automation_table_updater.upsert_column("Resolved directories", LatchDir)

    resolved_directories: Set[str] = set()
    for page in automation_table.list_records():
        for _, record in page.items():
            value = record.get_values()["Resolved directories"]
            assert isinstance(value, str)
            resolved_directories.add(value)

    assert isinstance(input_directory.remote_path, str)
    output_directory = LatchOutputDir(
        path=urljoin(input_directory.remote_path, "Output")
    )

    for child in input_directory.iterdir():
        if (
            isinstance(child, LatchFile)
            or child.remote_path == output_directory.remote_path
            or str(child) in resolved_directories
        ):
            continue

        with automation_table.update() as automation_table_updater:
            launch_workflow(
                wf_id=wf_id, input_directory=child, output_directory=output_directory
            )
            automation_table_updater.upsert_record(
                str(uuid.uuid4()),
                **{
                    "Resolved directories": child,
                },
            )
