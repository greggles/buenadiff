This tool was created to track and identify changes made to the text of web pages. This could be useful for a variety of situations. The original motivation was to support a site with multiple editors that provides professional translations via a 3rd party service.

## How it fits in a translation workflow:
A member of the website team uses this tool to periodically check for text changes on web pages. They copy out the differences (diffs) identified by this tool to a document and decide how to handle them.

* Some diffs like updating a year can be made by the internal team.
* If a block of text is moved on the page then the internal team can move the block of language in the translated language.
* If a bunch of changes are made throughout a section or the whole document, consider having the translation team re-translate that section or the whole document.

At the point where they copy the translations out of the diff report they should also create a new "reference" point. From that point on, the website manager should work to fix all the changes identified to keep the pages in-sync. The script in this tool only tracks changes between one reference point.

## Setting up this system the first time:
Follow these steps the first time only.

1. Copy the settings example to your own copy `cp url_data.example.csv url_data.csv`
2. Modify the url_data.csv to contain your data.
  * The filename (2nd column) must be unique.
  * The XPATH (3rd column) is a xpath to focus the scope of what to compare. Xpath supports "or" conditions to diff multiple elements.
3. Run `./curler.sh` to download copies of the files to the `working-copy` directory.
4. Copy (or move) all the html files from `working-copy` to `reference`
5. Stage and commit the html files in the `reference` directory and push it to GitHub

## Adding a new URL to be tracked:
The "diff" step will fail after a new row has been added to `url_data.csv`. You must create the reference copy of that file.

You can do this by manually running curl, e.g.
```commandline
curl https://example.com/url-you-added -o reference/filename.html
```

Or if you are adding a lot of new html files you can use the `curler.sh` script and manually move the files over, e.g.
```commandline
  ./curler.sh url_data.csv
  cp working-copy/*.html reference/
```

## Running the analysis using GitHub Actions

1. Click to "Actions"
2. Click "Run workflow" choosing to "compare"
3. Review the diff - if there are changes you are handling you can create a new reference point
4. Click "Run workflow" choosing to "create_reference"

## Folder structure:
* `reference/` is the historical copy of the site that is in a specific state.
* `working-copy/` is for the latest version of each page.

## Digging into history (advanced optional usage)
Pages are "committed" with each run of the tool in the working-copy directory. While not supported via the Actions, it is possible to dig into the history of the files in git to compare changes.

Consider scheduling runs regularly by modifying the `.github/workflows/CHANGETHIS.yml` and adding a `schedule` trigger at a frequency like daily:

```commandline
on:
  schedule:
    # Daily at 5:30 in UTC.
    - cron: '30 5 * * *'
```


TODO:
1. Track HTML changes in the Xpath. If a link or a font treatment changes on one page that fact needs to be updated in the other language.