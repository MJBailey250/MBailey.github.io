# Michael Bailey portfolio starter

A template-driven static site. Edit `site_content.json` or use `portfolio_update.ipynb`, then build with Python.

## Build locally

```bash
python build_site.py
```

Generated pages are written to `site/`: homepage, About, Projects, project detail pages, Notes, and Contact. Page templates live in `templates/`; shared styles live in `assets/site.css`.

## Notebook workflow

Open `portfolio_update.ipynb` in VS Code with the Jupyter extension and a Python 3 kernel. Edit the first cell, then run all cells. Replace the sample content with your real bio, projects, notes, email, and profile links.

To publish, copy the contents of `site/` into the root of your GitHub Pages repository, then commit and push. Keep the generated `assets/` and `projects/` directories.
