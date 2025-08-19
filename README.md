# terraform-plan-summariser-action

GitHub Action that takes a json based terraform plan output file as an input, and outputs a markdown based summary of the plan to the GitHub Actions Job Summary window

The Action is also capable of sending an alert to an MS Teams channel if required (see notes below)

## Usage

A json based terraform plan output file must first be output from a terraform plan command, as well as the directory in which the plan file has been produced in the checked out repository. A simple example of usage can be defined as follows:

```yaml
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Terraform Init
        run: |
          terraform init

      - name: Terraform Plan
        id: plan
        shell: bash
        run: |
          terraform plan --out=plan.tfplan
          terraform show -json plan.tfplan > json-plan.json
      
      - name: Summarise Plan
        uses: zedrazer/terraform-plan-summariser-action@1.0.0
        with:
          TF_PLAN_DIR: "."
          TF_PLAN_FILE: "json-plan.json"
```

Which will produce an output syled as follows:

#### Terraform Plan Summary

Key:

|                       | Action |
| -----------           | -------------- |
| :white_check_mark:    | Create |
| :interrobang:         | Replace |
| :wrench:              | Update |
| :x:                   | Delete |

The following changes have been detected from the terraform plan and can be summarised as follows:

|             | Resource |
| ----------- | -------------- |
| :interrobang: | aws_iam_role.my_iam_role |
| :wrench: | aws_iam_policy.my_iam_policy |
| :x:      | aws_iam_policy.another_iam_policy |

