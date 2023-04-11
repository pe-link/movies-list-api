# Movies List - (API)

API to get the producer with the longest gap between two consecutive awards, and what
got two awards faste.

# Dependencies

- Python ^3.10
- Linux
- Poetry
- Curl

### Install Curl (Http Request)
`apt update && apt install curl`

### Install Poetry
https://python-poetry.org/docs/

# Application
### Enter the main folder of the project: 
- `cd <project_dir>`
## Install dependencies
- `make install`

## Run Application
- `make run`

## Run Tests
- `make run-tests`

```
===================== test session starts ======================
platform linux -- Python 3.10.0, pytest-7.3.0, pluggy-1.0.0 -- /home/tqi_plink/.cache/pypoetry/virtualenvs/movies-list-api-0VPrr73E-py3.10/bin/python
cachedir: .pytest_cache
rootdir: /home/tqi_plink/movies-list-api
configfile: pytest.ini
plugins: json-0.4.0
collected 3 items                                              

tests/test_movies_list.py::test_get_winners_interval PASSED [ 33%]
tests/test_movies_list.py::test_find_interval_range PASSED [ 66%]
tests/test_movies_list.py::test_insert_csv_database PASSED [100%]

====================== 3 passed in 0.78s =======================

```

## Run Lint
- `make lint`

# Requests

- `curl --request GET 'http://localhost:5000/producers/range-winners'`

```json
{
  "max": [
    {
      "followingWin": 2015,
      "interval": 13,
      "previousWin": 2002,
      "producer": "Matthew Vaughn"
    }
  ],
  "min": [
    {
      "followingWin": 1991,
      "interval": 1,
      "previousWin": 1990,
      "producer": "Joel Silver"
    }
  ]
}
```

