#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_app.cdk_app_stack import CdkAppStack
from cdk_app.lambda_stack import LambdaStack

app = cdk.App()
cdk_app_stack = CdkAppStack(app, "cdk-app")
LambdaStack(app, 'lambda-stack', cdk_app_stack.table_objects)

app.synth()
