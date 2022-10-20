# eInk Radiator

This is the main project for a small screen radiator project, designed around the [Inky wHAT](https://shop.pimoroni.com/products/inky-what) eInk screen from [Pimoroni](https://shop.pimoroni.com/).

## HTTP API

This project starts an HTTP interface.

* `POST /api/next` - Go to the next slide
* `POST /api/prev` - Go to the previous slide
* `GET /api/screen/config.json` - Gets the configuration of the screen.
* `GET /api/screen/image.png` - Gets the current image on the screen.
* `GET /api/slides.json` - Get the list of slides
* `GET /api/slide/<name>/config.json` - Get the configuration for this slide
* `GET /api/slide/<name>/image.png` - Get the image for this slide
* `POST /api/slide/<name>/activate` - Make this slide active
