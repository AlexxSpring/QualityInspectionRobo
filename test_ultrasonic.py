from gpiozero import DistanceSensor
sensor = DistanceSensor(echo=24, trigger=23)
print(sensor.distance * 100)  # Should print real distance in cm