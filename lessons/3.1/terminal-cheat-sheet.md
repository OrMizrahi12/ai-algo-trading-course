# Terminal cheat sheet: Linux, macOS and Windows PowerShell

The lesson was filmed on Linux. macOS Terminal uses the same commands. Windows PowerShell understands almost all of
the same short names (they are built-in aliases of its own commands), with the differences marked below.

## Open a terminal

| System | How |
|---|---|
| Linux (Ubuntu and similar) | Applications menu → **Terminal** (or Ctrl+Alt+T on many systems) |
| macOS | **Applications → Utilities → Terminal** (or Cmd+Space, type `Terminal`) |
| Windows | Start menu → type **PowerShell** → open **Windows PowerShell** (or **Terminal** on Windows 11) |

## Read the prompt

| System | Typical prompt | What it says |
|---|---|---|
| Linux | `you@computer:~$` | user name, computer name, current folder (`~` = home), `$` = your turn |
| macOS | `you@MacBook ~ %` | user name, computer name, current folder, `%` = your turn |
| Windows PowerShell | `PS C:\Users\you>` | PowerShell, then the current folder, `>` = your turn |

## The ten commands

| What it does | Linux and macOS | Windows PowerShell |
|---|---|---|
| Where am I? (print working directory) | `pwd` | `pwd` |
| What's here? (list) | `ls` | `ls` (or `dir`) |
| List another folder | `ls Downloads` | `ls Downloads` |
| Go into a folder (change directory) | `cd Downloads` | `cd Downloads` |
| Go up one level | `cd ..` | `cd ..` |
| Go home | `cd ~` | `cd ~` |
| Make a folder | `mkdir practice` | `mkdir practice` |
| Make an empty file | `touch notes.txt` | `New-Item notes.txt` (`touch` does **not** exist) |
| Write text into a file (replaces it) | `echo 'Plan the trade, trade the plan.' > notes.txt` | the same line works; `Set-Content notes.txt 'Plan the trade, trade the plan.'` also does it |
| Add a line to the end of a file | `echo 'Risk small, learn fast.' >> notes.txt` | the same line works (or `Add-Content notes.txt '...'`) |
| Show what's in a file | `cat notes.txt` | `cat notes.txt` |
| Copy a file | `cp notes.txt backup.txt` | `cp notes.txt backup.txt` |
| Rename (or move) a file | `mv backup.txt old-notes.txt` | `mv backup.txt old-notes.txt` |
| Move a file into a folder | `mv old-notes.txt practice` | `mv old-notes.txt practice` |
| Delete a file, for good | `rm old-notes.txt` | `rm old-notes.txt` |
| Clean the screen (files stay) | `clear` | `clear` (or `cls`) |
| Open this folder in VS Code | `code .` | `code .` |

`rm` skips the Trash / Recycle Bin on every system: there is no undo.

On Windows PowerShell 5.1 (the one built into Windows 10 and 11), `echo ... > file` saves the file as UTF-16 text. Most
editors, VS Code included, read it fine. If a tool ever complains, use `Set-Content` instead.

## Speed tricks

| Trick | Linux and macOS | Windows PowerShell |
|---|---|---|
| Finish a name | Type the first letters, press **Tab** | Same; pressing Tab again cycles through the matches |
| See all matches | Press **Tab** twice | **Ctrl+Space** |
| Previous commands | **Up arrow** (again for older ones), Enter runs it | Same |
| Cancel the current line or stop a running command | **Ctrl+C** | **Ctrl+C** |

## Paths

- A **relative** path starts from where you are: `practice`, `Downloads/notes.txt`, `..` (the folder above).
- An **absolute** path starts from the top, so it works from anywhere:
  - Linux: `/home/you/practice`
  - macOS: `/Users/you/practice`
  - Windows: `C:\Users\you\practice` (PowerShell also accepts forward slashes)
- `~` means your home folder on all three.
- Type names exactly as they appear, capital letters included. Linux treats `Downloads` and `downloads` as different
  names. If a name has a space in it, put it in quotes: `cd 'My Folder'`.
