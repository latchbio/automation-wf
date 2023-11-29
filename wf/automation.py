import uuid
from typing import Set

from latch.registry.table import Table
from latch.resources.tasks import small_task
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile

from .utils import launch_workflow


@small_task
def automation_task(
    input_directory: LatchDir,
    output_directory: LatchOutputDir,
    target_wf_id: str,
    table_id: str,
    params: dict,
) -> None:
    """
    Logic on how to process the input directory and launch the target workflows.
    """

    # fetch the table using Latch SDK
    automation_table = Table(table_id)
    processed_directory_column = "Processed Directory"

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

    # check if the provided table contains column `Processed Directory` and creates one if it isn't present
    # we use Latch SDK to get the columns of the table and try to get the column by name
    if automation_table.get_columns().get(processed_directory_column, None) is None:
        with automation_table.update() as automation_table_updater:  # create an update context for the table
            automation_table_updater.upsert_column(processed_directory_column, LatchDir)

    # fetch all the directories that have been processed and recorded in the Registry table previously
    resolved_directories: Set[str] = set()
    # list_records() returns a generator of records(rows) of the Registry Table
    for page in automation_table.list_records():
        for _, record in page.items():
            value = record.get_values()[processed_directory_column]
            assert isinstance(
                value, LatchDir
            )  # we only allow processing of child directories
            resolved_directories.add(str(value))

    assert isinstance(input_directory.remote_path, str)
    assert isinstance(output_directory.remote_path, str)

    # Launch the target workflow for each child directory which hasn't been processed yet.
    # Record the processed directory in the Registry table.

    # iterdir() returns an iterator of the child files and directories of the input directory
    for child in input_directory.iterdir():
        # skip files, output directory and directories that have been processed
        if (
            isinstance(child, LatchFile)
            or str(child) == str(output_directory)
            or str(child) in resolved_directories
        ):
            continue

        with automation_table.update() as automation_table_updater:
            # use a util function to launch the target workflow with the right parameters
            launch_workflow(
                target_wf_id=target_wf_id,
                params=params,
            )
            # update registry table with the processed directory
            automation_table_updater.upsert_record(
                str(uuid.uuid4()),
                **{
                    processed_directory_column: child,
                },
            )
