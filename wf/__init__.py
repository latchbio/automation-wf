from latch.resources.workflow import workflow
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.metadata import LatchAuthor, LatchMetadata, LatchParameter
from wf.automation import automation_task

metadata = LatchMetadata(
    # MODIFY NAMING METADATA BELOW
    display_name="Automation Template",
    author=LatchAuthor(
        name="Your Name Here",
    ),
    # MODIFY NAMING METADATA ABOVE
    # IMPORTANT: these exact parameters are required for the workflow to work with automations
    parameters={
        "input_directory": LatchParameter(
            display_name="Input Directory",
        )
    },
)


@workflow(metadata)
def automation_workflow(input_directory: LatchDir) -> None:
    output_directory = LatchOutputDir(
        path="latch://FIXME"  # fixme: change to remote path of desired output directory
    )

    automation_task(
        input_directory=input_directory,
        output_directory=output_directory,
        target_wf_id="FIXME",  # fixme: change wf_id to the desired workflow id
        table_id="FIXME",  # fixme: change table_id to the desired registry table
    )
