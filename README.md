# lumendb-explore

Exploring the [Lumen Database](https://lumendatabase.org/) for a [CSE291B Project](https://cseweb.ucsd.edu/classes/sp23/cse291-b/).

## Installation
Create a virtual environment and enter it:

```
python -m venv venv && source venv/bin/activate
```

Install dependencies. If you are using Python 3.11, use
```
python -m pip install -r requirements.txt
```
If you are not, install
```
python -m pip install -r requirements3.10.txt
```

Create a file named `.env` with the contents
```
LUMEN_API={api key here}
```

## Usage
You'll need to run `source venv/bin/activate` every time when using this repo.

You can now run the example script with
```
python basictest.py
```
