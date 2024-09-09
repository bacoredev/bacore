"""Set functionality module."""

import subprocess as sup
from pathlib import Path
from pydantic import validate_call


@validate_call
def git_repository(
    repo: Path, remote: str, commit_msg: str, branch: str = "main", rebase: bool = False
) -> None:
    """Push latest changes in repository to remote.

    All the current edits are added and committed with the specified commit message.

    Args:
      repo: Path to the repository
      remote: Remote repository
      commit_msg: The commit message for the commit.
      branch: Branch to commit. Defaults to "master".
      rebase: If rebasing should be done when pulling. Default is False.
    """
    sup.run(["git", "-C", repo, "add", "-A"])
    sup.run(["git", "-C", repo, "commit", "-m", commit_msg])
    if rebase:
        sup.run(["git", "-C", repo, "pull", "--rebase"])
    sup.run(["git", "-C", repo, "push", remote, branch])
