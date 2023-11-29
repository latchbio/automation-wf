# Automation Template Workflow

Use this template if creating a workflow to be used with automations. Check the [documentation](https://docs.latch.bio/automation/automation-usecase.html) for step-by-step instructions on how to create an automation using this template.

## Description

This workflow receives the target `input_directory` and `automation_id` as a parameters. User specifies `target_wf_id` and `table_id` inside of `__init__.py`.

The workflow iterates through all the children of the target input directory, checks if the child is a directory and that it doesn't have an entry in the Registry Table corresponding to the `table_id` specified by the user of the workflow. Then it runs the workflow corresponding to `target_wf_id` and records all processed children in the table corresponding to `table_id`.

## Register Workflow

1. Clone this repo with
    ```bash
    git clone https://github.com/latchbio/automation-wf.git
    ```

2. In `__init__.py`, edit `author` and `display_name` in the metadata.
    ```python
    metadata = LatchMetadata(
        # MODIFY NAMING METADATA BELOW
        display_name="Automation Template",
        author=LatchAuthor(
            name="Your Name Here",
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
    ```

3. In `__init__.py`, change `output_directory`, `target_wf_id` and `table_id` in the workflow function.
    ```python
    @workflow(metadata)
    def automation_workflow(input_directory: LatchDir, automation_id: str) -> None:
        output_directory = LatchOutputDir(
            path="fixme"  # fixme: change to remote path of desired output directory
        )

        automation_task(
            input_directory=input_directory,
            output_directory=output_directory,
            target_wf_id="fixme",  # fixme: change wf_id to the desired workflow id
            table_id="fixme",  # fixme: change table_id to the desired registry table
        )
    ```

4. Register this workflow with:
    ```bash
    latch register automation-wf --yes
    ```
