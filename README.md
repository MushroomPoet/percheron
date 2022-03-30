# percheron
Command line tool to help with Magic the Gathering Drafting

Requires python (probably 3.0 or greater)

The card data comes from mtgjson.com (AllPrintings.json).
Score and value data is manually extracted from draftsim.com.
Count data is based on my own collection.

To run:
    ./cli

To lint:
    pip3 install pylint # Make sure pylint is on your PATH afterwords
    pylint cli */*.py

To test:
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade Pillow
    python3 -m pip install pytest pytest-cov    # pytest-html-reporter
    pytest -v --cov=. --cov-report html
