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

## HTTP Request

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

## Run Tests
- `make run-tests`

```
========================================= test session starts ==========================================
platform linux -- Python 3.10.0, pytest-7.3.0, pluggy-1.0.0 -- /home/tqi_plink/.cache/pypoetry/virtualenvs/movies-list-api-0VPrr73E-py3.10/bin/python
cachedir: .pytest_cache
rootdir: /home/tqi_plink/movies-list-api
configfile: pytest.ini
plugins: json-0.4.0
collected 5 items                                                                                      

tests/test_movies_list.py::test_get_winners_interval_api PASSED                                  [ 20%]
tests/test_movies_list.py::test_find_interval_range PASSED                                       [ 40%]
tests/test_movies_list.py::test_insert_csv_database PASSED                                       [ 60%]
tests/test_movies_list.py::test_find_interval_range_max_and_min_intervals PASSED                 [ 80%]
tests/test_movies_list.py::test_mock_consecutive_wins_min_and_max_intervals PASSED               [100%]

========================================== 5 passed in 0.76s ===========================================


```

## Run Lint
- `make lint`
