# Test Auth

This is a very basic app to test authentication in the Fedora infrastructure.


## OIDC

Test the OIDC authentication system using the `/oidc` path. You must have set a client secrets file by doing:

```
$ pip3 install oidc-register
$ oidc-register https://iddev.fedorainfracloud.org/openidc/ http://localhost:5000
```
