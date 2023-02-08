# Using S3 and AWS CloudFront for Docusaurus previews

Having previews of documentation changes submitted as pull requests
is important to encourage doc contributions.  Although Docusaurus 
itself is very easy to run, some environments have markdown files
spread out over multiple GitHub repos, and combining these when
making a change in one repo is an unnecessary burden for the doc
contributor.  The GitHub workflow in this demo repo provides a 
method for publishing previews in S3 and serving those with CloudFront.

Although this demo repo does not use markdown files spread out over multiple
repos, this [will be added](https://github.com/DanRoscigno/preview/issues/13).

## Docusaurus config changes

The config file is `docusaurus.config.js` and in there we need to 
modify the `baseURL` for each pull request so that we can write to 
a separate folder in the S3 bucket for each PR.  To do this we will
set an environment var `DOSSIER_BASE_URL` (the name was given by
[Daniel Cousineau](https://gist.github.com/dcousineau-godaddy) in
his [gist](https://gist.github.com/dcousineau-godaddy/9072b10bccc09705572423c56c8c5671)
which he generously posted in the Docusaurus discord).

So, at the top of the config file is where I define my constants
and this is what I have:

```js
const BASE_URL = process.env.DOSSIER_BASE_URL || '/';
```

This var, `BASE_URL` then gets used to set the `baseURL`:

```js
  baseUrl: BASE_URL,
```

## GitHub workflow

To get the name of the PR to use it as the folder name and baseURL:

```yml
      - name: Setup Environment
        run: |
          export PREVIEW_BRANCH_DIR=$(echo $GITHUB_HEAD_REF | sed -e 's#^refs/heads/##; s#[^0-9a-zA-Z-]#-#g')
          echo "PREVIEW_BRANCH_DIR=$PREVIEW_BRANCH_DIR" >> $GITHUB_ENV
```

You will also need the PR number to add a comment to the PR with the URL, so
pop that into the environment also.  This is then the full section:

```yml
      - name: Setup Environment
        run: |
          export PREVIEW_BRANCH_DIR=$(echo $GITHUB_HEAD_REF | sed -e 's#^refs/heads/##; s#[^0-9a-zA-Z-]#-#g')
          echo "PREVIEW_BRANCH_DIR=$PREVIEW_BRANCH_DIR" >> $GITHUB_ENV
          export PR_NUMBER=$(echo $GITHUB_REF | awk 'BEGIN { FS = "/" } ; { print $3 }')
          echo "PR_NUMBER=$PR_NUMBER" >> $GITHUB_ENV      
```

This website is built using [Docusaurus 2](https://docusaurus.io/), a modern static website generator.

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

Using SSH:

```
$ USE_SSH=true yarn deploy
```

Not using SSH:

```
$ GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
