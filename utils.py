def update_and_join(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            # Join existing and new value if the key exists in dict1
            dict1[key] = f"{dict1[key]} '{value}"
        else:
            # Add the new key-value pair
            dict1[key] = value
    return dict1