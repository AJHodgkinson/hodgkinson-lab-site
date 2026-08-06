# Hodgkinson Lab website

A rebuild of hodgkinsonlab.org as a plain static site — no Wix, no
subscription. Content lives in small, editable data files; a build script
turns them into the HTML that actually gets hosted.

```
hodgkinson-lab-site/
├── data/                  ← EDIT THESE to change content
│   ├── site.yml           (nav, tagline, footer, social links)
│   ├── people.yml         (current group members)
│   ├── alumni.yml         (lab alumni)
│   ├── publications.yml   (papers, newest first)
│   └── software.yml       (software/tools list)
├── templates/             HTML page templates (Jinja2) — rarely need editing
├── assets/                CSS, JS, images, favicon
│   └── images/people/     put headshot photos here (see README.txt inside)
├── build.py               generates the finished site into docs/
├── docs/                  the built, ready-to-host site (generated — don't
│                          hand-edit files in here, they get overwritten)
└── .github/workflows/     auto-build + deploy to GitHub Pages on push
```

## Adding or editing content

You don't need to touch HTML for routine updates:

- **New person joins the lab** → add a block to `data/people.yml`
- **Someone leaves** → cut their block from `people.yml`, paste it into `alumni.yml`
- **New publication** → add a block to the *top* of `data/publications.yml`
- **New software release** → add a block to `data/software.yml`
- **Change the tagline, nav, or footer** → edit `data/site.yml`

Each file has comments showing the format — copy an existing block and edit it.

## Previewing changes locally

```bash
pip install -r requirements.txt
python3 build.py
```

Then open `docs/index.html` in a browser. Re-run `python3 build.py` any time
you edit a file in `data/` to regenerate the site.

## Deploying (free, via GitHub Pages)

**1. Create a GitHub account** if you don't have one (free) at github.com.

**2. Create a new repository**, e.g. `hodgkinson-lab-site`. Keep it public
(GitHub Pages is free for public repos; it's also free for private repos on
most plans, but public is simplest).

**3. Push this folder to it:**

```bash
cd hodgkinson-lab-site
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/hodgkinson-lab-site.git
git push -u origin main
```

**4. Turn on GitHub Pages:**
- Go to the repo's **Settings → Pages**
- Under "Build and deployment", set **Source** to **GitHub Actions**
  (the workflow in `.github/workflows/deploy.yml` is already set up — it
  will build the site with `build.py` and deploy it automatically on every
  push to `main`)
- Wait a minute for the first deploy, then check the **Actions** tab for a
  green checkmark

At this point your site is live at `https://YOUR-USERNAME.github.io/hodgkinson-lab-site/`.
The next steps point your existing domain at it instead.

**5. Add your custom domain in GitHub:**
- Still in **Settings → Pages**, under "Custom domain" enter:
  `www.hodgkinsonlab.org`
- GitHub will commit a `CNAME` file for you (the build script also generates
  one automatically, so this stays correct on future deploys)

**6. Point the domain at GitHub in GoDaddy's DNS settings:**
- Log into GoDaddy → **My Products** → find `hodgkinsonlab.org` → **DNS** / **Manage DNS**
- Add/edit these records (delete any conflicting old Wix records for the
  same names first):

  | Type  | Name | Value                  |
  |-------|------|------------------------|
  | CNAME | www  | YOUR-USERNAME.github.io |
  | A     | @    | 185.199.108.153        |
  | A     | @    | 185.199.109.153        |
  | A     | @    | 185.199.110.153        |
  | A     | @    | 185.199.111.153        |

  (The four `A` records make the bare `hodgkinsonlab.org`, without `www`,
  also work and redirect to `www`. These are GitHub Pages' standard IP
  addresses.)

- DNS changes can take anywhere from a few minutes to ~24 hours to propagate.
- Back in GitHub **Settings → Pages**, once DNS has propagated, tick
  **Enforce HTTPS** (GitHub issues a free SSL certificate automatically —
  give it a little time after DNS propagates).

Your domain stays registered with GoDaddy exactly as before — you're only
changing where it *points*, not who it's registered through. You keep paying
GoDaddy's normal renewal fee for the domain; the Wix subscription is what
goes away.

## If you'd rather use Netlify or Cloudflare Pages instead

The `docs/` folder produced by `build.py` is a plain static site, so it works
identically on any static host, not just GitHub Pages:

- **Netlify** / **Cloudflare Pages**: connect your GitHub repo, set the
  build command to `pip install -r requirements.txt && python3 build.py`
  and the publish directory to `docs`. Both offer free custom-domain
  support with similarly simple DNS instructions.

## Adding the real photos

The People page currently shows placeholder circles instead of photos —
see `assets/images/people/README.txt` for direct links to the current
headshots on the old site, and the exact filenames to save them as.
