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
        'id': 'tableOne',
        'partition_key': "PartitionKey",
        'sort_key': "SortKey",
        'add_index': False
    },
    {
        'id': 'tableTwo',
        'partition_key': "PartitionKey",
        'sort_key': "SortKey"
    }
]



class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table_objects = {}

        ### update old_table_defs and new_table_defs here:
        for table_def in table_defs:
            table_object = _dynamodb.Table(self,
                id=table_def['id'],
                partition_key=_dynamodb.Attribute(
                    name=table_def['partition_key'],
                    type=_dynamodb.AttributeType.STRING
                ),
                sort_key=_dynamodb.Attribute(
                    name=table_def['sort_key'],
                    type=_dynamodb.AttributeType.STRING
                ),
                billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
                removal_policy=aws_cdk.RemovalPolicy.DESTROY
            )

            if table_def.get('add_index', False):
                table_object.add_local_secondary_index(
                    index_name='sample-index',
                    sort_key =_dynamodb.Attribute(
                        name='IndexKey',
                        type=_dynamodb.AttributeType.STRING
                    ),
                    projection_type=_dynamodb.ProjectionType.ALL
                )

            self.table_objects[table_def['id']] = table_object

