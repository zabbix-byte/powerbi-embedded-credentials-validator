from .aadservice import AadService
from .domain.reportconfig import ReportConfig
from .domain.embedtoken import EmbedToken
from .domain.embedconfig import EmbedConfig
from .domain.embedtokenrequestbody import EmbedTokenRequestBody
import requests
import json

# This class generate the link


class PbiEmbedService:
    def get_embed_params_for_single_report(self, workspace_id, report_id, additional_dataset_id=None, **kwargs):
        report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}'
        api_response = requests.get(report_url, headers=self.get_request_header(**kwargs))
        api_response = json.loads(api_response.text)
        report = ReportConfig(api_response['id'], api_response['name'], api_response['embedUrl'])
        dataset_ids = [api_response['datasetId']]

        if additional_dataset_id is not None:
            dataset_ids.append(additional_dataset_id)

        embed_token = self.get_embed_token_for_single_report_single_workspace(report_id, dataset_ids, workspace_id, **kwargs)
        embed_config = EmbedConfig(embed_token.tokenId, embed_token.token, embed_token.tokenExpiry, [report.__dict__])
        return json.dumps(embed_config.__dict__)

    def get_embed_token_for_single_report_single_workspace(self, report_id, dataset_ids, target_workspace_id=None, **kwargs):
        request_body = EmbedTokenRequestBody()

        for dataset_id in dataset_ids:
            request_body.datasets.append({'id': dataset_id})

        request_body.reports.append({'id': report_id})

        if target_workspace_id is not None:
            request_body.targetWorkspaces.append({'id': target_workspace_id})

        embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
        api_response = requests.post(embed_token_api, data=json.dumps(
            request_body.__dict__), headers=self.get_request_header(**kwargs))

        api_response = json.loads(api_response.text)
        embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])
        return embed_token

    def get_request_header(self, **kwargs):
        return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + AadService.get_access_token(**kwargs)}
