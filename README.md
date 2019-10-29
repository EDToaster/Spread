# Spread

Spread is a versatile multi-monitor wallpaper cropper. It supports up to infinity monitors, so long as you can define the coordinates of each monitor in your config file!

## Configuration

You can change the settings to match your monitor positions and sizes in `config.json`.

### config.json

`image`: input wallpaper image

`monitors`: list of `monitor` objects

### `monitor` Object

Each monitor object has the following attributes:

`name`: name of the monitor (refers to image output name)

`dimensions`: `[x, y, width, height]` of the monitor

## Usage

Put your image in the path specified in `config.json`, then run the script using `python spread.py`. The generated images will be saved in the `out` folder. 

## Demo

![Original](/assets/Orig.jpg)
![Demo](/assets/Demo.png)
