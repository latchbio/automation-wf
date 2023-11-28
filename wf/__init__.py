from latch.resources.workflow import workflow
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter

from wf.automation import automation_task

metadata = LatchMetadata(
    # MODIFY NAMING METADATA BELOW
    display_name="Automation Template",
    author=LatchAuthor(
        name="Taras Priadka",
    ),
    # MODIFY NAMING METADATA ABOVE
    parameters={
        "input_directory": LatchParameter(
            display_name="Input Directory",
        ),
        "automation_id": LatchParameter(
            display_name="Automation ID",
        ),
    },
)


@workflow(metadata)
def automation_workflow(input_directory: LatchDir, automation_id: str) -> None:
    output_directory = LatchOutputDir(
        path="fixme"  # fixme: change to remote path of desired output directory
    )

    # MODIFY THE WORKFLOW PARAMETERS BELOW
    params = {
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
    }
    # MODIFY WORKFLOW PARAMETERS ABOVE

    automation_task(
        input_directory=input_directory,
        output_directory=output_directory,
        params=params,
        target_wf_id="fixme",  # fixme: change wf_id to the desired workflow id
        table_id="fixme",  # fixme: change table_id to the desired registry table
    )
