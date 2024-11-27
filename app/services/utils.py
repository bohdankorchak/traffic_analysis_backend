class Coordinates:
    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

def decode_polyline(encoded):
    points = []
    index = lat = lng = 0

    while index < len(encoded):
        result = shift = 0
        while True:
            b = ord(encoded[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lat += ~(result >> 1) if (result & 1) else (result >> 1)

        result = shift = 0
        while True:
            b = ord(encoded[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lng += ~(result >> 1) if (result & 1) else (result >> 1)

        points.append([lat / 1e5, lng / 1e5])
    return points