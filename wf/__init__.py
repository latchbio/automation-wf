from latch.resources.workflow import workflow
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter

from wf.automation import automation_task

metadata = LatchMetadata(
    display_name="Automation Template",
    author=LatchAuthor(
        name="YOUR NAME HERE",
    ),
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
    automation_task(
        input_directory=input_directory,
        output_directory=LatchOutputDir(
            path="latch://<FIXME>"  # fixme: change to remote path of desired output directory
        ),
        target_wf_id="FIXME",  # fixme: change wf_id to desired workflow
        table_id="FIXME",  # fixme: change table_id to desired registry table
    )
