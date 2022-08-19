from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, Arraylist

import random

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    def getGeneratorName(self):
        return 'Generator Danych BHP'

    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)

class BHPFuzzer(IIntruderPayloadGenerator):
    def __init__(self, extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterations = 0

        return

    def hasMorePayloads(self):
        if self.num_iterations == self.max_payloads:
            return False
        else:
            return True

    def getNextPayload(self,current_payload):
        #Konwersja na łańcuch
        payload = "".join(chr(x) for x in current_payload)

        #Wywołanie mutatora w celu zmiany żądania POST
        payload = self.mutate_payload(payload)

        #Zwiększenie liczby prób fuzzingu
        self.num_iterations += 1

        return payload

    def reset(self):
        self.num_iterations = 0
        return

    def mutate_payload(self, original_payload):
        #wybierz prosty mutator albo wywołaj skrypt zewnętrznny
        picker = random.randint(1, 3)

        #wybiera losowe miejsce w załadunku do zmiany
        offset = random.randint(0, len(original_payload)-1)

        front, back = original_payload[:offset], original_payload[offset:]

        #Próba wtrysku SQL
        if picker == 1:
            front += "'"

        #Próba ataku XSS
        elif picker == 2:
            front += "<script>alert('BHP!'):</script>"

        #Powtórzenie fragmentu oryginalnego ładunku
        elif picker == 3:
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(0, 10)
            for i in range(repeater):
                front += original_payload[:offset+chunk_length]

        return front + back
