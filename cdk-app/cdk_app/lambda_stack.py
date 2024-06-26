import aws_cdk
from aws_cdk import Stack, aws_lambda as _lambda
from constructs import Construct

lambda_defs = [
    {
        'id': 'lambdaOne',
        'tables_used': [
            'tableOne'
        ]
    },
    {
        'id': 'lambdaTwo',
        'tables_used': [
            'tableOne','tableTwo'
        ]
    }
]


class LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, tables, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### update old_lambda_defs and new_lambda_defs here:
        for lambda_def in lambda_defs:
            lambda_env_data={}

            for table_used in lambda_def['tables_used']:
                lambda_env_data[f'TABLENAME{table_used.upper()}'] = tables[table_used].table_name

            sample_lambda = _lambda.Function(self,
                id=lambda_def['id'],
                runtime=_lambda.Runtime.PYTHON_3_9,
                code=_lambda.Code.from_asset("lambda"),
                handler=f"{lambda_def['id']}.handler",
                environment=lambda_env_data
            )

            for table_used in lambda_def['tables_used']:
                tables[table_used].grant_read_write_data(sample_lambda)
