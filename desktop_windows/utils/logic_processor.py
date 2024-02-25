import os


def check_value(compare_to, compare_with):
    if compare_to in compare_with:
        return True
    else:
        return False


def remove_file(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        print(file_path)
        if filename not in ["also-logo.png", "favicon.ico"]:
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                raise('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            continue
        