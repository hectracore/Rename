The user points out that during the `/r` (rename) flow, when selecting a destination folder for a Series (or movie), they expect a button for "Automatic Assignment" (auto-create/auto-assign to its own folder) like it was originally planned.
This button would automatically assign the file to a folder named after the media (e.g. `title` from metadata).
If the folder doesn't exist, it should be created (or implicitly resolved during processing).

Wait! How would it work? If the user clicks `Auto-Assign`, what happens?
If `dest_folder` is set to `"auto"`, the processing script (in `process.py`) should handle creating the folder if it doesn't exist, or assigning to an existing one.
Let's see how `process.py` handles `dest_folder`.
