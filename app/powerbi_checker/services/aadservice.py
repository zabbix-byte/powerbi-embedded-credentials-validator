import msal


# This class generate the auth token
class AadService:
    @staticmethod
    def get_access_token(scope, auth_mode, client_id, authority, powerbi_user, powerbi_pass, tenant_id, client_secret):
        response = None
        try:
            if auth_mode.lower() == 'masteruser':

                clientapp = msal.PublicClientApplication(client_id,
                                                         authority=authority)
                accounts = clientapp.get_accounts(username=powerbi_user)

                if accounts:
                    response = clientapp.acquire_token_silent(scope, account=accounts[0])

                if not response:
                    response = clientapp.acquire_token_by_username_password(
                        powerbi_user,
                        powerbi_pass, scopes=scope)

            elif auth_mode.lower() == 'serviceprincipal':
                authority = authority.replace('organizations', tenant_id)
                clientapp = msal.ConfidentialClientApplication(client_id,
                                                               client_credential=client_secret,
                    authority=authority)

                response = clientapp.acquire_token_for_client(scopes=scope)

            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))
