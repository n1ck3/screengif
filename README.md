# screengif

A simple Python program than captures the screen for set amount of time and saves it as an animated gif to the Desktop.

It tries to mimic the built in Screencapture functionality in OS X.

# Getting started

Pull this repo

```
cd ~
mkdir git && cd git
git clone https://github.com/n1ck3/screengif.git
```

Prepare for running screengif

```
cd ~/git/screengif
virtaualenv .
source bin/activate
pip install -r requirements.txt
```

Actually running screengif

```
~/git/screengif/screengif.py [-c|--clipboard]
```

# TODO:

- [ ] Add proper argument handling
- [ ] Add possibility to *only* copy to clipboard
- [ ] Add support for linux
- [ ] Optimize execution
- [ ] Add menubar (taskbar) item to manage the app
