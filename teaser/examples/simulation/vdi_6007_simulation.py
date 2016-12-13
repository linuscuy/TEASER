#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example script for VDI 6007 simulation usage
"""

import numpy as np

from teaser.project import Project
import teaser.logic.simulation.VDI_6007.weather as weat
import teaser.logic.simulation.VDI_6007.low_order_VDI as low_order_VDI
import teaser.logic.simulation.VDI_6007.eqAirTemp as equ_air


def gen_res_type_example_building():
    """
    Generate example residential type building for VDI 6007 calculation

    Returns
    -------
    prj : object
        TEASER project instance
    """

    prj = Project(load_data=True)
    prj.name = "ArchetypeBuildings"
    prj.type_bldg_residential(name="ResidentialBuilding",
                              year_of_construction=1988,
                              number_of_floors=2,
                              height_of_floors=2.8,
                              net_leased_area=200,
                              with_ahu=True,
                              residential_layout=0,
                              neighbour_buildings=0,
                              attic=1,
                              cellar=1,
                              construction_type="heavy",
                              dormer=1)

    return prj


def vdi_example_6007(thermal_zone, weather):
    """
    Example function to perform VDI 6007 calculation with thermal_zone

    Parameters
    ----------
    thermal_zone : object
        TEASER thermal zone object
    weather : object
        Weather object of TEASER
    """

    timesteps = 365 * 24

    # Load constant house parameters
    if len(thermal_zone.inner_walls) != 0:
        withInnerwalls = True
    else:
        withInnerwalls = False

    #  Convert into house data dictionary
    #  #-------------------------------------------------------
    houseData = {"R1i": thermal_zone.r1_iw,
                 "C1i": thermal_zone.c1_iw/3600,   # Convert Ws/K to Wh/K
                 "Ai": thermal_zone.area_iw,
                 "RRest": thermal_zone.r_rest_ow,
                 "R1o": thermal_zone.r1_ow,
                 "C1o": thermal_zone.c1_ow/3600,  # Convert Ws/K to Wh/K
                 "Ao": [thermal_zone.area_ow],
                 "Aw": thermal_zone.window_area_list,
                 "At": thermal_zone.window_area_list,
                 "Vair": thermal_zone.volume,
                 "rhoair": thermal_zone.density_air,
                 "cair": thermal_zone.heat_capac_air/3600,  # Conv. Ws/kgK to Wh/kgK
                 "splitfac": thermal_zone.windows[0].a_conv,
                 "g": thermal_zone.weighted_g_value,
                 "alphaiwi": thermal_zone.alpha_comb_inner_iw,
                 "alphaowi": thermal_zone.alpha_comb_inner_ow,
                 "alphaWall": thermal_zone.alpha_comb_outer_ow,
                 "withInnerwalls": withInnerwalls}
    #  TODO: Add further parameters to house data to use equAirTemp.py

    houseDataval = {"R1i": 0.000779671554640369,
                "C1i": 12333949.4129606,
                "Ai": 58,
                "RRest": 0.011638548,
                "R1o": 0.00171957697767797,
                "C1o": 4338751.41,
                "Ao": [28],
                "Aw": np.zeros(1),
                "At": [7,],
                "Vair": 52.5,
                "rhoair": 1.19,
                "cair": 0,
                "splitfac": 0.09,
                "g": 1,
                "alphaiwi": 2.12,
                "alphaowi": 2.398,
                "alphaWall": 28 * 9.75, # 28 * sum(Ao)
                "withInnerwalls": True}

    for key in houseDataval:
        if isinstance(houseData[key], float) or isinstance(houseData[key], int):
            print(key, houseData[key] - houseDataval[key])

    #  Solar radiation input on each external area in W/m2
    #  #-------------------------------------------------------
    # solarRad_in = np.zeros((timesteps, 5))
    solarRad_in = np.transpose(weather.sun_rad)

    source_igRad = np.zeros(timesteps)

    krad = 1

    #  Equal air temperature based on VDI in K
    #  #-------------------------------------------------------
    #  equalAirTemp = np.zeros(timesteps) + 273.15 + 10
    equalAirTemp = weather.temp + 0.5

    # equalAirTemp = equ_air.eqAirTemp(weather=weather, houseData=houseData,
    #                                  solarRad_in=solarRad_in, method="vdi")

    #  Environment temperatures in K
    #  #-------------------------------------------------------
    #  weatherTemperature = np.zeros(timesteps) + 273.15 + 10  # in K
    weatherTemperature = weather.temp
    print(weatherTemperature)

    #  Ventilation rate: Fresh air at temperature weatherTemperature in m3/s
    #  #-------------------------------------------------------
    #  TODO: Substitute with TEASER call (or VDI call)
    # ventRate = np.zeros(timesteps)
    ventRate = np.zeros(timesteps) + thermal_zone.volume * 1 / 3600

    #  Internal convective gains in W
    #  #-------------------------------------------------------
    #  TODO: Substitute with TEASER boundary conditions
    #  logic/buildingobjects/boundaryconditions/boundaryconditions.py
    #  Living (18599) / SIA for occupancy
    Q_ig = np.zeros(timesteps)  # + 200

    # Radiative heat transfer coef. between inner and outer walls in W/m2K
    alphaRad = np.zeros(timesteps) + 5

    # Define set points for heating
    #  #-------------------------------------------------------
    #  TODO: Calculate with function call (depending on occupancy)
    # t_set_heating = np.zeros(timesteps) + 273.15 + 21  # in Kelvin
    t_set_heat_day = \
        np.array([18, 18, 18, 18, 18, 18, 21, 21, 21, 21, 21, 21,
                 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 18]) + 273.15
    t_set_heating = np.tile(t_set_heat_day, 365)

    # Define set points for cooling (cooling is disabled for high values)
    #  #-------------------------------------------------------
    t_set_cooling = np.zeros(timesteps) + 273.15 + 1000  # in Kelvin

    heater_limit = np.zeros((timesteps, 3)) + 1e10
    cooler_limit = np.zeros((timesteps, 3)) - 1e10

    # Calculate indoor air temperature with VDI model
    T_air, Q_hc, Q_iw, Q_ow = \
        low_order_VDI.reducedOrderModelVDI(houseData=houseData,
                                           weatherTemperature=weatherTemperature,
                                           solarRad_in=solarRad_in,
                                           equalAirTemp=equalAirTemp,
                                           alphaRad=alphaRad,
                                           ventRate=ventRate,
                                           Q_ig=Q_ig,
                                           source_igRad=source_igRad,
                                           krad=krad,
                                           heater_order=np.array([1, 2, 3]),
                                           cooler_order=np.array([1, 2, 3]),
                                           t_set_heating=t_set_heating,
                                           t_set_cooling=t_set_cooling,
                                           heater_limit=heater_limit,
                                           cooler_limit=cooler_limit)

    return (T_air, Q_hc, Q_iw, Q_ow)


if __name__ == '__main__':

    weather = weat.Weather()

    #  Convert temperature to Kelvin
    weather.temp += 273.15

    #  Get TEASER project with residential type building
    prj = gen_res_type_example_building()

    #  Pointer to building object
    building = prj.buildings[0]

    #  Extract thermal_zone
    thermal_zone = prj.buildings[0].thermal_zones[0]

    print('UA value before retrofiting:')
    print(prj.buildings[0]._thermal_zones[0]._outer_walls[0].ua_value)
    print('Inner resistance (VDI 6007) of thermal zone before retrofit:')
    print(thermal_zone.r1_ow)
    print()

    # building.retrofit_building(year_of_retrofit=2014)
    #
    # print('UA value after retrofiting:')
    # print(prj.buildings[0]._thermal_zones[0]._outer_walls[0].ua_value)
    # print('Inner resistance (VDI 6007) of thermal zone after retrofit:')
    # print(thermal_zone.r1_ow)
    # print()

    #  Rund VDI 6007 example with thermal zone
    (T_air, Q_hc, Q_iw, Q_ow) = vdi_example_6007(thermal_zone, weather=weather)

    print('Indoor air temperature in Kelvin:')
    print(T_air)
    print()

    print('Heating(+) / cooling(-) load in Watt:')
    print(Q_hc)
    print()

    q_heat = np.zeros(len(Q_hc))
    q_cool = np.zeros(len(Q_hc))
    for i in range(len(Q_hc)):
        if Q_hc[i] > 0:
            q_heat[i] = Q_hc[i]
        elif Q_hc[i] < 0:
            q_cool[i] = Q_hc[i]

    print('Sum of heating energy in kWh:')
    print(sum(q_heat)/1000)

    print('Sum of cooling energy in kWh:')
    print(-sum(q_cool) / 1000)

    import matplotlib.pyplot as plt

    fig = plt.figure()
    fig.add_subplot(411)
    plt.plot(weather.temp - 273.15)
    plt.ylabel('Outdoor air\ntemperature in\ndegree Celsius')
    fig.add_subplot(412)
    plt.plot(weather.sun_rad[0])
    plt.ylabel('Sun radiation\non surface 0')  # TODO: Add unit
    fig.add_subplot(413)
    plt.plot(T_air - 273.15)
    plt.ylabel('Indoor air\ntemperature in\ndegree Celsius')
    fig.add_subplot(414)
    plt.plot(Q_hc / 1000)
    plt.ylabel('Heating/cooling\npower (+/-)\nin kW')
    plt.xlabel('Time in hours')
    plt.show()