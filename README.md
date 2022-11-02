# eInk Radiator

The eInk Radiator is a [project of mine](https://petewall.net/tag/eink-radiator/), designed around the [Inky wHAT](https://shop.pimoroni.com/products/inky-what) eInk screen from [Pimoroni](https://shop.pimoroni.com/), to "radiate" various information on a schedule.

This repository contains the main orchestrator and an administative user interface. It also uses several other repositories:

## Display

The [https://github.com/petewall/eink-radiator-display](display) repo controls how to display a slide to the eInk screen

## Image Sources

These repositories are small, self-contained tools for generating images:

* [Blank](https://github.com/petewall/eink-radiator-image-source-blank) - Creates a blank, single-color image
* Concourse - (TBD) Creates a slide based on a [Concourse](https://concourse-ci.org/) pipeline(s)
* Grafana Widget - (TBD) Display a Grafana-rendered dashboard widget, based on [this video](https://www.youtube.com/watch?v=AEQhsWX4v78)
* [Image](https://github.com/petewall/eink-radiator-image-source-image) - Resizes or crops an image from a URL
* Images - (TBD) Creates a slide from a set of images at random
* [QR Code](https://github.com/petewall/eink-radiator-image-source-qrcode) - (In development) Creates a QR Code
* Stocks - (TBD) Creates a slide showing stock information
* Text - (TBD) Creates a slide based on text
* Weather - (TBD) Creates a slide showing weather data

## User Interface

When running, the eInk Radiator starts a server where the slides can be managed. This UI interacts via an HTTP API:

### HTTP API

* `POST /api/next` - Go to the next slide
* `POST /api/prev` - Go to the previous slide
* `GET /api/screen/config.json` - Gets the configuration of the screen.
* `GET /api/screen/image.png` - Gets the current image on the screen.
* `GET /api/slides.json` - Get the list of slides
* `GET /api/slide/<name>/config.json` - Get the configuration for this slide
* `GET /api/slide/<name>/image.png` - Get the image for this slide
* `POST /api/slide/<name>/activate` - Make this slide active

#### TODO: Add API calls for adding/rearranging/deleting slides
#### TODO: Add API calls for changing slide configuration and previewing slides
