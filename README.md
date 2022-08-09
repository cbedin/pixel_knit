This is a small Flask app that creates low-resolution images for needle arts. It's specifically designed with knitting in mind, but can be used for anything!

After cloning, it can be run locally like any Flask app. The goal is to collect any image from a user and do two things:

* Reduce the total number of colors, to allow a project to be rendered in a limited number of yarn colors

* Reduce the resolution of the image, to account for the decreased resolution of needle arts

This is accomplished through simple k-means clustering