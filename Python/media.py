import webbrowser

class Movie():
    def __init__ (self, title, storyline, img, trailer):
        self.title = title
        self.storyline = storyline
        self.img_url = img
        self.trailer_url = trailer


    def showtrailer (self):
        webbrowser.open(self.trailer_url)
