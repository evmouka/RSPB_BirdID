def update_and_join(dict1, dict2):
    for key, value in dict2.items():
        if key == 'new_attribute' and key in dict1:
            dict1['new_attribute'] = update_and_join(dict1['new_attribute'], dict2['new_attribute'])
            continue
        if key in dict1:
            existing_values = set(dict1[key].split(", "))
            new_values = set(value.split(", "))
            combined_values = ", ".join(existing_values | new_values)
            dict1[key] = combined_values
        else:
            dict1[key] = value
    return dict1