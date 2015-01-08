
def distance_to_co2(km):
    if km < 3500:
        kgco2 = 1.36307304e-08*km**2  - 7.06618762e-05*km + 1.52332253e-01

    else:
        kgco2 =  1.63625000e-10*km**2 - 1.81805000e-06*km + 6.87451000e-02

    
    totco2 = kgco2 * km

    return totco2

