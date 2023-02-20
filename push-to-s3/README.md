
I don't do Python because I never know what version of what
works with which python code.  This is me trying a virtual
env.

The Python is in `preview-build.py`

### Setup the virtual env
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install boto3
python3 -m pip freeze > requirements.txt
```

### Build docs
```bash
export DOSSIER_BASE_URL=43 # This should be the PR number
yarn build
```

### Copy in the build dir

### Environment vars
export AWS_S3_KEY_ID=AKIAXXXXXXXXXXXXXXXX
export AWS_S3_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export DOSSIER_BASE_URL=43
export AWS_S3_BUCKET=doc-pr-preview
```


python3 -m preview-build
```
