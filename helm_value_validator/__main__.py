import argparse
import os
import subprocess

from helm_value_validator.colors import ENDC, RED
from helm_value_validator.validator import compare_values


def main():
    parser = argparse.ArgumentParser(description="Compare custom Helm chart values against official defaults.")
    parser.add_argument(
        "-c", "--custom", help="The path to your custom Helm values file (e.g., custom_values.yaml).", required=True
    )
    parser.add_argument(
        "-n", "--chart", help="The Helm chart name (e.g., prometheus-community/kube-prometheus-stack).", required=True
    )

    args = parser.parse_args()

    # Ensure helm and yq are available (yq is not strictly necessary but good to check)
    if not os.environ.get("SKIP_TOOL_CHECK"):
        try:
            subprocess.run(["/usr/bin/helm", "version"], check=True, capture_output=True, shell=False)
        except subprocess.CalledProcessError:
            print(f"{RED}Error: 'helm' command not found. Please ensure Helm is installed and in your PATH.{ENDC}")
            exit(1)

    compare_values(args.custom, args.chart)


if __name__ == "__main__":
    main()
