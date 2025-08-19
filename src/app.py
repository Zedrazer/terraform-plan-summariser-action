"""
Python executable for Terraform Plan Summariser GitHub Action
"""

import json
import os
from jinja2 import Template

def parse_terraform_plan():
    plan_file = os.environ.get("INPUT_TF_PLAN_FILE")
    plan_dir = os.environ.get("INPUT_TF_PLAN_DIR")
    alert_type = os.environ.get("INPUT_ALERT_TYPE")

    with open(f"/github/workspace/{plan_dir}/{plan_file}") as terraform_plan_json:
        terraform_plan = json.load(terraform_plan_json)

    changes = terraform_plan["resource_changes"]

    creates = []
    deletes = []
    updates = []
    replaces = []

    for change in changes:
        action = change["change"]["actions"]
        resource = change["address"]
        if str(action) == "['create']":
            action_fmt = ":white_check_mark:"
            creates.append(f" |{action_fmt} | {resource} |")
        elif str(action) == "['update']":
            action_fmt = ":wrench:"
            updates.append(f"| {action_fmt} | {resource} |")
        elif str(action) == "['delete']":
            action_fmt = ":x:"
            deletes.append(f"| {action_fmt} | {resource} |")
        elif str(action) == "['delete', 'create']":
            action_fmt = ":interrobang:"
            replaces.append(f"| {action_fmt} | {resource} |")

    if not creates and not updates and not deletes and not replaces:
        result = "No changes were detected in the terraform plan. Nothing to summarise."
        show_tables = False
    else:
        result = "The following changes have been detected from the terraform plan and can be summarised as follows:"
        show_tables = True

    with open("/src/step_output.md.j2") as step_output_template:
        template = Template(step_output_template.read())

    rendered_step_output_template = template.render(
        result=result,
        creates=creates,
        updates=updates,
        deletes=deletes,
        replaces=replaces,
        show_tables=show_tables,
    )

    with open("/src/step_output.md", "w") as step_output_final:
        step_output_final.write(rendered_step_output_template)

    with open("/src/step_output.md") as step_output:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as step_output_env:
            print(step_output.read(), file=step_output_env)


parse_terraform_plan()
