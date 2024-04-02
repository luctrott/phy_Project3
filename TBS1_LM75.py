import smbus

class LM75:
    def __init__(self, address):
        self._i2c = smbus.SMBus(1)
        self._address = address

    def _swap_bytes(self, word):
        return ((word << 8) & 0xFF00) + (word >> 8)

    def _two_complement(self, word):
        if(word >= 0x8000):
            return -((0xFFFF - word) + 1)
        else:
            return word

    def temperature_c(self):
        rdwo = self._i2c.read_word_data(self._address, 0x00)
        word = self._swap_bytes(rdwo)
        temperature = self._two_complement(word)
        temperature = temperature >> 5
        temperature = temperature * 0.125
        return temperature
