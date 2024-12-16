def extract_name_from_email(email):
    # Split the email address by "@" to get the username part
    username = email.split("@")[0]

    # Split the username by "." and assume the first part is the name
    name_parts = username.split(".")

    # Capitalize each part of the name and join them
    name = " ".join([part.capitalize() for part in name_parts])

    return name
