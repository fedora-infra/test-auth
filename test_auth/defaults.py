# OIDC
OIDC_CLIENT_SECRETS = "client_secrets.json"
OIDC_SCOPES = [
    "openid",
    "email",
    "profile",
    "https://id.fedoraproject.org/scope/groups",
    "https://id.fedoraproject.org/scope/agreements",
    "https://id.fedoraproject.org/scope/fas-attributes",
]

# OpenID
OPENID_ENDPOINT = "https://id.fedoraproject.org/openid/"
OPENID_ASK_FOR = ["email", "nickname", "fullname"]
OPENID_ASK_FOR_OPTIONAL = [
    "language",
    "timezone",
    "website",
    "blog",
    "image",
]


# FAS OpenID
FAS_OPENID_ENDPOINT = "https://id.fedoraproject.org/openid/"
