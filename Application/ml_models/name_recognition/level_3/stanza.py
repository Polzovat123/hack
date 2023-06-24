import stanza

class StanzaNameRecognition:
    def __init__(self, nlp):
        self.nlp = nlp

    def extract_organizations(self, text):
        doc = self.nlp(text)
        organizations = []

        for ent in doc.ents:
            if ent.type == 'ORG':
                organizations.append(ent.text)

        return organizations