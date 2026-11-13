# Tennis Career Package

A Python package that retrieves and cleans tennis career match data from Tennis Abstract and plots player age against the age difference between the player and opponent.

## Install

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-sunyonglee1.git
```

## Usage

```python
from tennis_package import get_player_data, plot_age_matches
import matplotlib.pyplot as plt

serena = get_player_data("Serena Williams")
figure = plot_age_matches(serena)
plt.show()

nadal = get_player_data("Rafael Nadal")
figure = plot_age_matches(nadal)
plt.show()
```

`get_player_data()` returns a pandas DataFrame with match date, tournament, surface, result, opponent, both players’ ages, and age difference. Unknown player names raise a `ValueError`.

## Tests

Run the tests with:

```bash
python -m pytest -q
```

The tests use mock data and do not contact Tennis Abstract.