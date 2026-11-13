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

## Personal Reflections

This assignment taught me how to turn a one-time data analysis into a reusable Python package. I learned to handle the differences between women’s and men’s career files, especially how opponent ages are represented. I also used mock data to test the cleaning functions without relying on a live server. During integration, Tennis Abstract returned a 403 error in DataHub, which helped me distinguish a code issue from a limitation in accessing an external website.