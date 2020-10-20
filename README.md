# Test Auth

This is a very basic app to test authentication in the Fedora infrastructure.

## Configuration

You can configure the app using a configuration file, you need to point to this
file with the `TESTAUTH_SETTINGS` environment variable.

In the configuration file you can set:

- `SECRET_KEY`: a unique secret key for signing cookies (see the Flask documentation)
- `OIDC_CLIENT_SECRETS`: the path to the `client_secrets.json` file for OIDC auth
- `OIDC_SCOPES`: the list of OIDC scopes to request from the server
- `OPENID_ENDPOINT`: the URL of the OpenID server endpoint

## OIDC

Test the OIDC authentication system using the `/oidc` path. You must have set a client secrets file by doing:

```
$ pip3 install oidc-register
$ oidc-register https://iddev.fedorainfracloud.org/openidc/ http://localhost:5000/oidc
```

Where `https://iddev.fedorainfracloud.org/openidc/` is the URL of the OIDC server endpoint.

## OpenID

Test the OpenID authentication system using the `/openid` path. There is no server-side configuration to do.
