# cdk-issue

This is a simplified sample stack involving one dynamo table and one lambda function. In the real world, this stack involves dozens of tables and dozens of lambda functions.

The goal is to separate the stack into two separate stacks - one for dynamo and one for lambda.

Each table and lambda is defined at the beginning of cdk_app_stack, and then dynamically created by CDK. Each lambda function should only be given access to those tables in its definition.
