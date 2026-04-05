Look at this code in `plugins/process.py`:
```python
                if not dest_folder and not skip_myfiles:
                    if self.tmdb_id:
                        folder_type = "series" if self.media_type == "series" else "movies"
                        folder = await db.folders.find_one({"user_id": self.user_id, "tmdb_id": self.tmdb_id})
                        if not folder:
                            res = await db.folders.insert_one({
                                "user_id": self.user_id,
                                "name": self.title,
                                "type": folder_type,
                                "tmdb_id": self.tmdb_id,
                                "created_at": datetime.datetime.utcnow()
                            })
                            folder_id = res.inserted_id
                        else:
                            folder_id = folder["_id"]
```
Wait!
If `dest_folder` is NOT set (`None`), it AUTOMATICALLY assigns it to a folder based on `tmdb_id`!
BUT wait! In `plugins/flow.py`:
When building the destination menu, there is no button for "Auto-Assign"!
And if the user clicks NOTHING? They can't, it's a mandatory step in the flow!
Ah!!
If they click "Save to MyFiles (Root)", `dest_folder` is `"root"`.
If they click "Don't save to MyFiles", `dest_folder` is `"none"`.
If they click a specific folder, `dest_folder` is the `ObjectId` string.
If they create a new folder, it sets it to the new `ObjectId` string.
So `dest_folder` is ALWAYS set! It is NEVER `None` because the user must click a button to proceed!
This means the automatic assignment code (`if not dest_folder and not skip_myfiles`) is NEVER EXECUTED!!!
Because there is no button to pass `dest_folder=None` (or `"auto"`)!
The user wants a button for "Automatic Assignment" so that it creates/uses its own folder (like it was originally planned).
So I just need to add an "🤖 Auto-Assign Folder" button to the Destination Folder menu, which sets `dest_folder` to `"auto"`.
And update `process.py`:
```python
                if (not dest_folder or dest_folder == "auto") and not skip_myfiles:
```
