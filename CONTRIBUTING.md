# How to Contribute

Thank you for reading this contribution guide and to have interest to django boost!

We’re still working out the kinks to make contributing to this project as easy and transparent as possible, but we’re not quite there yet. Hopefully this document makes the process for contributing clear and answers some questions that you may have.

## Code of Conduct

Facebook has adopted the Contributor Covenant as its [Code of Conduct](./CODE_OF_CONDUCT.md), and we expect project participants to adhere to it. Please read [the full text](./CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.

## Development

All work on React happens directly on GitHub.

We welcome any trivial contributions!

## Setup Development Environment

1. Clone the latest code.

```bash
$ git clone https://github.com/ChanTsune/django-boost.git
```

2. Install the necessary libraries for development.

```bash
$ cd django_boost
$ pip install -r requirements/develop.txt
```

## Testing

```bash
$ python manage.py test
```

## Code format

This project uses PEP8 as the format for the code.
It is recommended to use autopep8.

## Development Flow

This project uses a development flow based on GitHub flow.

### Issue

In principle, all work is done in association with an issue.  
Deviations from the principles include

- Correcting translation errors
- Typo fixes
- code format
- Experimental Implementation

### Branch

All branches are derived from the master.
Each implementation is done in a `feature/[working name]` branch.
For urgent fixes, a hotfix branch is created and used to do the work there. This brand will be merged into master as soon as we are sure the problem is solved.
In preparation for the release, a release/version branch will be created and the work required for the release, including updating the version number, will be done.
It is expected that the branch name will be numbered at the end of the branch name to indicate which issue it relates to.

### Marge

In this project, branch will be rebase and add to base branch.  
The following are some of the things that deviate from the principle.  

- When a large file (several MB) that is not used at the time of the latest commit is committed

### Pull Request

When you're done, send out a pull request to the master branch of this project.
When you make a pull request, you want to have the latest master branch merged with the one just before you made the pull request.
The code will be merged into this project once it has been reviewed and the pull request has been approved.
**Before submitting a pull request,** please make sure the following is done:

1. Fork the repository and create your branch from master.
1. Run `pip install requirements/develop.txt` in the repository root.
1. If you’ve fixed a bug or added code that should be tested, add tests!
1. Ensure the test suite passes (`python manage.py test`).
1. Format your code with pep8.
1. Make sure your code lints (`tox`).

## Contribute

### Code

Contributions to unresolved issues and bug fixes.

### Document

Typo corrections to the document.
Sample codes.
Clearer wording of the document.

### Translation

Contribution to a better translation.

Special thanks for your contribution in correcting errors in the translation into English, as the main administrator of the project is not a native English speaker.

### Feature Request

This includes suggestions for the implementation of this project and suggestions for operationalizing the project.

### Bug Report

This is a report of a bug you discovered.

It doesn't matter how trivial it is. Is it a bug? If you think you have a problem, please don't hesitate to report it.

We'll check in as soon as possible and work to fix the problem.

This project will be better with a report from you!
This contribution guide is for anyone who doesn't know how to contribute to this project. We are not necessarily required to make contributions in the form of this guide.
We are happy to accept any contributions that do not violate the Code of Contract.

## License

By contributing to Django-Boost, you agree that your contributions will be licensed under its MIT license.

Thank you for your Contribution ❤️
