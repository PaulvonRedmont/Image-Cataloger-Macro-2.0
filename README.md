# Image-Cataloger-Macro

I've spent the last few summers photocopying and cataloging academic books and journals for a professor at a nearby university. To speed up the rather tedious job of cataloging, I hastily wrote up this script over a weekend and used it to expedite the task of cataloging the scanned books and articles.

The primary functionality of this script is as a macro of sorts. The user will select the leading image of a book (typically the front cover matter) in Windows File Manager (that is, click on it, such that the image is highlighted in blue), and then press "1", which will trigger the script to use the shortcut CTR+SHIFT+C to copy the image's file path via `pyautogui`. The file path will then be put through the tesseract engine via `pytesseract` after being resized to increase OCR accuracy, and the results saved to a text document. My method for cataloging books was to write down the image file path of a book's front cover as well as the name of the corresponding book, so the scanned material could be easily located by future users. This method drastically decreases the amount of time needed to catalog a single book from about 2 minutes to less than 20 seconds (including the time it takes for OCR to correctly scan the title page).

UPDATE 7/17/24:

I've also added a feature that will copy these images to a separate folder, serving two functionalities:

1. Allows the user to see which images were cataloged quickly
2. Allows for easier data collection if one wishes to train an AI to do this rather tedious job

This script was built for a very strange and edge use, so it's probably only useful for inspiration pertaining to other similar macros.
