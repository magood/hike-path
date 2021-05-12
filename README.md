Hiking Paths Over DEMs as Graphs.

Readme in progress


Considering using GDAL:
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt update
sudo apt install python-numpy gdal-bin libgdal-dev

...because a lot of other python tools use it.


Some notes on the data:
3DEP - USGS 1/3 Arc Second
U.S. Geological Survey, 20210312, USGS 1/3 Arc Second n40w108 20210312: U.S. Geological Survey.
https://www.usgs.gov/faqs/what-are-projection-horizontal-and-vertical-datum-and-resolution-3d-elevation-program-3dep?qt-news_science_products=0#qt-news_science_products
All 3DEP seamless DEMs are provided in geographic coordinates (longitude and latitude) in units of decimal degrees, horizontally referenced on the North American Datum of 1983 (NAD83). All elevation values are in units of meters, typically referenced to the North American Vertical Datum of 1988 (NAVD88), although the National Geodetic Vertical Datum of 1929 (NGVD29) and local reference datums are used in some areas outside of the conterminous United States (CONUS).
#1/3 arcsecond is said to be ~10m per pixel, and so for now we'll go with that.  Precision isn't key here.