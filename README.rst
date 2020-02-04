Pubiç, a tough client for Hubic
===============================

Pubiç provides a way to synchronize local data with your Hubic account.

Pubiç is the meeting of Python and Hubic. It is basically the same thing as
the official Hubic Linux client from OVH, except for one hair: Pubiç is
expected to be faster and much smaller than the original client which
originaly comes with mono. Features stay the same (at this time!).

Unlike the official Linux client from OVH, Pubiç is made to be

- light
- simple
- fast
- reliable


Features
--------

At this early development stage it only supports:

- authentication against Hubic services
- listing your Hubic containers and backups
- list your files stored in the main Hubic container
- search for a file/directory name pattern

It will soon provide:

- a fast and reliable way to download files
- a daemon mode to keep a folder synced with your Hubic cloud storage

Extra features that are not available in the official client will soon come:

- local sync folders setup wizard (no more way to declare an empty folder as
  syncing folder and loose everything in the cloud!)
- ability to manage and create backups


Install
-------

Requirements :

- probably creating an app key in your Hubic account
- Python 3.7 (backward compatibility will be considered later)
