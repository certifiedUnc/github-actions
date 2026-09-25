# GitHub Actions Tutorial with Python

This repository is a practical tutorial for learning GitHub Actions. It starts with a tiny Python calculator, then adds the most useful automation topics from the GitHub Actions tutorial docs:

- create an example workflow
- build and test Python code
- use a custom composite action
- build and publish a Docker image
- build and publish a Python package
- automate issue triage with `GITHUB_TOKEN`
- understand migration from other CI/CD tools


## Repository

GitHub repository for this tutorial:

```text
https://github.com/certifiedUnc/github-actions
```

This local folder is configured to use that repository as `origin`. If you need to set it again, run:

```bash
git remote set-url origin https://github.com/certifiedUnc/github-actions.git
git branch -M main
git push -u origin main
```

For a brand-new folder with no `origin` remote yet, use `git remote add origin https://github.com/certifiedUnc/github-actions.git` instead.

## Project Files

```text
.
├── calculator.py
├── test_calculator.py
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── .github
    ├── actions
    │   └── python-test
    │       └── action.yml
    └── workflows
        ├── python-ci.yml
        ├── docker.yml
        ├── package.yml
        └── issue-automation.yml
```

## 1. The Python Example

The app is intentionally small. `calculator.py` contains four functions:

```python
add(2, 3)
subtract(7, 4)
multiply(6, 5)
divide(10, 2)
```

The tests are in `test_calculator.py` and use `pytest`.

Run the project locally:

```bash
python -m pip install -r requirements.txt
pytest
python calculator.py
```

## 2. Basic GitHub Actions Concepts

A GitHub Actions workflow is a YAML file inside `.github/workflows/`.

Important terms:

- **Workflow**: the automation file, such as `python-ci.yml`.
- **Event**: what starts the workflow, such as `push`, `pull_request`, or `workflow_dispatch`.
- **Job**: a group of steps that run on the same runner.
- **Runner**: the machine that runs the job, such as `ubuntu-latest`.
- **Step**: one command or reusable action inside a job.
- **Action**: reusable automation, such as `actions/checkout` or `actions/setup-python`.

## 3. Python CI Workflow

The main workflow is `.github/workflows/python-ci.yml`.

It runs when:

- code is pushed to `main`
- a pull request targets `main`
- someone manually starts it from the Actions tab

It tests the code on Python 3.10, 3.11, and 3.12:

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

The matrix is useful because it repeats the same job with different values.

## 4. Custom Composite Action

The reusable local action is here:

```text
.github/actions/python-test/action.yml
```

It does three things:

1. Sets up Python.
2. Installs dependencies from `requirements.txt`.
3. Runs `pytest`.

The CI workflow calls it like this:

```yaml
- name: Run local Python test action
  uses: ./.github/actions/python-test
  with:
    python-version: ${{ matrix.python-version }}
```

This keeps the workflow short and shows how repeated steps can become a custom action.

## 5. Docker Workflow

The `Dockerfile` packages the calculator example into a small Python image.

Build locally:

```bash
docker build --tag calculator:local .
docker run calculator:local
```

The workflow `.github/workflows/docker.yml` has two jobs:

- `build`: builds the Docker image on pushes, pull requests, or manual runs.
- `publish`: publishes the image to GitHub Container Registry only after a push to `main`.

Publishing uses:

```yaml
permissions:
  contents: read
  packages: write
```

That gives the workflow enough permission to read the repository and write a package to GitHub Packages.

## 6. Publishing a Python Package

The Python package metadata is in `pyproject.toml`.

Build locally:

```bash
python -m pip install --upgrade build
python -m build
```

The workflow `.github/workflows/package.yml` builds package files and uploads them as a workflow artifact.

When a tag like `v1.0.0` is pushed, the workflow also publishes to PyPI using trusted publishing:

```yaml
permissions:
  id-token: write
```

For this repository, configure PyPI trusted publishing for `certifiedUnc/github-actions` before expecting the publish step to succeed.

## 7. Issue Automation

The workflow `.github/workflows/issue-automation.yml` runs when an issue is opened or edited.

It uses the GitHub CLI and the automatic `GITHUB_TOKEN` to:

- add the `bug` label if the issue mentions "bug"
- add the `help wanted` label if the issue mentions "help"
- comment on newly opened issues

This shows how GitHub Actions can automate project management, not just code testing.

## 8. Migration Notes

Teams often migrate to GitHub Actions from Jenkins, GitLab CI/CD, CircleCI, Travis CI, Azure Pipelines, or Bitbucket Pipelines.

A simple migration approach:

1. Identify the old pipeline triggers.
2. List each old pipeline stage.
3. Convert each stage into a GitHub Actions job or step.
4. Replace old environment variables and secrets with GitHub Actions secrets.
5. Run the workflow on a branch before making it required for `main`.

Example mapping:

| Old CI/CD idea | GitHub Actions equivalent |
| --- | --- |
| Pipeline file | `.github/workflows/*.yml` |
| Build stage | Job |
| Script command | Step with `run:` |
| Plugin/reusable task | Action with `uses:` |
| Secret variable | Repository or organization secret |
| Manual pipeline run | `workflow_dispatch` |

## 9. Suggested Teaching Order

Use this order when presenting the tutorial:

1. Show the Python code and tests.
2. Run tests locally.
3. Explain `.github/workflows/python-ci.yml`.
4. Push the code and show the workflow run.
5. Explain the local composite action.
6. Build the Docker image.
7. Explain package publishing.
8. Show issue automation.
9. Finish with migration concepts.

## 10. What Not To Overcomplicate

For a first tutorial, avoid starting with every GitHub Actions feature. The examples here are enough to teach the foundation and still expose students to real-world automation patterns.

## References Used

This tutorial adapts the essential ideas from these GitHub Docs pages:

- [Creating an example workflow](https://docs.github.com/en/actions/tutorials/create-an-example-workflow)
- [Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Creating a composite action](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action)
- [Publishing Docker images](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images)
- [Adding labels to issues](https://docs.github.com/en/actions/tutorials/manage-your-work/add-labels-to-issues)
- [Manually migrating to GitHub Actions](https://docs.github.com/en/actions/tutorials/migrate-to-github-actions/manual-migrations)
