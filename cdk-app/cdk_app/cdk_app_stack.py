import aws_cdk
from aws_cdk import Stack, CfnOutput, aws_events_targets
from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_dynamodb as _dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from constructs import Construct


class CdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        response_lambda = _lambda.Function(self,
            id="sampleLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="lambda.handler")

        auth_lambda = _lambda.Function(self,
            id="authLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="authorizer.handler")

        api = _apigw.RestApi(
            self,
            "sampleApi",
            default_cors_preflight_options={
                'allow_origins': _apigw.Cors.ALL_ORIGINS,
                'allow_methods': ["POST", "OPTIONS"],
                'allow_headers': [
                    'Content-Type',
                    'X-Amz-Date',
                    'Authorization',
                    'X-Api-Key',
                    'X-Amz-Security-Token'
                ]
            }
        )

        auth = _apigw.CfnAuthorizer(self, "sampleAuthorizer",
                                                name="sampleAuthorizer",
                                                rest_api_id=api.rest_api_id,
                                                type="REQUEST",

                                                authorizer_result_ttl_in_seconds=1,
                                                authorizer_uri=f"arn:aws:apigateway:{aws_cdk.Aws.REGION}:lambda:path/2015-03-31/functions/{auth_lambda.function_arn}/invocations",
                                                identity_source=_apigw.IdentitySource.header('auth-header'))

        authorizer_id = auth.attr_authorizer_id

        auth_lambda.grant_invoke(iam.ServicePrincipal("apigateway.amazonaws.com"))

        auth_ifunction = _lambda.Function.from_function_arn(self,
                                                            "authIFunction",
                                                            auth_lambda.function_arn
                                                            )

        auth2 = _apigw.RequestAuthorizer(self, 
                                        "sampleAuthorizer2",
                                        identity_sources=[_apigw.IdentitySource.header('auth-header')],
                                        handler=auth_ifunction,
                                        results_cache_ttl=aws_cdk.Duration.seconds(1)
                                        )
        
        res = api.root.add_resource("sample-resource")

        lambda_integration = _apigw.LambdaIntegration(
            response_lambda,
            proxy=False,
            integration_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": "'*'",
                    },
                }
            ],
        )

        method = res.add_method(
            "POST",
            lambda_integration,
            #authorization_type=_apigw.AuthorizationType.CUSTOM,
            #authorizer=auth,
            authorizer=auth2,
            method_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": True,
                    },
                }
            ]
        )

        # method_resource = method.node.find_child('Resource')
        # method_resource.add_property_override('AuthorizationType', 'CUSTOM')
        # method_resource.add_property_override('AuthorizerId', {
        #     "Ref": authorizer_id})