# helm-value-validator

[![Release](https://img.shields.io/github/v/release/makanu/helm-value-validator)](https://img.shields.io/github/v/release/makanu/helm-value-validator)
[![Build status](https://img.shields.io/github/actions/workflow/status/makanu/helm-value-validator/main.yml?branch=main)](https://github.com/makanu/helm-value-validator/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/makanu/helm-value-validator/branch/main/graph/badge.svg)](https://codecov.io/gh/makanu/helm-value-validator)
[![Commit activity](https://img.shields.io/github/commit-activity/m/makanu/helm-value-validator)](https://img.shields.io/github/commit-activity/m/makanu/helm-value-validator)
[![License](https://img.shields.io/github/license/makanu/helm-value-validator)](https://img.shields.io/github/license/makanu/helm-value-validator)

Just a simple no dependency helm values validator script.

## Usage

This Repo is still in development and usage of the script can change rapidly.

### Just the script

```bash
python validate.dependency
```

### As the Package

To better maintain, I converted the script also as a python package.

You need to install [uv](https://docs.astral.sh/uv/).

```bash
uv run helm-value-validator -h
```

- **Github repository**: <https://github.com/makanu/helm-value-validator/>
- **Documentation** <https://makanu.github.io/helm-value-validator/>

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
