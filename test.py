def format_name_from_file(name: str):
    parts = name.split("_")
    formatted_name = []

    for part in parts:
        if "." in part:
            part = part.upper()
        formatted_name.append(part.capitalize())

    return " ".join(formatted_name)


print(format_name_from_file("j.c._jersild"))
