import pyqrcode

a = pyqrcode.create("this is a test")
a.png("test.png", scale=8)


def generate_url(protocol, options) -> dict:

    #

    return {
        "url": "",
        "image": "path/to/image"
    }

