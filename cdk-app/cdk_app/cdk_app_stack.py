import aws_cdk
from aws_cdk import Stack, CfnOutput, aws_events_targets
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from constructs import Construct



table_defs = [
    {
        'id': 'sampleTable',
        'partition_key': "PartitionKey"
    },
    {
        'id': 'otherTable',
        'partition_key': "PartitionKey"
    }
]


class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table_objects = {}

        for table_def in table_defs:
            sample_table = _dynamodb.Table(self,
                id=table_def['id'],
                partition_key=_dynamodb.Attribute(
                    name=table_def['partition_key'],
                    type=_dynamodb.AttributeType.STRING
                ),
                billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
                removal_policy=aws_cdk.RemovalPolicy.DESTROY
            )

            self.table_objects[table_def['id']] = sample_table


