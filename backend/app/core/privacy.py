def mask_hash_identificador(hash_str: str) -> str:
    if not hash_str:
        return ""
    if len(hash_str) <= 8:
        return "*" * len(hash_str)
    return f"{hash_str[:4]}{'*' * (len(hash_str) - 8)}{hash_str[-4:]}"


def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return ""
    user, domain = email.split("@", 1)
    if len(user) <= 2:
        masked_user = "*" * len(user)
    else:
        masked_user = user[0] + "*" * (len(user) - 2) + user[-1]
    return masked_user + "@" + domain
