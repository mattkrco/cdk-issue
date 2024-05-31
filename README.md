# cdk-issue

This is a simplified sample cdk deployment involving two separate stacks - one for dynamo and one for lambda. In the real world, these stacks involve dozens of tables and dozens of lambda functions, as well as other constructs. Each table and lambda is defined at the beginning of cdk_app_stack and lambda_stack, and then dynamically created by CDK.

I am unable to add an index to an already existing table. To reproduce, run "cdk bootstrap" and then "cdk deploy --all". Then edit cdk_app_stack.py, changing 'add_index' to True on line 17. Then, rerun "cdk deploy --all". It should throw an error saying "Export cdk-app:ExportsOutputFnGetAtttableTwo3F505A29Arn45AA5E74 cannot be deleted as it is in use by lambda-stack".

Here are some relevant github issues I found around this issue:

https://github.com/aws/aws-cdk/issues/5304

https://github.com/aws/aws-cdk/pull/12778
