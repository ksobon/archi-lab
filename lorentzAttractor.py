import Rhino as rc

x = P0.X
y = P0.Y
z = P0.Z

MaxCount = 200000
Count = 1

outPoints = []
for i in range(0, N-1, 1):
    pt = rc.Geometry.Point3d(x,y,z)
    outPoints.append(pt)
    Dist = 0
    while Dist < minDist:
        Count = Count + 1
        if Count > MaxCount:
            break
        else:
            dx = dt * (sigma * (y - x))
            dy = dt * (x * (rho - z) - y)
            dz = dt * (x * y - beta * z)
            Dist = Dist + (dx * dx + dy * dy + dz * dz) ** 0.5
            x = x + dx
            y = y + dy
            z = z + dz
pts = outPoints
