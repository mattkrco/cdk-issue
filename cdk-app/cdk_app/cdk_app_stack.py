import aws_cdk
from aws_cdk import Stack, CfnOutput, aws_events_targets
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from constructs import Construct

lambda_defs = [
    {
        'id': 'sampleLambda',
        'tables_used': [
            'sampleTable'
        ]
    }
]

table_defs = [
    {
        'id': 'sampleTable',
        'partition_key': "PartitionKey"
    }
]


class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table_objects = {}

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

            table_objects[table_def['id']] = sample_table

        for lambda_def in lambda_defs:
            lambda_env_data={}

            for table_used in lambda_def['tables_used']:
                lambda_env_data[f'TABLENAME{table_used.upper()}'] = table_objects[table_used].table_name

            sample_lambda = _lambda.Function(self,
                id=lambda_def['id'],
                runtime=_lambda.Runtime.PYTHON_3_9,
                code=_lambda.Code.from_asset("lambda"),
                handler="lambda.handler",
                environment=lambda_env_data
            )

            for table_used in lambda_def['tables_used']:
                table_objects[table_used].grant_read_write_data(sample_lambda)

