# Automation Template Workflow

Use this template if creating a workflow to be used with automations. Check the [documentation](https://docs.latch.bio/automation/automation-usecase.html) for step-by-step instructions on how to create an automation using this template.

**Usage Note**:

Automations are currently only passing `input_directory` as the parameter to the automation workflow. If your workflow has different parameters automation will fail to start it. Make sure that the workflows which you use with automation have the following parameter dictionary:
```python
parameters={
            "input_directory": LatchParameter(
                display_name="Input Directory",
            )
        }
```


## Description

This workflow receives the target `input_directory` as the parameter. User specifies `target_wf_id` and `table_id` inside of `__init__.py`.

Workflow parameters:
- `input_directory`: target parent directory which is watched by automation.
- `target_wf_id`:  the ID of another workflow which will process child of the `input_directory`. This workflow should contain the logic to process child directories.
- `table_id`: the ID of an empty table with no columns that you have created. This table is used to record processed children to avoid reprocessing if the workflow runs again.

The workflow iterates through all the children of the target input directory, checks if the child is a directory and that it doesn't have an entry in the Registry Table corresponding to the `table_id` specified by the user of the workflow. Then it runs the workflow corresponding to `target_wf_id` and records all processed children in the table corresponding to `table_id`.

## Use Automation Template Workflow

1. Clone this repo with:
    ```bash
    git clone https://github.com/latchbio/automation-wf.git
    ```

2. In `__init__.py`, edit `author` and `display_name` in the metadata:
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
        },
    )
    ```

3. In `__init__.py`, change `output_directory`, `target_wf_id` and `table_id` in the workflow function:
    ```python
    @workflow(metadata)
    def automation_workflow(input_directory: LatchDir) -> None:
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

4. (Optional) change the `params` dictionary in `automations.py` if your target workflow uses different parameters.
    ```python
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

    ```

5. (Optional) change the logic of how child workflows are kicked off in `automations.py` if you want the template workflow to have a different behavior.

6. Register this workflow with:
    ```bash
    latch register automation-wf --yes
    ```
