def print_validation_report(errors):
    if not errors:
        print("Data validation passed ✅")
    else:
        print("Data validation failed ❌")
        for error in errors:
            print(" -", error)