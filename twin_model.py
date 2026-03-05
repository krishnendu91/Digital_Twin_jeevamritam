class WaterTreatmentTwin:

    def __init__(self):

        self.tank_input = 50
        self.tank_output = 60
        self.pressure1 = 1.5
        self.pressure2 = 1.2
        self.mode = "filter"

    def update_sensor(self,data):

        self.tank_input = data["tank1"]
        self.tank_output = data["tank2"]
        self.pressure1 = data["pressure1"]
        self.pressure2 = data["pressure2"]

    def set_mode(self,mode):

        self.mode = mode

twin = WaterTreatmentTwin()