# Terminal Command Journal

A working reference of commands used while building and maintaining this
portfolio, plus common commands worth knowing. Grouped by task so it's
searchable later.

---

## Navigation

```bash
pwd                     # print current directory
ls                       # list files in current directory
ls -la                    # list files including hidden ones, with details
cd foldername             # move into a folder
cd ..                      # move up one level
cd ~                        # jump to home directory
cd -                         # jump back to the previous directory
cd ~/Documents                # jump to a specific folder from anywhere
```

Tip: type `cd ` (with a trailing space), then drag a folder from Finder into
the Terminal window — it fills in the full path automatically, avoiding
typos or special characters like `~`.

Tip: typing the start of a filename or folder and pressing **Tab**
autocompletes it — useful for names with spaces or long paths.

---

## Python environment setup

```bash
python3 --version                  # check installed Python version
python3 -m venv vt-env              # create a virtual environment named vt-env
source vt-env/bin/activate           # activate the venv (prompt shows (vt-env))
deactivate                            # exit the venv
```

```bash
pip install requests                 # install a package inside the active venv
pip show requests                     # confirm a package is installed + where
pip --version                          # confirm pip version / location
python3 -m pip install --upgrade pip    # upgrade pip itself
```

Note: a venv is a folder (e.g. `vt-env/`) sitting inside a project directory.
Activating it works from any directory — you don't need to be inside the
venv's folder to use it, only to have run `source .../activate` once in that
terminal session.

---

## Running and checking scripts

```bash
python3 script.py                     # run a script
python3 script.py --dry-run            # run with a custom flag/argument
python3 -m py_compile script.py         # check for syntax errors without running it
wc -l script.py                          # count lines in a file
head -5 script.py                         # preview the first 5 lines
```

---

## Environment variables / secrets

```bash
export VT_API_KEY="your-key-here"        # set an environment variable for this session
echo ${VT_API_KEY:+API key is set}         # confirm it's set, without printing the value
```

Note: `export` only lasts for the current terminal session/window. Closing
the terminal or opening a new tab means it needs to be set again.

**Never** paste a real key value into chat, commit messages, or scripts.
Scripts should read secrets via `os.getenv("VAR_NAME")`, never hardcode them.

---

## Searching files

```bash
grep "text" file.py                       # search for a string in a file
grep -i "text" file.py                      # case-insensitive search
grep -r "text" .                             # search recursively from current folder
grep -r "text" . --exclude-dir=vt-env          # search but skip a specific folder
grep -rE "[0-9a-f]{64}" . --exclude-dir=vt-env   # search using a regex pattern
```

Used this repeatedly to confirm no API key was hardcoded anywhere in the repo
before committing.

---

## Editing files (nano)

```bash
nano filename.md          # open a file in the nano editor
```

Inside nano:
- `Ctrl + O` then `Return` — save (write out)
- `Ctrl + X` — exit
- If there are unsaved changes on exit, nano asks `Save modified buffer?` —
  press `Y` then `Return` to save and exit in one step

---

## Moving / renaming files

```bash
mv oldname.png newname.png                 # rename a file
mv file.py ~/Downloads/soc-portfolio/         # move a file into a folder
mv "file with spaces.png" no-spaces.png        # quote filenames containing spaces
```

Tip: for filenames with spaces or odd characters, type the first part of the
name and press **Tab** to autocomplete rather than retyping it — avoids
"No such file or directory" errors from a mistyped name.

---

## Git — day-to-day

```bash
git status                     # see staged / unstaged / untracked changes
git pull                        # bring in remote changes before pushing
git add file1 file2               # stage specific files
git add .                          # stage everything in the current folder
git commit -m "message"              # commit staged changes with a message
git push                              # push commits to the remote
git push -v                            # push with verbose output
git log --oneline -5                    # view the last 5 commits, condensed
```

## Git — remote / auth

```bash
git remote set-url origin git@github.com:username/repo.git   # switch remote to SSH
ssh-keygen -t ed25519 -C "you@example.com"                     # generate an SSH key
pbcopy < ~/.ssh/id_ed25519.pub                                   # copy public key to clipboard
git config --global credential.helper osxkeychain                 # cache HTTPS credentials in Keychain
```

Note: GitHub no longer accepts account passwords for git operations over
HTTPS. Use a Personal Access Token as the password, or switch to SSH.

## Git — checking a diff between two files

```bash
diff file1 file2         # show line-by-line differences between two files
```

Used this to compare a stray `README` file against the real `README.md`
before deleting the wrong one.

---

## .gitignore basics

```bash
echo "vt-env/" >> .gitignore      # add a line to .gitignore (creates it if missing)
echo "*.csv" >> .gitignore
cat .gitignore                     # view current contents
```

---

## Homebrew (package installer for macOS)

```bash
brew install --cask github-desktop     # install a GUI app via Homebrew
```

---

## Commands I'll likely need later

```bash
chmod +x script.py              # make a script executable
./script.py                       # run an executable script directly
history                            # view recent command history
history | grep keyword               # search command history
clear                                 # clear the terminal screen
man command_name                       # view the manual page for a command
curl -I https://example.com              # check response headers from a URL
top                                        # view running processes / resource usage
df -h                                        # check disk space, human-readable
```

---

## Lessons tied to specific mistakes

- **`wc -1` vs `wc -l`** — the flag is a lowercase L (`-l` for "lines"), not
  the number one. Typing `-1` throws `illegal option`.
- **Curly quotes from pasted text** — content copied from Google Docs or
  similar can silently swap straight quotes (`"`) for curly ones (`"` `"`),
  breaking Python syntax. Worth checking with `head` after pasting code from
  a non-plain-text source.
- **Hidden file extensions** — Finder can hide `.txt`, so a manual rename can
  leave a file as `name.py.txt` without it being obvious. `ls` in Terminal
  always shows the real, full filename.
