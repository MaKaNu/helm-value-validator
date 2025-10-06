import subprocess

import yaml

from helm_value_validator.colors import BLUE, BOLD, ENDC, GRAY, GREEN, RED, YELLOW


def fetch_default_values(chart_name):
    """Fetches the default values.yaml content for a Helm chart using subprocess."""
    print(f"{YELLOW}{BOLD}--- 1. Fetching default values for {chart_name} ---{ENDC}")
    try:
        # Run 'helm show values' and capture stdout
        result = subprocess.run(  # noqa: S603
            ["/usr/bin/helm", "show", "values", chart_name], capture_output=True, text=True, check=True
        )
        # Load the YAML content directly from the output string
        return yaml.safe_load(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error fetching Helm chart values:{ENDC}")
        print(e.stderr)
        if e.stderr == "Error: repo prometheus-community not found\n":
            print(f"{BLUE}Use Full url or add helm repo!{ENDC}")
        exit(1)
    except Exception as e:
        print(f"{RED}An unexpected error occurred during fetching or parsing: {e}{ENDC}")
        exit(1)


def flatten_yaml(data, parent_key="", sep="."):
    """Recursively flattens a YAML dictionary into a dot-separated key-value map."""
    items = {}
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_yaml(v, new_key, sep=sep))
        elif isinstance(v, list):
            # Do not flatten lists further, as we only care about scalar values at the end
            # We can still check list presence, but for comparison, we treat it as a complex object.
            items[new_key] = str(v)
        else:
            items[new_key] = v
    return items


def get_value_by_path(data, path):
    """Retrieves a nested value from a dictionary using a dot-separated path."""
    keys = path.split(".")
    current = data
    try:
        for key in keys:
            current = current[key]
        return str(current)
    except (TypeError, KeyError):
        return f"{GRAY}N/A or Complex{ENDC}"  # Value not found or path points to a complex structure (list/dict)


def compare_values(basic_file, chart_name):
    """Main function to load files, compare values, and print the results."""

    # 1. Load Custom Values
    try:
        with open(basic_file) as f:
            custom_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"{RED}Error: Custom values file '{basic_file}' not found.{ENDC}")
        exit(1)

    # 2. Fetch Default Values
    default_data = fetch_default_values(chart_name)

    # 3. Flatten Custom Values to get all scalar paths
    flattened_custom = flatten_yaml(custom_data)

    # 4. Print Comparison Header
    print(f"\n{YELLOW}{BOLD}--- 2. Comparing Custom Values in '{basic_file}' to Defaults ---{ENDC}")
    print(f"{BOLD}{GRAY}{'-' * 100}{ENDC}")
    print(f"{BOLD}{GRAY}{'Key Path':<50} | {'Custom Value':<25} | {'Default Value'}{ENDC}")
    print(f"{BOLD}{GRAY}{'-' * 100}{ENDC}")

    # 5. Iterate and Compare
    sorted_paths = sorted(flattened_custom.keys())

    for path in sorted_paths:
        custom_value = flattened_custom[path]
        default_value = get_value_by_path(default_data, path)

        # Color coding the custom value
        custom_colored = f"{GREEN}{custom_value}{ENDC}"

        # Color coding the default value if it's found and differs from the custom value
        if default_value.strip(GRAY) == str(custom_value):
            default_colored = f"{BLUE}{default_value}{ENDC}"  # Default matches custom (but still showing blue if found)
        elif default_value.startswith(GRAY):
            default_colored = default_value  # N/A or Complex, keep gray
        else:
            default_colored = f"{BLUE}{default_value}{ENDC}"

        # Print comparison row
        print(f"{path:<50} | {custom_colored:<35} | {default_colored}")

    print(f"{BOLD}{GRAY}{'-' * 100}{ENDC}")
