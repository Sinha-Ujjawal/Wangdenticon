![](images/wangdenticon.png)

## Wangdenticon

Inspired by [Github's identicons](https://github.blog/2013-08-14-identicons/) and [tsoding wang-tiles](https://github.com/tsoding/wang-tiles) created a project to generate "Wangdenticon"

## Getting Started

You need [python 3.7.6](https://www.python.org/downloads/release/python-376/) or higher to run the scripts

1. Install dependencies

```sh
pip install -r requirements.txt
```

2. Usage

```python
from wangdenticon import make_wangdenticon

YOUR_SIZE = 255
GRIDSIZE = 6 # 6 is recommended
BGCOLOR = (0, 0, 0)

# will create a (YOUR_SIZE x YOUR_SIZE) Pillow Image
img = make_wangdenticon(
    name="YOUR NAME",
    size=YOUR_SIZE,
    gridsize=GRIDSIZE,
    bgcolor=BGCOLOR,
    invert=False,
)
img.show()
```

![](images/example.png)

## Licence

Licensed under [MIT](LICENSE)
