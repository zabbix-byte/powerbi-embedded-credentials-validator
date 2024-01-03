import json

from django.shortcuts import render
from .services.pbiembedservice import PbiEmbedService


def main(request):
    info = ''
    error = False
    tenant_error = False
    powerbi_user_error = False
    powerbi_pass_error = False
    client_id_error = False
    report_id_error = False
    auth_mode_error = False
    authority_url_error = False
    scope_error = False
    client_secret_error = False

    if request.method == 'POST':
        workspace_id = request.POST.get('workspaceId', '').strip()
        report_id = request.POST.get('reportId', '').strip()
        auth_mode = request.POST.get('authenticationMode', '').strip()
        client_id = request.POST.get('clientId', '').strip()
        authority_url = request.POST.get('authorityUrl', '').strip()
        tenant = request.POST.get('tenantId', '').strip()
        scope = request.POST.get('scopeBase', '').strip()
        powerbi_user = request.POST.get('powerBiUser', '').strip()
        powerbi_pass = request.POST.get('powerBiPass', '').strip()
        secret = request.POST.get('clientSecret', '').strip()

        if scope:
            scopes = scope.split(',')

        try:
            info = PbiEmbedService().get_embed_params_for_single_report(
                workspace_id=workspace_id,
                report_id=report_id,
                auth_mode=auth_mode,
                client_id=client_id,
                authority=authority_url,
                tenant_id=tenant,
                scope=scopes,
                powerbi_user=powerbi_user,
                powerbi_pass=powerbi_pass,
                client_secret=secret,
            )
        except Exception as e:
            error = True
            info = str(e)

            if 'AADSTS50059' in info:
                tenant_error = True
                powerbi_user_error = True
                powerbi_pass_error = True

            if 'AADSTS50126' in info:
                powerbi_pass_error = True

            if 'AADSTS700016' in info:
                client_id_error = True

            if 'Expecting value: line 1 column 1' in info:
                report_id_error = True

                info = 'REPORT_ID or WORKSPACE_ID not exists or some other problem.'

            if auth_mode.lower() != 'masteruser' and auth_mode.lower() != 'serviceprincipal':
                auth_mode_error = True
                info = 'AUTHENTICATION_MODE restricted on only two modes masteruser and serviceprincipal.'

            if 'authority configuration' in info or authority_url in info:
                authority_url_error = True

            if 'AADSTS65001' in info:
                scope_error = True

            if 'client_secret' in info or 'client_assertion' in info or 'AADSTS7000216' in info:
                client_secret_error = True

            if 'tenant' in info or 'AADSTS90019' in info:
                tenant_error = True

        return render(request, 'main.html', {'info': info,
                                             'workspace_id': workspace_id,
                                             'report_id': report_id,
                                             'auth_mode': auth_mode,
                                             'client_id': client_id,
                                             'authority_url': authority_url,
                                             'tenant': tenant,
                                             'scope': scope,
                                             'powerbi_user': powerbi_user,
                                             'powerbi_pass': powerbi_pass,
                                             'secret': secret,
                                             'error': error,
                                             'tenant_error': tenant_error,
                                             'powerbi_user_error': powerbi_user_error,
                                             'powerbi_pass_error': powerbi_pass_error,
                                             'client_id_error': client_id_error,
                                             'report_id_error': report_id_error,
                                             'auth_mode_error': auth_mode_error,
                                             'authority_url_error': authority_url_error,
                                             'scope_error': scope_error,
                                             'client_secret_error': client_secret_error
                                             })

    return render(request, 'main.html', {'info': info,
                                         'workspace_id': '',
                                         'report_id': '',
                                         'auth_mode': 'MasterUser',
                                         'client_id': '',
                                         'authority_url': 'https://login.microsoftonline.com/organizations',
                                         'tenant': '',
                                         'scope': 'https://analysis.windows.net/powerbi/api/.default',
                                         'powerbi_user': '',
                                         'powerbi_pass': '',
                                         'secret': '',
                                         'error': error,
                                         'tenant_error': tenant_error,
                                         'powerbi_user_error': powerbi_user_error,
                                         'powerbi_pass_error': powerbi_pass_error,
                                         'client_id_error': client_id_error,
                                         'report_id_error': report_id_error,
                                         'auth_mode_error': auth_mode_error,
                                         'authority_url_error': authority_url_error,
                                         'scope_error': scope_error,
                                         'client_secret_error': client_secret_error
                                         })
