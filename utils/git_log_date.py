import shlex
import subprocess

def git_log_date(filepath, post, branch: str="origin/master", message: str=""):
    """
    The Git log Command Ran as a Subprocess to Pull date information from history.
    git log -b [branch] --format="[string] %ad" -- [filepath] | [head/tail] -1
    ------
    - filepath (Path or str) - the filepath of the document
    - post (str: Either 'head' or 'tail') tells to get either the first (Creation) or the Last(Modification)
    - branch (str: default='origin/master') filters results to only include the specified branch. Remove '-b' if None
    - message (str: message before the preformated date

    The results of this command can be given to maya or datetime.strptime as the format is Mon, Jan 01, 2019 19:00 -0800
    """

    if branch:
        branch = f'-b {branch}'
    else:
        branch = ''

    if post in ('head', 'tail'):
        command = f'git log {branch} --format="{message} %ad" -- {filepath} | {post} -1'
        return subprocess.run(shlex.split(command))

    else:
        raise CommandError('post must be "head" or "tail"')
