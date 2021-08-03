#! /bin/bash
# Build lambda zip release package
# https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

# Usage: ./build-package.sh

PYTHON=python3.8

TMPDIR=`mktemp -d`

rm -rf .venv build_lambda

virtualenv .venv
source .venv/bin/activate
pip3 install --prefix $TMPDIR -r requirements.in
deactivate

mv $TMPDIR/lib/$PYTHON/site-packages build_lambda
cp -r qualys_rss.py build_lambda
rm -rf build_lambda/pycparser*

rm -rf .venv
rm -rf $TMPDIR

cd build_lambda
zip -Xr9 ../qualys_rss.zip .
cd ..
rm -rf build_lambda
