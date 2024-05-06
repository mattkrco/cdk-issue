# cdk-issue

This is a simplified sample cdk deployment involving two separate stacks - one for dynamo and one for lambda. In the real world, these stacks involve dozens of tables and dozens of lambda functions. Each table and lambda is defined at the beginning of cdk_app_stack and lambda_stack, and then dynamically created by CDK.

I am unable to remove a table without resorting to workarounds. To reproduce, run cdk deploy --all, changing cdk_app_stack.py to use "old_table_defs", and lambda_stack.py to use "old_lambda_defs". Then switch them to use "new_table_defs" and "new_lambda_defs", and rerun cdk deploy -all. It should throw an error saying "Export cdk-app:ExportsOutputFnGetAtttableTwo3F505A29Arn45AA5E74 cannot be deleted as it is in use by lambda-stack".

I have already figured out how to use the --exclusively flag to deploy one stack at a time to get around this issue, but I would like to have a setup that doesn't require a workaround, so that I only need to run "cdk deploy" once.
