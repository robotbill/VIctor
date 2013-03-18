class Command(object):
    def __init__(self, text):
        tokens = self.tokenize(text)
        self.command = tokens[0].strip()
        self.arguments = [ s.strip() for s in tokens[1:] ]

    def run(self):
        print "Running {} with {}".format(self.command, self.arguments)

    def tokenize(self, text):
        return text[1:].split(" ")

