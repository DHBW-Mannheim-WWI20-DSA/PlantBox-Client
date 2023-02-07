import smbus

# I2C-Busnummer (0 für Revision 1, 1 für Revision 2)
bus = smbus.SMBus(1)

# I2C-Adresse des AD-Wandlers (0x48 ist die Standardadresse)
address = 0x48

# Register des AD-Wandlers, das die Daten des Sensors enthält
channel = 4

while True:
    # AD-Wandler auslesen
    data = bus.read_byte_data(address, channel)
    # Daten in Prozent umrechnen
    soil_moisture = (195 - data) / (195 - 75) * 100
    # Ausgabe auf der Konsole
    print("Soil moisture: {:.2f}%".format(soil_moisture))
    # Wartezeit einlegen
    time.sleep(1)
