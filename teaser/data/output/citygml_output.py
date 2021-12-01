# Created October 2015
# TEASER Development Team

"""CityGML

This module contains function to save and load Projects in the non proprietary
CityGML file format .gml
"""
import re
import os
import lxml.etree as ET
from datetime import date, datetime
import uuid
import teaser.data.output.citygml_classes as cl
import pyxb
import pyxb.utils
import pyxb.namespace
import pyxb.bundles
import pyxb.binding as bd
import pyxb.bundles.common.raw.xlink as xlink
import pandas as pd

def save_gml_lxml(project, path, gml_copy=None, ref_coordinates=None, results=None):
    """Based on CityGML Building export from CityBIT"""

    # if path.endswith("gml"):
    #     out_file = open(path, 'w')
    # else:
    #     out_file = open(path + ".gml", 'w')

    crs = "urn:adv:crs:ETRS89_UTM32*DE_DHHN2016_NH*GCG2016"
    print('crs:', crs)

    global nsClass
    nsClass = cl.CGML2

    # creating new namespacemap
    newNSmap = {'core': nsClass.core, 'gen': nsClass.gen, 'grp': nsClass.grp, 'app': nsClass.app, 'bldg': nsClass.bldg,
                'gml': nsClass.gml, 'xal': nsClass.xal, 'xlink': nsClass.xlink, 'xsi': nsClass.xsi,
                'energy': nsClass.energy}
    schemaLocation = "http://www.opengis.net/citygml/2.0 http://www.sig3d.org/citygml/2.0/energy/1.0/EnergyADE.xsd"

    # creating new root element
    global nroot_E
    nroot_E = ET.Element(ET.QName(nsClass.core, 'CityModel'),attrib={"{" + nsClass.xsi + "}schemaLocation" : schemaLocation}, nsmap=newNSmap)

    # creating name element
    name_E = ET.SubElement(nroot_E, ET.QName(nsClass.gml, 'name'), nsmap={'gml': nsClass.gml})
    name_E.text = 'created using the e3D TEASERplus'

    """create new cityObjectMember here"""
    cityObjectMember_E = ET.SubElement(nroot_E, ET.QName(nsClass.core, 'cityObjectMember'))

    # setting gml:id
    # if u_GML_id != None:
    #     gmlID = u_GML_id
    # else:

    if ref_coordinates is not None:

        gml_out = _set_reference_boundary(cityObjectMember_E,
                                          ref_coordinates[0],
                                          ref_coordinates[1])
    else:
        bldg_center = [0, 0, 0]
        pass

    materials = {}

    for i, bldg_count in enumerate(project.buildings):
        gmlID = "e3D_TEASERplus_" + str(bldg_count.internal_id)

        if gml_copy is None or re.match(r"(\w+)bt_", bldg_count.name):

            gml_bldg = ET.SubElement(cityObjectMember_E, ET.QName(nsClass.bldg, 'Building'),
                                       attrib={ET.QName(nsClass.gml, 'id'): gmlID})

            _set_gml_building_lxml(gml_bldg, nsClass, bldg_count, ET)

            """for testing the loop"""
            if results is not None:
                _save_simulation_results(gml_bldg, results=results)

            bldg_center = [i * 80, 0, 0]

            if type(bldg_count).__name__ == "SingleFamilyDwelling":
                building_length = (bldg_count.thermal_zones[0].area /
                                   bldg_count.thermal_zones[0].typical_width)
                building_width = bldg_count.thermal_zones[0].typical_width
                building_height = (bldg_count.number_of_floors *
                                   bldg_count.height_of_floors)

            else:
                building_width = 0.05 * (bldg_count.net_leased_area /
                                         bldg_count.number_of_floors)
                building_length = (bldg_count.net_leased_area /
                                   bldg_count.number_of_floors) / building_width
                building_height = (bldg_count.number_of_floors *
                                   bldg_count.height_of_floors)

            _set_lod_2_lxml(gml_bldg, building_length, building_width, building_height, bldg_center, nsClass, None)

        else:
            for e in range(0, len(gml_copy)):
                # if gml_copy[e].Feature.id == bldg_count.name:
                gml_out.featureMember.append(gml_copy[e])
                gml_bldg = gml_copy[e].Feature

            if results is not None:
                _save_simulation_results(gml_bldg, results=results)

        for zone_count in bldg_count.thermal_zones:
            _set_gml_volume_lxml(gml_bldg, nsClass, zone_count, ET)
            PolyIDs = _set_gml_thermal_zone_lxml(gml_bldg, nsClass, zone_count, ET)
            # gml_usage = _set_gml_usage(zone_count, zone_count.use_conditions)


        tree = ET.ElementTree(nroot_E)

        # writing file
        print('writing file')
        print(tree)
        print(os.path.normpath(os.path.join(path, "test.gml")))
        print(str(os.path.join(path, "test.gml")))
        tree.write(os.path.join(path), pretty_print=True, xml_declaration=True,
                   encoding='utf-8', standalone='yes', method="xml")


def _set_gml_building_lxml(gml_bldg, nsClass, teaser_building, ET):
    """Creates an instance of a citygml Building with attributes

        creates a citygml.building.Building object. And fills the attributes of
        this instance with attributes of the TEASER building

        Parameters
        ----------

        teaser_building : Building Object of TEASER
            Instance of a TEASER object with set attributes

        Returns
        -------

        gml_bldg : citygml.building.Building() object
            Returns a citygml Building with attributes
        """

# gml_bldg = ET.SubElement(cityObjectMember_E, ET.QName(nsClass.bldg, 'Building'),
#                                        attrib={ET.QName(nsClass.gml, 'id'): gmlID})

    ET.SubElement(gml_bldg, ET.QName(nsClass.gml,
                                       'description')).text = 'created using the e3D TEASER+'

    # building attributes
    ET.SubElement(gml_bldg, ET.QName(nsClass.gml, 'name')).text = teaser_building.name
    ET.SubElement(gml_bldg, ET.QName(nsClass.core, 'creationDate')).text = str(date.today())
    ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'buildingFunction')).text = str(teaser_building.type_of_building)
    ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'yearOfConstruction')).text = \
        str(teaser_building.year_of_construction)
    ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'roofType'), attrib={
        'codeSpace': 'http://www.sig3d.org/codelists/citygml/2.0/building/2.0/_AbstractBuilding_roofType.xml'})\
        .text = str(1000)
    ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'measuredHeight'), attrib={'uom': "m"}).text = \
        str(teaser_building.number_of_floors * teaser_building.height_of_floors)
    ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'storeysAboveGround')).text = \
        str(teaser_building.number_of_floors)


def _set_reference_boundary(gml_out, lower_coords, upper_coords):
    """Adds a reference coordinate system with `Envelope`'s corners

    The gml file includes a reference coordinate system defined in the
    `boundedBy` object, within which the `Envelope` object contains both a
    `lowerCorner` and an `upperCorner`. Both corners extend
    `gml.DirectPositionType`. This method sets all necessary parts of the
    `boundedBy` in a given gml file.

    Parameters
    ----------

    gml_out : citygml.CityModel() object
        A CityModel object, where citygml is a reference to
        `pyxb.bundles.opengis.citygml.base`. The reference coordinate system
        will be added to this object.
    lower_coords : list
        A list that contains the coordinates of the point for the
        `lowerCorner` definition. It should contain 3 ints or floats for
        x, y, and z coordinates of the point.
    upper_coords : list
        A list that contains the coordinates of the point for the
        `upperCorner` definition. It should contain 3 ints or floats for
        x, y, and z coordinates of the point.

    Returns
    -------

    gml_out : citygml.CityModel() object
        Returns the modified CityModel object
    """
    assert len(lower_coords) == 3, 'lower_coords must contain 3 elements'
    assert len(upper_coords) == 3, 'lower_coords must contain 3 elements'

    reference_bound = gml.boundedBy()

    reference_envelope = gml.Envelope()
    reference_envelope.srsDimension = 3
    reference_envelope.srsName = 'urn:adv:crs:ETRS89_UTM32'

    lower_corner = gml.DirectPositionType(lower_coords)
    lower_corner.srsDimension = 3
    reference_envelope.lowerCorner = lower_corner
    upper_corner = gml.DirectPositionType(upper_coords)
    upper_corner.srsDimension = 3
    reference_envelope.upperCorner = upper_corner

    reference_bound.Envelope = reference_envelope
    gml_out.boundedBy = reference_bound

    return gml_out


def _set_lod_2_lxml(gml_bldg, length, width, height, bldg_center, nsClass, PolyIDs):
    """Adds a LOD 2 representation of the building based on building length,
    width and height

    alternative way to handle building position

    Parameters
    ----------

    gml_bldg : bldg.Building() object
        A building object, where bldg is a reference to
        `pyxb.bundles.opengis.citygml.building`.
    length : float
        length of the building
    width : float
        width of the building
    height : float
        height of the building
    bldg_center : list
        coordinates in the reference system of the building center


    """

    # Ground surface

    boundedBy_E = ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'boundedBy'))
    groundSurfaceID = "GML_" + str(uuid.uuid1())
    wallRoofGround_E = ET.SubElement(boundedBy_E, ET.QName(nsClass.bldg, 'GroundSurface'),
                                     attrib={ET.QName(nsClass.gml, 'id'): groundSurfaceID})
    ET.SubElement(wallRoofGround_E, ET.QName(nsClass.gml, 'name')).text = 'GroundSurface'
    lodnMultisurface_E = ET.SubElement(wallRoofGround_E, ET.QName(nsClass.bldg, 'lod2MultiSurface'))
    multiSurface_E = ET.SubElement(lodnMultisurface_E, ET.QName(nsClass.gml, 'MultiSurface'))
    surfaceMember_E = ET.SubElement(multiSurface_E, ET.QName(nsClass.gml, 'surfaceMember'))

    bldg_center[0] -= length / 2
    bldg_center[1] -= width / 2

    coords = [[bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1], bldg_center[2]],
              [bldg_center[0], width + bldg_center[1], bldg_center[2]]]

    polyID = str(uuid.uuid1())

    _add_surface_lxml(surfaceMember_E, nsClass, coords, polyID)

    # Roof surface

    boundedBy_E = ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'boundedBy'))
    roofSurfaceID = "GML_" + str(uuid.uuid1())
    wallRoofGround_E = ET.SubElement(boundedBy_E, ET.QName(nsClass.bldg, 'RoofSurface'),
                                     attrib={ET.QName(nsClass.gml, 'id'): roofSurfaceID})
    ET.SubElement(wallRoofGround_E, ET.QName(nsClass.gml, 'name')).text = 'RoofSurface'
    lodnMultisurface_E = ET.SubElement(wallRoofGround_E, ET.QName(nsClass.bldg, 'lod2MultiSurface'))
    multiSurface_E = ET.SubElement(lodnMultisurface_E, ET.QName(nsClass.gml, 'MultiSurface'))
    surfaceMember_E = ET.SubElement(multiSurface_E, ET.QName(nsClass.gml, 'surfaceMember'))

    coords = [[bldg_center[0], bldg_center[1], bldg_center[2] + height],
              [length + bldg_center[0], bldg_center[1],
               bldg_center[2] + height],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2] + height],
              [bldg_center[0], width + bldg_center[1], bldg_center[2] + height]]

    polyID = str(uuid.uuid1())

    _add_surface_lxml(surfaceMember_E, nsClass, coords, polyID)

    # Side a surface

    boundedBy_E = ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'boundedBy'))
    wall_a_SurfaceID = "GML_" + str(uuid.uuid1())
    wallRoofGround_E = ET.SubElement(boundedBy_E, ET.QName(nsClass.bldg, 'WallSurface'),
                                     attrib={ET.QName(nsClass.gml, 'id'): wall_a_SurfaceID})
    ET.SubElement(wallRoofGround_E, ET.QName(nsClass.gml, 'name')).text = 'WallSurface'
    lodnMultisurface_E = ET.SubElement(wallRoofGround_E, ET.QName(nsClass.bldg, 'lod2MultiSurface'))
    multiSurface_E = ET.SubElement(lodnMultisurface_E, ET.QName(nsClass.gml, 'MultiSurface'))
    surfaceMember_E = ET.SubElement(multiSurface_E, ET.QName(nsClass.gml, 'surfaceMember'))

    coords = [[bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], bldg_center[1],
               bldg_center[2] + height],
              [bldg_center[0], bldg_center[1], bldg_center[2] + height]]

    polyID = str(uuid.uuid1())

    _add_surface_lxml(surfaceMember_E, nsClass, coords, polyID)

    # Side b surface

    boundedBy_E = ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'boundedBy'))
    wall_b_SurfaceID = "GML_" + str(uuid.uuid1())
    wallRoofGround_E = ET.SubElement(boundedBy_E, ET.QName(nsClass.bldg, 'WallSurface'),
                                     attrib={ET.QName(nsClass.gml, 'id'): wall_b_SurfaceID})
    ET.SubElement(wallRoofGround_E, ET.QName(nsClass.gml, 'name')).text = 'WallSurface'
    lodnMultisurface_E = ET.SubElement(wallRoofGround_E, ET.QName(nsClass.bldg, 'lod2MultiSurface'))
    multiSurface_E = ET.SubElement(lodnMultisurface_E, ET.QName(nsClass.gml, 'MultiSurface'))
    surfaceMember_E = ET.SubElement(multiSurface_E, ET.QName(nsClass.gml, 'surfaceMember'))

    coords = [[bldg_center[0], width + bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2] + height],
              [bldg_center[0], width + bldg_center[1], bldg_center[2] + height]]

    polyID = str(uuid.uuid1())

    _add_surface_lxml(surfaceMember_E, nsClass, coords, polyID)

    # Side c surface

    boundedBy_E = ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'boundedBy'))
    wall_c_SurfaceID = "GML_" + str(uuid.uuid1())
    wallRoofGround_E = ET.SubElement(boundedBy_E, ET.QName(nsClass.bldg, 'WallSurface'),
                                     attrib={ET.QName(nsClass.gml, 'id'): wall_c_SurfaceID})
    ET.SubElement(wallRoofGround_E, ET.QName(nsClass.gml, 'name')).text = 'WallSurface'
    lodnMultisurface_E = ET.SubElement(wallRoofGround_E, ET.QName(nsClass.bldg, 'lod2MultiSurface'))
    multiSurface_E = ET.SubElement(lodnMultisurface_E, ET.QName(nsClass.gml, 'MultiSurface'))
    surfaceMember_E = ET.SubElement(multiSurface_E, ET.QName(nsClass.gml, 'surfaceMember'))

    coords = [[bldg_center[0], bldg_center[1], bldg_center[2]],
              [bldg_center[0], width + bldg_center[1], bldg_center[2]],
              [bldg_center[0], width + bldg_center[1], bldg_center[2] + height],
              [bldg_center[0], bldg_center[1], bldg_center[2] + height]]

    polyID = str(uuid.uuid1())

    _add_surface_lxml(surfaceMember_E, nsClass, coords, polyID)

    # Side d surface

    boundedBy_E = ET.SubElement(gml_bldg, ET.QName(nsClass.bldg, 'boundedBy'))
    wall_d_SurfaceID = "GML_" + str(uuid.uuid1())
    wallRoofGround_E = ET.SubElement(boundedBy_E, ET.QName(nsClass.bldg, 'WallSurface'),
                                     attrib={ET.QName(nsClass.gml, 'id'): wall_d_SurfaceID})
    ET.SubElement(wallRoofGround_E, ET.QName(nsClass.gml, 'name')).text = 'WallSurface'
    lodnMultisurface_E = ET.SubElement(wallRoofGround_E, ET.QName(nsClass.bldg, 'lod2MultiSurface'))
    multiSurface_E = ET.SubElement(lodnMultisurface_E, ET.QName(nsClass.gml, 'MultiSurface'))
    surfaceMember_E = ET.SubElement(multiSurface_E, ET.QName(nsClass.gml, 'surfaceMember'))

    coords = [[length + bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2] + height],
              [length + bldg_center[0], bldg_center[1],
               bldg_center[2] + height]]

    polyID = str(uuid.uuid1())

    _add_surface_lxml(surfaceMember_E, nsClass, coords, polyID)


def _add_surface_lxml(multi_surface, nsClass, coords, polyID):
    assert len(coords) == 4, 'coords must contain 4 elements'
    for coord in coords:
        assert len(coord) == 3, 'Each coord list should contain 3 elements'

    surfaceMember_E = ET.SubElement(multi_surface, ET.QName(nsClass.gml, 'surfaceMember'))
    polygon_E = ET.SubElement(surfaceMember_E, ET.QName(nsClass.gml, 'Polygon'),
                              attrib={ET.QName(nsClass.gml, 'id'): polyID})
    exterior_E = ET.SubElement(polygon_E, ET.QName(nsClass.gml, 'exterior'))
    ring_id = polyID + '_0'
    linearRing_E = ET.SubElement(exterior_E, ET.QName(nsClass.gml, 'LinearRing'),
                                 attrib={ET.QName(nsClass.gml, 'id'): ring_id})

    input_list = []
    for coord in coords:
        for value in coord:
            input_list.append(value)
    for value in coords[0]:
        input_list.append(value)

    stringed = [str(j) for j in input_list]
    ET.SubElement(linearRing_E, ET.QName(nsClass.gml, 'posList')).text = ' '.join(stringed)


def _set_gml_volume_lxml(gml_bldg, nsClass, thermal_zone, ET):

    # declaring Volume Object

    gml_volume = ET.SubElement(gml_bldg, ET.QName(nsClass.energy, 'volume'))
    gml_volume_type = ET.SubElement(gml_volume, ET.QName(nsClass.energy, 'VolumeType'))
    ET.SubElement(gml_volume_type, ET.QName(nsClass.energy, 'type')).text = "grossVolume"
    ET.SubElement(gml_volume_type, ET.QName(nsClass.energy, 'value'), attrib={'uom': "m3"}).text \
        = str(thermal_zone.volume)


def _set_gml_floor_area_lxml(gml_bldg, nsClass,thermal_zone, ET):

    # declaring Floor Area Object

    gml_floor_area = ET.SubElement(gml_bldg, ET.QName(nsClass.energy, 'floorArea'))
    gml_floor_area_type = ET.SubElement(gml_floor_area, ET.QName(nsClass.energy, 'FloorArea'))
    ET.SubElement(gml_floor_area_type, ET.QName(nsClass.energy, 'type')).text = "grossFloorArea"
    ET.SubElement(gml_floor_area_type, ET.QName(nsClass.energy, 'value'), attrib={'uom': "m2"}).text \
        = str(thermal_zone.area)


def _set_gml_thermal_zone_lxml(gml_bldg, nsClass, thermal_zone, ET):

    thermal_zone_id = str("GML_" + str(thermal_zone.internal_id))
    usage_zone_id = str("GML_" + str(thermal_zone.use_conditions.internal_id))
    gml_thermal_zone = ET.SubElement(gml_bldg, ET.QName(nsClass.energy, 'thermalZone'))
    gml_Thermal_Zone = ET.SubElement(gml_thermal_zone, ET.QName(nsClass.energy, 'ThermalZone'),
                                     attrib={ET.QName(nsClass.gml, 'id'): thermal_zone_id})
    ET.SubElement(gml_Thermal_Zone, ET.QName(nsClass.energy, 'contains'),
                  attrib={ET.QName(nsClass.xlink, 'href'): str('#'+usage_zone_id)})
    _set_gml_volume_lxml(gml_Thermal_Zone, nsClass, thermal_zone, ET)
    _set_gml_floor_area_lxml(gml_Thermal_Zone, nsClass, thermal_zone, ET)
    ET.SubElement(gml_Thermal_Zone, ET.QName(nsClass.energy, 'isCooled')).text = "false"
    ET.SubElement(gml_Thermal_Zone, ET.QName(nsClass.energy, 'isHeated')).text = "true"
    gml_volume_geometry = ET.SubElement(gml_Thermal_Zone, ET.QName(nsClass.energy, 'volumeGeometry'))
    polyIDs, exteriorSurfaces = _set_composite_surface(gml_volume_geometry, nsClass, thermal_zone, ET)

    """Set Usage zone for thermal zone"""
    _set_usage_zone_lxml(thermal_zone, gml_bldg, usage_zone_id)

    """Set boundary Surfaces"""

    construction_id_windows = None

    for i in range(len(exteriorSurfaces)):
        if i == 0:
            surfaceType = 'WallSurface'
            construction_id = None

        elif i == 1:
            surfaceType = 'RoofSurface'
            construction_id = None

        elif i == 2:
            surfaceType = 'GroundSurface'
            construction_id = None


        for surface in exteriorSurfaces[i]:
            thermal_openings = []

            for win_count in thermal_zone.windows:
                if surface.orientation == win_count.orientation and surface.tilt == win_count.tilt:
                    thermal_openings.append(win_count)
            construction_id, construction_id_windows = \
                _set_gml_thermal_boundary_lxml(gml_Thermal_Zone, surface, thermal_openings,
                                               nsClass, construction_id, construction_id_windows)

    return polyIDs


def _set_composite_surface(solid, nsClass, thermal_zone, ET):

    exteriorSurfaces = [thermal_zone.outer_walls, thermal_zone.rooftops, thermal_zone.ground_floors]
    polyIDs = []
    n = 0
    UUID = uuid.uuid1()
    for dictionary in exteriorSurfaces:
        for key in dictionary:
            ID = "PolyID" + str(UUID) + '_' + str(n)
            polyIDs.append(ID)
            hashtagedID = '#' + ID
            ET.SubElement(solid, ET.QName(nsClass.gml, 'surfaceMember'),
                          attrib={ET.QName(nsClass.xlink, 'href'): hashtagedID})
            n -= - 1
    return polyIDs, exteriorSurfaces


def _set_gml_thermal_boundary_lxml(gml_zone, wall, thermal_openings, nsClass, construction_id, construction_id_windows):
    """Control function to add a thermal boundary surface to the thermal zone

    The thermal zone instance of citygml is modified and thermal boundary
    surfaces are added. The thermal boundaries are chosen according to their
    type (OuterWall, InnerWall, Roof, etc.). For outer walls (including roof)
    the thermal boundary is returned to add windows (Thermal Openings).

    Parameters
    ----------

    gml_zone : energy.thermalZones() object
        A thermalZone object, where energy is a reference to
        `pyxb.bundles.opengis.citygml.energy`.

    wall : TEASER instance of Wall()
        Teaser instance of Wall or its inherited classes

    thermal_openings: List of TEASER instances of Window() or Door()
        Teaser instance of BuildingElement or its inherited classes
    Returns
    ----------

    _current_tb : energy.ThermalBoundarySurface()
        A ThermalBoundarySurface object with semantic information
        (area, azimuth, inclination etc.)

    """
    _current_tb = None
    if type(wall).__name__ == "OuterWall":

        thermal_boundary_type_value = "outerWall"


    elif type(wall).__name__ == "Rooftop":
        thermal_boundary_type_value = "roof"


    elif type(wall).__name__ == "GroundFloor":

        thermal_boundary_type_value = "groundSlab"

    elif type(wall).__name__ == "InnerWall":
        thermal_boundary_type_value = "intermediaryFloor"


    elif type(wall).__name__ == "Ceiling" or type(wall).__name__ == "Floor":

        thermal_boundary_type_value = "interiorWall"

    else:
        print("Strange Wall Surface detected!")

    boundedBy_E = ET.SubElement(gml_zone, ET.QName(nsClass.energy, 'boundedBy'))
    thermal_boundary_E = ET.SubElement(boundedBy_E, ET.QName(nsClass.energy, 'ThermalBoundary'),
                                       attrib={ET.QName(nsClass.gml, 'id'): str("GML_" + str(wall.internal_id))})
    ET.SubElement(thermal_boundary_E, ET.QName(nsClass.energy, "thermalBoundaryType")).text = \
        thermal_boundary_type_value
    ET.SubElement(thermal_boundary_E, ET.QName(nsClass.energy, "azimuth"), attrib={'uom': "deg"}).text = \
        str(wall.orientation)
    ET.SubElement(thermal_boundary_E, ET.QName(nsClass.energy, "inclination"), attrib={'uom': "deg"}).text = \
        str(wall.tilt)
    ET.SubElement(thermal_boundary_E, ET.QName(nsClass.energy, "area"), attrib={'uom': "m2"}).text = \
        str(wall.area)
    if construction_id is None:
        construction_id = _set_gml_construction_lxml( wall)
    else:
        pass
    print(construction_id)
    ET.SubElement(thermal_boundary_E, ET.QName(nsClass.energy, "construction"), attrib={ET.QName(nsClass.xlink, 'href'):
                                                                                        str("#" + str(construction_id))})

    if thermal_openings is not None:
        for thermal_opening in thermal_openings:
            contains = ET.SubElement(thermal_boundary_E, ET.QName(nsClass.energy, "contains"))
            thermal_opening_E = ET.SubElement(contains, ET.QName(nsClass.energy, "ThermalOpening"),
                                              attrib={ET.QName(nsClass.gml, 'id'): str("GML_" + str(thermal_opening.internal_id))})
            ET.SubElement(thermal_opening_E, ET.QName(nsClass.energy, "area"), attrib={'uom': "m2"}).text = \
                str(thermal_opening.area)
            if construction_id_windows is None:
                construction_id_windows = _set_gml_construction_lxml(thermal_opening)
            else:
                pass
            ET.SubElement(thermal_opening_E, ET.QName(nsClass.energy, "construction"),
                          attrib={ET.QName(nsClass.xlink, 'href'): str("#" + construction_id_windows)})
    return construction_id, construction_id_windows


def _set_gml_construction_lxml(element):
    construction_id = str("GML_" + str(uuid.uuid1()))
    feature_member = ET.SubElement(nroot_E, ET.QName(nsClass.gml, 'featureMember'))
    construction_gml = ET.SubElement(feature_member, ET.QName(nsClass.energy, 'Construction'),
                                     attrib={ET.QName(nsClass.gml, 'id'): str(construction_id)})
    ET.SubElement(construction_gml, ET.QName(nsClass.gml, "description")).text = \
        str(type(element).__name__ +"_construction")
    ET.SubElement(construction_gml, ET.QName(nsClass.gml, "name")).text = \
        str(type(element).__name__ + "_construction")
    ET.SubElement(construction_gml, ET.QName(nsClass.energy, "uValue"), attrib={'uom': "W/K*m2"}).text = \
        str(element.ua_value / element.area)


    for layer_count in element.layer:
        layer_gml = ET.SubElement(construction_gml, ET.QName(nsClass.energy, "layer"))
        Layer_gml = ET.SubElement(layer_gml, ET.QName(nsClass.energy, "Layer"),
                                  attrib={ET.QName(nsClass.gml, 'id'): str("GML_" + str(layer_count.internal_id))})
        layer_comp = ET.SubElement(Layer_gml, ET.QName(nsClass.energy, "layerComponent"))
        Layer_comp = ET.SubElement(layer_comp, ET.QName(nsClass.energy, "LayerComponent"),
                                  attrib={ET.QName(nsClass.gml, 'id'):
                                              str("GML_" + str(layer_count.internal_id) + "_1")})
        ET.SubElement(Layer_comp, ET.QName(nsClass.energy, "areaFraction"), attrib={'uom': "scale"}).text = str(1)
        ET.SubElement(Layer_comp, ET.QName(nsClass.energy, "thickness"), attrib={'uom': "m"}).text = \
            str(layer_count.thickness)
        ET.SubElement(Layer_comp, ET.QName(nsClass.energy, 'material'),
                                         attrib={ET.QName(nsClass.xlink, 'href'):
                                                     str("#" + "GML_" + layer_count.material.material_id)})

        feature_member_material = ET.SubElement(nroot_E, ET.QName(nsClass.gml, 'featureMember'))
        material_gml = ET.SubElement(feature_member_material, ET.QName(nsClass.energy, 'SolidMaterial'),
                                         attrib={ET.QName(nsClass.gml, 'id'):
                                                     str("GML_" + layer_count.material.material_id)})
        ET.SubElement(material_gml, ET.QName(nsClass.gml, "description")).text = \
            str(layer_count.material.name)
        ET.SubElement(material_gml, ET.QName(nsClass.gml, "name")).text = \
            str(layer_count.material.name)
        ET.SubElement(material_gml, ET.QName(nsClass.energy, "conductivity"), attrib={'uom': "W/K*m"}).text = \
            str(layer_count.material.thermal_conduc)
        ET.SubElement(material_gml, ET.QName(nsClass.energy, "density"), attrib={'uom': "kg/m3"}).text = \
            str(layer_count.material.density)
        ET.SubElement(material_gml, ET.QName(nsClass.energy, "specificHeat"), attrib={'uom': "kJ/K*kg"}).text = \
            str(layer_count.material.heat_capac)
    return construction_id


def _set_usage_zone_lxml(thermal_zone, gml_bldg, usage_zone_id):
    usage_zone = thermal_zone.use_conditions
    gml_usage_zone = ET.SubElement(gml_bldg, ET.QName(nsClass.energy, 'usageZone'))
    gml_Usage_Zone = ET.SubElement(gml_usage_zone, ET.QName(nsClass.energy, 'UsageZone'),
                                   attrib={ET.QName(nsClass.gml, 'id'): usage_zone_id})
    ET.SubElement(gml_Usage_Zone, ET.QName(nsClass.energy, 'usageZoneType')).text = str(usage_zone.usage)

    """Heating"""
    heating_schedule = ET.SubElement(gml_Usage_Zone, ET.QName(nsClass.energy, 'heatingSchedule'))
    _set_schedule(heating_schedule, usage_zone,  usage_zone_id, "heating")

    """Cooling"""
    # TODO: Check together with isCooled if AHU is used and set cooling

    """Ventilation"""
    # ventilation_schedule = ET.SubElement(gml_Usage_Zone, ET.QName(nsClass.energy, 'ventilationSchedule'))
    # _set_schedule(usage_zone, ventilation_schedule, usage_zone_id, "ventilation")

    """Occupiedby"""
    occupied_by = ET.SubElement(gml_Usage_Zone, ET.QName(nsClass.energy, 'occupiedBy'))
    occupants = ET.SubElement(occupied_by, ET.QName(nsClass.energy, 'Occupants'),
                              attrib={ET.QName(nsClass.gml, 'id'): (usage_zone_id + "_Occupants")})
    heat_dissipation = ET.SubElement(occupants, ET.QName(nsClass.energy, 'heatDissipation'))
    heat_exchange_type = ET.SubElement(heat_dissipation, ET.QName(nsClass.energy, 'HeatExchangeType'))
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'convectionFraction'), attrib={'uom': "scale"}).text = \
        str(usage_zone.ratio_conv_rad_persons)
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'radiantFraction'), attrib={'uom': "scale"}).text = \
        str(1 - usage_zone.ratio_conv_rad_persons)
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'totalValue'), attrib={'uom': "W"}).text = \
        str(usage_zone.fixed_heat_flow_rate_persons)
    ET.SubElement(occupants, ET.QName(nsClass.energy, 'Persons')).text = str(int(usage_zone.persons*thermal_zone.area))
    occupancy_rate = ET.SubElement(occupants, ET.QName(nsClass.energy, 'occupancyRate'))
    _set_schedule(occupancy_rate, usage_zone, usage_zone_id, "persons")

    """Machines"""
    equipped_with = ET.SubElement(gml_Usage_Zone, ET.QName(nsClass.energy, 'equippedWith'))
    electrical_app = ET.SubElement(equipped_with, ET.QName(nsClass.energy, 'ElectricalAppliances'),
                              attrib={ET.QName(nsClass.gml, 'id'): (usage_zone_id + "_Machines")})
    heat_dissipation = ET.SubElement(electrical_app, ET.QName(nsClass.energy, 'heatDissipation'))
    heat_exchange_type = ET.SubElement(heat_dissipation, ET.QName(nsClass.energy, 'HeatExchangeType'))
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'convectionFraction'), attrib={'uom': "scale"}).text = \
        str(usage_zone.ratio_conv_rad_machines)
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'radiantFraction'), attrib={'uom': "scale"}).text = \
        str(1 - usage_zone.ratio_conv_rad_machines)
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'totalValue'), attrib={'uom': "W/m2"}).text = \
        str(usage_zone.machines)

    opperation_schedule = ET.SubElement(electrical_app, ET.QName(nsClass.energy, 'operationSchedule'))
    _set_schedule(opperation_schedule, usage_zone, usage_zone_id, "machines")

    """Lighting"""
    equipped_with = ET.SubElement(gml_Usage_Zone, ET.QName(nsClass.energy, 'equippedWith'))
    electrical_app = ET.SubElement(equipped_with, ET.QName(nsClass.energy, 'LightingFacilities'),
                              attrib={ET.QName(nsClass.gml, 'id'): (usage_zone_id + "_Lighting")})
    heat_dissipation = ET.SubElement(electrical_app, ET.QName(nsClass.energy, 'heatDissipation'))
    heat_exchange_type = ET.SubElement(heat_dissipation, ET.QName(nsClass.energy, 'HeatExchangeType'))
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'convectionFraction'), attrib={'uom': "scale"}).text = \
        str(usage_zone.ratio_conv_rad_lighting)
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'radiantFraction'), attrib={'uom': "scale"}).text = \
        str(1 - usage_zone.ratio_conv_rad_lighting)
    ET.SubElement(heat_exchange_type, ET.QName(nsClass.energy, 'totalValue'), attrib={'uom': "W/m2"}).text = \
        str(usage_zone.lighting_power)
    opperation_schedule = ET.SubElement(electrical_app, ET.QName(nsClass.energy, 'operationSchedule'))
    _set_schedule(opperation_schedule, usage_zone, usage_zone_id, "lighting")


def _set_schedule(schedule_type, usage_zone, usage_zone_id, type_name):
    daily_pattern = ET.SubElement(schedule_type, ET.QName(nsClass.energy, 'DailyPatternSchedule'),
                                  attrib={ET.QName(nsClass.gml, 'id'): str(usage_zone_id + f"{type_name}_schedule")})
    ET.SubElement(daily_pattern, ET.QName(nsClass.gml, "name")).text = str(type_name)
    period_of_year = ET.SubElement(daily_pattern, ET.QName(nsClass.energy, 'periodOfYear'))
    Period_of_year = ET.SubElement(period_of_year, ET.QName(nsClass.energy, 'PeriodOfYear'))
    period = ET.SubElement(Period_of_year, ET.QName(nsClass.energy, 'period'))

    time_period = ET.SubElement(period, ET.QName(nsClass.gml, 'TimePeriod'))
    ET.SubElement(time_period, ET.QName(nsClass.gml, 'beginPosition')).text = str("2023-01-01T00:00:00")
    ET.SubElement(time_period, ET.QName(nsClass.gml, 'endPosition')).text = str("2023-12-31T00:00:00")

    daily_schedule = ET.SubElement(Period_of_year, ET.QName(nsClass.energy, 'dailySchedule'))
    Daily_schedule = ET.SubElement(daily_schedule, ET.QName(nsClass.energy, 'DailySchedule'))

    for day_type in ["weekDay", "weekEnd"]:
        ET.SubElement(Daily_schedule, ET.QName(nsClass.energy, 'dayType')).text = str(day_type)
        schedule = ET.SubElement(Daily_schedule, ET.QName(nsClass.energy, 'schedule'))
        regular_ts = ET.SubElement(schedule, ET.QName(nsClass.energy, 'RegularTimeSeries'))

        variable_props = ET.SubElement(regular_ts, ET.QName(nsClass.energy, 'variableProperties'))
        time_value_prop = ET.SubElement(variable_props, ET.QName(nsClass.energy, 'TimeValuesProperties'))
        ET.SubElement(time_value_prop, ET.QName(nsClass.energy, 'acquisitionMethod')).text = str("estimation")
        ET.SubElement(time_value_prop, ET.QName(nsClass.energy, 'interpolationType')).text = \
            str("averageInSucceedingInterval")
        ET.SubElement(time_value_prop, ET.QName(nsClass.energy, 'thematicDescription')).text = str("Nominal" + type_name)

        temporal_extant = ET.SubElement(regular_ts, ET.QName(nsClass.energy, 'temporalExtent'))
        time_period = ET.SubElement(temporal_extant, ET.QName(nsClass.gml, 'TimePeriod'))
        ET.SubElement(time_period, ET.QName(nsClass.gml, 'beginPosition')).text = str("00:00:00")
        ET.SubElement(time_period, ET.QName(nsClass.gml, 'endPosition')).text = str("00:00:23")

        ET.SubElement(regular_ts, ET.QName(nsClass.energy, 'timeInterval'), attrib={'unit': "hour"}).text = str(1)

        if type_name == "heating" or "type"=="cooling":
            uom = "K"
        if type_name == "ventilation":
            uom = "1/h"
        else:
            uom = "scale"

        if day_type is "weekDay":

            ET.SubElement(regular_ts, ET.QName(nsClass.energy, 'values'), attrib={'uom': uom}).text = str(usage_zone.schedules[f"{type_name}_profile"].iloc[0:23].values).strip('[]')

        if day_type is "weekEnd":

            ET.SubElement(regular_ts, ET.QName(nsClass.energy, 'values'), attrib={'uom': uom}).text = str(usage_zone.schedules[f"{type_name}_profile"].iloc[120:143].values).strip('[]')

    return


def _add_gml_boundary_lxml(boundary_surface, gml_id):
    """Adds a surface to the  LOD representation of the building

    Parameters
    ----------

    boundary_surface : bldg.BoundarySurfacePropertyType() object
        A boundary surface object (Roof, Wall, Floor) for one side of the bldg
    gml_id : str
        gmlID of the corresponding gml.Solid to reference the Surface

    Returns
    -------

    boundary_surface : gml.BoundarySurfacePropertyType() object
        Returns the modified boundary surface object

    """
    boundary_surface.id = "b_" + gml_id
    boundary_surface.lod2MultiSurface = gml.MultiSurfacePropertyType()
    boundary_surface.lod2MultiSurface.MultiSurface = gml.MultiSurfaceType()
    boundary_surface.lod2MultiSurface.MultiSurface.surfaceMember.append(
        gml.SurfacePropertyType())
    boundary_surface.lod2MultiSurface.MultiSurface.surfaceMember[
        -1].href = gml_id

    boundary_surface.opening.append(bldg.OpeningPropertyType())
    boundary_surface.opening[-1].Opening = bldg.Window()
    boundary_surface.opening[-1].Opening.id = gml_id + "_win"

    return boundary_surface


def save_gml(project, path, gml_copy=None, ref_coordinates=None, results=None):
    """This function saves a project to a cityGML file

    The function needs the Python Package PyXB. And the opengis bundle for GML
    and CityGML. This function underlies a lot of simplifications and
    assumptions. Be careful using it.

    Parameters
    ----------
    project: Project()
        Teaser instance of Project()
    path: string
        complete path to the output file
    gml_copy: list
        which Buildings should be outputted and the original GML copied
    results: list
        simulation results, can be saved as heating energy demands in the EnergyADE
    ref_coordinates: list
        list with  lower and one upper reference coordinates. Each coordinate
        should contain 3 ints or floats for x, y, and z coordinates of the
        point. e.g: [[458877,,5438353, -0.2], [458889,5438363,6.317669]]
    """

    if path.endswith("gml"):
        out_file = open(path, 'w')
    else:
        out_file = open(path + ".gml", 'w')

    pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(citygml.Namespace, 'core')
    pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(gml.Namespace, 'gml')
    pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(bldg.Namespace, 'bldg')
    pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(energy.Namespace, 'energy')
    pyxb.utils.domutils.BindingDOMSupport.DeclareNamespace(xlink.Namespace, 'xlink')

    gml_out = citygml.CityModel()
    gml_out.name = [og.gml.CodeType(project.name)]

    if ref_coordinates is not None:

        gml_out = _set_reference_boundary(gml_out,
                                          ref_coordinates[0],
                                          ref_coordinates[1])
    else:
        bldg_center = [0, 0, 0]
        pass

    materials = {}

    for i, bldg_count in enumerate(project.buildings):

        if gml_copy is None or re.match(r"(\w+)bt_", bldg_count.name):
            gml_out.featureMember.append(citygml.cityObjectMember())
            gml_bldg = _set_gml_building(bldg_count)

            """for testing the loop"""
            if results is not None:
                _save_simulation_results(gml_bldg, results=results)

            bldg_center = [i * 80, 0, 0]

            if type(bldg_count).__name__ == "SingleFamilyDwelling":
                building_length = (bldg_count.thermal_zones[0].area /
                                   bldg_count.thermal_zones[0].typical_width)
                building_width = bldg_count.thermal_zones[0].typical_width
                building_height = (bldg_count.number_of_floors *
                                   bldg_count.height_of_floors)

            else:
                building_width = 0.05 * (bldg_count.net_leased_area /
                                         bldg_count.number_of_floors)
                building_length = (bldg_count.net_leased_area /
                                   bldg_count.number_of_floors) / building_width
                building_height = (bldg_count.number_of_floors *
                                   bldg_count.height_of_floors)

            gml_bldg = _set_lod_2(gml_bldg,
                                  building_length,
                                  building_width,
                                  building_height,
                                  bldg_center)

        else:
            for e in range(0, len(gml_copy)):
                # if gml_copy[e].Feature.id == bldg_count.name:
                gml_out.featureMember.append(gml_copy[e])
                gml_bldg = gml_copy[e].Feature

            if results is not None:
                _save_simulation_results(gml_bldg, results=results)

        gml_out.featureMember[-1].Feature = gml_bldg

        for zone_count in bldg_count.thermal_zones:
            gml_volume = _set_gml_volume(zone_count)
            gml_zone = _set_gml_thermal_zone(zone_count)
            floor_area = _set_gml_floor_area(zone_count)
            gml_usage = _set_gml_usage(zone_count, zone_count.use_conditions)

            for out_wall_count in zone_count.outer_walls:
                thermal_openings = []
                for win_count in zone_count.windows:
                    if out_wall_count.orientation == win_count.orientation and out_wall_count.tilt == win_count.tilt:
                        thermal_openings.append(win_count)

                outer_bound = _set_gml_thermal_boundary(gml_zone, out_wall_count, thermal_openings)
                construction, material_list, openings_construction = \
                    (_set_gml_construction(outer_bound, out_wall_count, thermal_openings))
                gml_out.featureMember.append(construction)
                for open_con in openings_construction:
                    gml_out.featureMember.append(open_con)
                for mat in material_list:
                    materials.update({mat.Feature.id: mat})

            for rooftops in zone_count.rooftops:
                thermal_openings = []
                for win_count in zone_count.windows:
                    if rooftops.orientation == win_count.orientation and rooftops.tilt == win_count.tilt:
                        thermal_openings.append(win_count)

                rooftop = _set_gml_thermal_boundary(gml_zone, rooftops, thermal_openings)
                construction, material_list, openings_construction = \
                    (_set_gml_construction(rooftop, rooftops, thermal_openings))
                gml_out.featureMember.append(construction)
                for open_con in openings_construction:
                    gml_out.featureMember.append(open_con)
                for mat in material_list:
                    materials.update({mat.Feature.id: mat})

            for ground_floors in zone_count.ground_floors:
                ground_floor = _set_gml_thermal_boundary(gml_zone, ground_floors, None)
                construction, material_list, openings_construction = \
                    _set_gml_construction(ground_floor, ground_floors, None)
                gml_out.featureMember.append(construction)
                for mat in material_list:
                    materials.update({mat.Feature.id: mat})

            for in_wall_count in zone_count.inner_walls:
                in_wall = _set_gml_thermal_boundary(gml_zone, in_wall_count, None)
                construction, material_list, openings_construction = \
                    _set_gml_construction(in_wall, in_wall_count, None)
                gml_out.featureMember.append(construction)
                for mat in material_list:
                    materials.update({mat.Feature.id: mat})

            for ceilings in zone_count.ceilings:
                ceiling = _set_gml_thermal_boundary(gml_zone, ceilings, None)
                construction, material_list, openings_construction = \
                    _set_gml_construction(ceiling, ceilings, None)
                gml_out.featureMember.append(construction)
                for mat in material_list:
                    materials.update({mat.Feature.id: mat})

            for floors in zone_count.floors:
                floor = _set_gml_thermal_boundary(gml_zone, floors, None)
                construction, material_list, openings_construction = \
                    _set_gml_construction(floor, floors, None)
                gml_out.featureMember.append(construction)
                for mat in material_list:
                    materials.update({mat.Feature.id: mat})

            gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(gml_volume)
            gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(gml_zone)
            gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(gml_usage)
            gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(floor_area)

    for key in materials:
        gml_out.featureMember.append(materials[key])

    out_file.write(gml_out.toDOM().toprettyxml())


def _set_gml_building(teaser_building):
    """Creates an instance of a citygml Building with attributes

    creates a citygml.building.Building object. And fills the attributes of
    this instance with attributes of the TEASER building

    Parameters
    ----------

    teaser_building : Building Object of TEASER
        Instance of a TEASER object with set attributes

    Returns
    -------

    gml_bldg : citygml.building.Building() object
        Returns a citygml Building with attributes
    """
    gml_bldg = bldg.Building()

    gml_bldg.name = [og.gml.CodeType(teaser_building.name)]
    # gml_bldg.function = [bldg.BuildingFunctionType(1120)]
    gml_bldg.yearOfConstruction = \
        bd.datatypes.gYear(teaser_building.year_of_construction)
    # gml_bldg.roofType = bldg.RoofTypeType(1000)
    gml_bldg.measuredHeight = gml.LengthType(teaser_building.number_of_floors *
                                             teaser_building.height_of_floors)
    gml_bldg.measuredHeight.uom = bd.datatypes.anyURI('m')
    gml_bldg.storeysAboveGround = teaser_building.number_of_floors
    gml_bldg.storeyHeightsAboveGround = gml.MeasureOrNullListType(
        [teaser_building.height_of_floors] *
        int(teaser_building.number_of_floors))
    gml_bldg.storeyHeightsAboveGround.uom = bd.datatypes.anyURI('m')

    """building attributes from EnergyADE we can in principle provide"""

    gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(energy.constructionWeight(
                                                                 energy.ConstructionWeightValue.heavy))

    # gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(
    #     energy.atticType("None"))
    # gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(
    #    energy.basementType("None"))
    #    gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(
    #                    energy.constructionStyle(teaser_building.construction_type))
    # gml_bldg.GenericApplicationPropertyOfAbstractBuilding.append(
    #                energy.yearOfRefurbishment(
    #                bd.datatypes.gYear(teaser_building.year_of_construction)))

    return gml_bldg


def _set_lod_2(gml_bldg, length, width, height, bldg_center):
    """Adds a LOD 2 representation of the building based on building length,
    width and height

    alternative way to handle building position

    Parameters
    ----------

    gml_bldg : bldg.Building() object
        A building object, where bldg is a reference to
        `pyxb.bundles.opengis.citygml.building`.
    length : float
        length of the building
    width : float
        width of the building
    height : float
        height of the building
    bldg_center : list
        coordinates in the reference system of the building center

    Returns
    -------

    gml_bldg : bldg.Building() object
        Returns the modified building object

    """
    boundary_surface = []
    lod_2_solid = gml.SolidPropertyType()

    lod_2_solid.Solid = gml.Solid_()
    exterior_solid = gml.SurfacePropertyType()
    composite_surface = gml.CompositeSurface()

    bldg_center[0] -= length / 2
    bldg_center[1] -= width / 2

    # Ground surface
    coords = [[bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1], bldg_center[2]],
              [bldg_center[0], width + bldg_center[1], bldg_center[2]]]

    composite_surface = _add_surface(composite_surface, coords)
    composite_surface.surfaceMember[-1].Surface.id = gml_bldg.name[
        0].value() + "_ground"

    boundary_surface.append(bldg.BoundarySurfacePropertyType())
    boundary_surface[-1].BoundarySurface = bldg.FloorSurface()

    boundary_surface[-1].BoundarySurface = _add_gml_boundary(
        boundary_surface[-1].BoundarySurface,
        gml_bldg.name[0].value() + "_ground")

    # Roof surface
    coords = [[bldg_center[0], bldg_center[1], bldg_center[2] + height],
              [length + bldg_center[0], bldg_center[1],
               bldg_center[2] + height],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2] + height],
              [bldg_center[0], width + bldg_center[1], bldg_center[2] + height]]

    composite_surface = _add_surface(composite_surface, coords)
    composite_surface.surfaceMember[-1].Surface.id = (gml_bldg.name[0].value() +
                                                      "_roof")

    boundary_surface.append(bldg.BoundarySurfacePropertyType())
    boundary_surface[-1].BoundarySurface = bldg.RoofSurface()

    boundary_surface[-1].BoundarySurface = _add_gml_boundary(
        boundary_surface[-1].BoundarySurface,
        gml_bldg.name[0].value() + "_roof")

    # Side a surface
    coords = [[bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], bldg_center[1],
               bldg_center[2] + height],
              [bldg_center[0], bldg_center[1], bldg_center[2] + height]]

    composite_surface = _add_surface(composite_surface, coords)
    composite_surface.surfaceMember[-1].Surface.id = (gml_bldg.name[0].value() +
                                                      "_a")

    boundary_surface.append(bldg.BoundarySurfacePropertyType())
    boundary_surface[-1].BoundarySurface = bldg.WallSurface()

    boundary_surface[-1].BoundarySurface = _add_gml_boundary(
        boundary_surface[-1].BoundarySurface,
        gml_bldg.name[0].value() + "_a")

    # Side b surface

    coords = [[bldg_center[0], width + bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2] + height],
              [bldg_center[0], width + bldg_center[1], bldg_center[2] + height]]

    composite_surface = _add_surface(composite_surface, coords)
    composite_surface.surfaceMember[-1].Surface.id = (gml_bldg.name[0].value() +
                                                      "_b")

    boundary_surface.append(bldg.BoundarySurfacePropertyType())
    boundary_surface[-1].BoundarySurface = bldg.WallSurface()

    boundary_surface[-1].BoundarySurface = _add_gml_boundary(
        boundary_surface[-1].BoundarySurface,
        gml_bldg.name[0].value() + "_b")
    # Side c surface
    coords = [[bldg_center[0], bldg_center[1], bldg_center[2]],
              [bldg_center[0], width + bldg_center[1], bldg_center[2]],
              [bldg_center[0], width + bldg_center[1], bldg_center[2] + height],
              [bldg_center[0], bldg_center[1], bldg_center[2] + height]]
    composite_surface = _add_surface(composite_surface, coords)
    composite_surface.surfaceMember[-1].Surface.id = (gml_bldg.name[0].value() +
                                                      "_c")

    boundary_surface.append(bldg.BoundarySurfacePropertyType())
    boundary_surface[-1].BoundarySurface = bldg.WallSurface()

    boundary_surface[-1].BoundarySurface = _add_gml_boundary(
        boundary_surface[-1].BoundarySurface,
        gml_bldg.name[0].value() + "_c")
    # Side d surface
    coords = [[length + bldg_center[0], bldg_center[1], bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2]],
              [length + bldg_center[0], width + bldg_center[1],
               bldg_center[2] + height],
              [length + bldg_center[0], bldg_center[1],
               bldg_center[2] + height]]
    composite_surface = _add_surface(composite_surface, coords)
    composite_surface.surfaceMember[-1].Surface.id = (gml_bldg.name[0].value() +
                                                      "_d")

    boundary_surface.append(bldg.BoundarySurfacePropertyType())

    boundary_surface[-1].BoundarySurface = bldg.WallSurface()

    boundary_surface[-1].BoundarySurface = _add_gml_boundary(
        boundary_surface[-1].BoundarySurface,
        gml_bldg.name[0].value() + "_d")

    exterior_solid.Surface = composite_surface
    lod_2_solid.Solid.exterior = exterior_solid

    gml_bldg.lod2Solid = lod_2_solid
    gml_bldg.boundedBy_ = boundary_surface
    return gml_bldg


def _add_surface(composite_surface, coords):
    """Adds a surface to the  LOD representation of the building

    Parameters
    ----------

    composite_surface : gml.CompositeSurface() object
        A surface object object for one side of the building
    coords : list
        A list that contains the coordinates of the 4 points defining the
        ground area of the building. Each of the 4 list elements should consist
        of a list with 3 ints or floats for the x, y, and z coordinates of one
        point.

    Returns
    -------

    composite_surface : gml.CompositeSurface() object
        Returns the modified composite surface object

    """
    assert len(coords) == 4, 'coords must contain 4 elements'
    for coord in coords:
        assert len(coord) == 3, 'Each coord list should contain 3 elements'

    composite_surface.surfaceMember.append(gml.SurfacePropertyType())
    polygon = gml.Polygon()
    linear_ring = gml.LinearRing()
    exterior_polygon = gml.AbstractRingPropertyType(linear_ring)

    input_list = []
    for coord in coords:
        for value in coord:
            input_list.append(value)
    for value in coords[0]:
        input_list.append(value)

    pos_list = gml.posList(input_list)

    linear_ring.posList = pos_list
    exterior_polygon.LinearRing = linear_ring
    polygon.exterior = exterior_polygon

    composite_surface.surfaceMember[-1].Surface = polygon

    return composite_surface


def _add_gml_boundary(boundary_surface, gml_id):
    """Adds a surface to the  LOD representation of the building

    Parameters
    ----------

    boundary_surface : bldg.BoundarySurfacePropertyType() object
        A boundary surface object (Roof, Wall, Floor) for one side of the bldg
    gml_id : str
        gmlID of the corresponding gml.Solid to reference the Surface

    Returns
    -------

    boundary_surface : gml.BoundarySurfacePropertyType() object
        Returns the modified boundary surface object

    """
    boundary_surface.id = "b_" + gml_id
    boundary_surface.lod2MultiSurface = gml.MultiSurfacePropertyType()
    boundary_surface.lod2MultiSurface.MultiSurface = gml.MultiSurfaceType()
    boundary_surface.lod2MultiSurface.MultiSurface.surfaceMember.append(
        gml.SurfacePropertyType())
    boundary_surface.lod2MultiSurface.MultiSurface.surfaceMember[
        -1].href = gml_id

    boundary_surface.opening.append(bldg.OpeningPropertyType())
    boundary_surface.opening[-1].Opening = bldg.Window()
    boundary_surface.opening[-1].Opening.id = gml_id + "_win"

    return boundary_surface


def _set_gml_volume(thermal_zone):
    """Sets an instance of a citygml VolumeType with attributes

        creates a energy.volume() object. And fills the attributes of
        this instance with attributes of the TEASER building

        Parameters
        ----------

        thermal_zone : ThermalZone() object
        A ThermalZone object, from TEASER

        Returns
        -------

        gml_volume : energy.volume() object
            Returns a EnergyADE VolumeType with attributes
        """

    gml_volume = energy.volume()
    gml_volume.VolumeType = energy.VolumeTypeType()
    gml_volume.VolumeType.type = energy.VolumeTypeValue.grossVolume
    gml_volume.VolumeType.value_ = thermal_zone.volume
    gml_volume.VolumeType.value_.uom = bd.datatypes.anyURI('m^3')

    return gml_volume


def _set_gml_thermal_zone(thermal_zone):
    """creates a citygml.energy instance of a thermal zone

    EnergyADE includes information of a thermal zone, these values are set in
    this class.

    Parameters
    ----------

    thermal_zone : ThermalZone() object
        A ThermalZone object, from TEASER

    Returns
    -------

    gml_zone : energy.thermalZones() object
        A thermalZone object, where energy is a reference to
        `pyxb.bundles.opengis.citygml.raw.energy`.
    """

    gml_zone = energy.thermalZone()
    gml_zone.AbstractThermalZone = energy.ThermalZone()

    gml_zone.AbstractThermalZone.id = thermal_zone.name
    gml_zone.AbstractThermalZone.isCooled = bd.datatypes.boolean(False)
    gml_zone.AbstractThermalZone.isHeated = bd.datatypes.boolean(True)
    gml_zone.AbstractThermalZone.infiltrationRate = gml.MeasureType(
        thermal_zone.infiltration_rate)
    gml_zone.AbstractThermalZone.infiltrationRate.uom = bd.datatypes.anyURI('1/h')

    return gml_zone


def _set_gml_usage(thermal_zone, boundary_conditions):
    """Sets an instance of a EnergyADE UsageZone with attributes

            creates a UsageZone object. And fills the attributes of
            this instance with attributes of the TEASER building, UseConditions

            Parameters
            ----------

            thermal_zone : ThermalZone() object
            A ThermalZone object, from TEASER

            Returns
            -------

            gml_usage : energy.usageZone() object
        A usageZone object, where energy is a reference to
        `pyxb.bundles.opengis.citygml.raw.energy`
            """

    gml_usage = energy.usageZone()
    gml_usage.AbstractUsageZone = energy.UsageZone()
    gml_usage.AbstractUsageZone.usageZoneType = thermal_zone.name

    """Heating Schedule"""
    gml_usage.AbstractUsageZone.heatingSchedule = energy.AbstractSchedulePropertyType()
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule = \
        energy.DailyPatternSchedule()
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule.name = \
        [og.gml.CodeType("Heating Schedule")]
    """periodOfYear[] / PeriodOfYear"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear.append(energy.PeriodOfYearPropertyType())
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear = energy.PeriodOfYearType()
    """period"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.period = gml.TimePeriodPropertyType()
    """dailySchedule[] / DailySchedule"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule.append(energy.DailySchedulePropertyType())
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule = energy.DailyScheduleType()
    """dayType"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.dayType = "typicalDay"
    """schedule / RegularTimeSeries"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule = energy.AbstractTimeSeriesPropertyType()
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries = \
        energy.RegularTimeSeries()
    """Typical Schedule values: combination of heating_time, set_temp_heat and temp_set_back (night set-back)"""
    heating_profile = []
    for i in range(0, 23):
        heating_profile.append(boundary_conditions.set_temp_heat - boundary_conditions.temp_set_back - 273.15)
    for i in range(boundary_conditions.heating_time[0], boundary_conditions.heating_time[1]):
        heating_profile[i] = boundary_conditions.set_temp_heat - 273.15

    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.values = \
        heating_profile
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.values.uom = \
        bd.datatypes.anyURI('scale')
    """variable Properties"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties = \
        energy.TimeValuesPropertiesPropertyType()
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties. \
        interpolationType = "averageInSucceedingInterval"
    """temporalExtend/ period of messure"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.temporalExtent = \
        gml.TimePeriodPropertyType()
    """time Interval"""
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval = 1
    gml_usage.AbstractUsageZone.heatingSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval.unit = \
        bd.datatypes.anyURI('hour')


    """Persons / OccupiedBy"""
    gml_usage.AbstractUsageZone.occupiedBy.append(energy.OccupantsPropertyType(energy.Occupants()))
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.id = "Occupants_" + str(boundary_conditions.internal_id)
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.numberOfOccupants = round(boundary_conditions.persons)

    """Occupant Heat Dissipation"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation = energy.HeatExchangeTypePropertyType()
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation.HeatExchangeType = energy.HeatExchangeType()
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation.HeatExchangeType.convectiveFraction = \
        boundary_conditions.ratio_conv_rad_persons
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation.HeatExchangeType.convectiveFraction.uom = \
        bd.datatypes.anyURI('scale')
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation.HeatExchangeType.radiantFraction = \
        1 - boundary_conditions.ratio_conv_rad_persons
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation.HeatExchangeType.radiantFraction.uom = \
        bd.datatypes.anyURI('scale')
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation.HeatExchangeType.totalValue = \
        100  # AixLib: currently not used, it is always set to 100 W/person
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.heatDissipation.HeatExchangeType.totalValue.uom = \
        bd.datatypes.anyURI('W/person')

    # TODO: finish / add period, variable Properties and temporal Extend
    """Occupant Profile"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate = energy.AbstractSchedulePropertyType()
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule = \
        energy.DailyPatternSchedule()
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule.name = \
        [og.gml.CodeType("Occupant_Profile")]
    """periodOfYear[] / PeriodOfYear"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule.\
        periodOfYear.append(energy.PeriodOfYearPropertyType())
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear = energy.PeriodOfYearType()
    """period"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.period = gml.TimePeriodPropertyType()
    """dailySchedule[] / DailySchedule"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule.append(energy.DailySchedulePropertyType())
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule = energy.DailyScheduleType()
    """dayType"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.dayType = "typicalDay"
    """schedule / RegularTimeSeries"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule = energy.AbstractTimeSeriesPropertyType()
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries = \
        energy.RegularTimeSeries()
    """values"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.values = \
        boundary_conditions.profile_persons
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.values.uom = \
        bd.datatypes.anyURI('scale')
    """variable Properties"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties =\
        energy.TimeValuesPropertiesPropertyType()
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties.\
        interpolationType = "averageInSucceedingInterval"
    """temporalExtend/ period of messure"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.temporalExtent =\
        gml.TimePeriodPropertyType()
    """time Interval"""
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval = 1
    gml_usage.AbstractUsageZone.occupiedBy[-1].Occupants.occupancyRate.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval.unit =\
        bd.datatypes.anyURI('hour')

    """equippedWith / ElectricalAppliances / Machines"""
    gml_usage.AbstractUsageZone.equippedWith.append(energy.FacilitiesPropertyType(energy.ElectricalAppliances()))
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.id = "Machines_" + str(boundary_conditions.internal_id)

    "Machines Heat Dissipation"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation = energy.HeatExchangeTypePropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType = energy.HeatExchangeType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.convectiveFraction = \
        boundary_conditions.ratio_conv_rad_machines
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.convectiveFraction.uom = \
        bd.datatypes.anyURI('scale')
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.radiantFraction = \
        1 - boundary_conditions.ratio_conv_rad_machines
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.radiantFraction.uom = \
        bd.datatypes.anyURI('scale')
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.totalValue = \
        boundary_conditions.machines * thermal_zone.area  # machines[W/m²] AixLib: activityType
    # currently not used, it is always set to 100 W/machine VDI 2078
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.totalValue.uom = \
        bd.datatypes.anyURI('W')

    # TODO: finish / add period, variable Properties and temporal Extend
    """Machine Profile"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule = energy.AbstractSchedulePropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule = \
        energy.DailyPatternSchedule()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule.name = \
        [og.gml.CodeType("Machine_Profile")]
    """periodOfYear[] / PeriodOfYear"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear.append(energy.PeriodOfYearPropertyType())
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear = energy.PeriodOfYearType()
    """period"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.period = gml.TimePeriodPropertyType()
    """dailySchedule[] / DailySchedule"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule.append(energy.DailySchedulePropertyType())
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule = energy.DailyScheduleType()
    """dayType"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.dayType = "typicalDay"
    """schedule / RegularTimeSeries"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule = energy.AbstractTimeSeriesPropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries = \
        energy.RegularTimeSeries()
    """values"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[
        -1].DailySchedule.schedule.AbstractTimeSeries.values = boundary_conditions.profile_machines
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[
        -1].DailySchedule.schedule.AbstractTimeSeries.values.uom = bd.datatypes.anyURI('scale')
    """variable Properties"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties = \
        energy.TimeValuesPropertiesPropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties. \
        interpolationType = "averageInSucceedingInterval"
    """temporalExtend/ period of messure"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.temporalExtent = \
        gml.TimePeriodPropertyType()
    """time Interval"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval = 1
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval.unit = \
        bd.datatypes.anyURI("hour")

    """equippedWith / ElectricalAppliances / Lighting"""
    gml_usage.AbstractUsageZone.equippedWith.append(energy.FacilitiesPropertyType(energy.LightingFacilities()))
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.id = "Lighting_" + str(boundary_conditions.internal_id)

    """Lighting Heat Dissipation"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation = energy.HeatExchangeTypePropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType = energy.HeatExchangeType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.convectiveFraction = \
        boundary_conditions.ratio_conv_rad_persons
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.convectiveFraction.uom = \
        bd.datatypes.anyURI('scale')
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.radiantFraction = \
        1 - boundary_conditions.ratio_conv_rad_persons
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.radiantFraction.uom = \
        bd.datatypes.anyURI('scale')
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.totalValue = \
        boundary_conditions.lighting_power   # lighting_power : float [W/m2]
    # spec. electr. Power for lighting. This value is taken from SIA 2024
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.heatDissipation.HeatExchangeType.totalValue.uom = \
        bd.datatypes.anyURI('W/m^2')

    # TODO: finish / add period, variable Properties and temporal Extend
    """Lighting Profile"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule = energy.AbstractSchedulePropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule = \
        energy.DailyPatternSchedule()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule.name = \
        [og.gml.CodeType("Lighting_Profile")]
    """periodOfYear[] / PeriodOfYear"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear.append(energy.PeriodOfYearPropertyType())
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear = energy.PeriodOfYearType()
    """period"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.period = gml.TimePeriodPropertyType()
    """dailySchedule[] / DailySchedule"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule.append(energy.DailySchedulePropertyType())
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule = energy.DailyScheduleType()
    """dayType"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.dayType = "typicalDay"
    """schedule / RegularTimeSeries"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule = energy.AbstractTimeSeriesPropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries = \
        energy.RegularTimeSeries()
    """values"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[
        -1].DailySchedule.schedule.AbstractTimeSeries.values = boundary_conditions.profile_lighting
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[
        -1].DailySchedule.schedule.AbstractTimeSeries.values.uom = bd.datatypes.anyURI('scale')
    """variable Properties"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties = \
        energy.TimeValuesPropertiesPropertyType()
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.variableProperties. \
        interpolationType = "averageInSucceedingInterval"
    """temporalExtend/ period of messure"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.temporalExtent = \
        gml.TimePeriodPropertyType()
    """time Interval"""
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval = 1
    gml_usage.AbstractUsageZone.equippedWith[-1].Facilities.operationSchedule.AbstractSchedule. \
        periodOfYear[-1].PeriodOfYear.dailySchedule[-1].DailySchedule.schedule.AbstractTimeSeries.timeInterval.unit = \
        bd.datatypes.anyURI("hour")

    return gml_usage


def _set_gml_floor_area(thermal_zone):
    """Sets an instance of a citygml FloorAreaType with attributes

            creates a energy.volume() object. And fills the attributes of
            this instance with attributes of the TEASER building

            Parameters
            ----------

            thermal_zone : ThermalZone() object
            A ThermalZone object, from TEASER

            Returns
            -------

            gml_volume : energy.floorArea() object
                Returns a EnergyADE floorType with attributes
            """

    floor_area = energy.floorArea()
    floor_area.FloorArea = energy.FloorAreaType()
    floor_area.FloorArea.type = energy.FloorAreaTypeValue.netFloorArea
    floor_area.FloorArea.value_ = thermal_zone.area
    floor_area.FloorArea.value_.uom = bd.datatypes.anyURI('m^2')

    return floor_area


def _set_gml_thermal_boundary(gml_zone, wall, thermal_openings):
    """Control function to add a thermal boundary surface to the thermal zone

    The thermal zone instance of citygml is modified and thermal boundary
    surfaces are added. The thermal boundaries are chosen according to their
    type (OuterWall, InnerWall, Roof, etc.). For outer walls (including roof)
    the thermal boundary is returned to add windows (Thermal Openings).

    Parameters
    ----------

    gml_zone : energy.thermalZones() object
        A thermalZone object, where energy is a reference to
        `pyxb.bundles.opengis.citygml.energy`.

    wall : TEASER instance of Wall()
        Teaser instance of Wall or its inherited classes

    thermal_openings: List of TEASER instances of Window() or Door()
        Teaser instance of BuildingElement or its inherited classes
    Returns
    ----------

    _current_tb : energy.ThermalBoundarySurface()
        A ThermalBoundarySurface object with semantic information
        (area, azimuth, inclination etc.)

    """
    _current_tb = None
    if type(wall).__name__ == "OuterWall":

        gml_zone.AbstractThermalZone.boundedBy_.append(energy.ThermalBoundaryPropertyType())
        gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary = energy.ThermalBoundaryType()

        _current_tb = gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary
        _current_tb.thermalBoundaryType = energy.ThermalBoundaryTypeValue("outerWall")
        _current_tb.id = "GML_" + str(wall.internal_id)
        _current_tb.azimuth = gml.AngleType(wall.orientation)
        _current_tb.azimuth.uom = bd.datatypes.anyURI('deg')
        _current_tb.inclination = gml.AngleType(wall.tilt)
        _current_tb.inclination.uom = bd.datatypes.anyURI('deg')
        _current_tb.area = gml.AreaType(wall.area)
        _current_tb.area.uom = bd.datatypes.anyURI('m^2')
        _current_tb.delimits.append(energy.ThermalZonePropertyType())
        _current_tb.delimits[-1].href = gml_zone.AbstractThermalZone.id

        if thermal_openings is not None:
            for thermal_opening in thermal_openings:
                _current_tb.contains.append(energy.ThermalOpeningPropertyType(energy.ThermalOpening()))
                _current_tb.contains[-1].ThermalOpening.id = "GML_" + str(thermal_opening.internal_id)
                _current_tb.contains[-1].ThermalOpening.area = gml.AreaType(thermal_opening.area)
                _current_tb.contains[-1].ThermalOpening.area.uom = bd.datatypes.anyURI('m^2')

        return _current_tb

    elif type(wall).__name__ == "Rooftop":

        gml_zone.AbstractThermalZone.boundedBy_.append(energy.ThermalBoundaryPropertyType())
        gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary = energy.ThermalBoundaryType()

        _current_tb = gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary
        _current_tb.thermalBoundaryType = energy.ThermalBoundaryTypeValue("roof")
        _current_tb.id = "GML_" + str(wall.internal_id)
        _current_tb.azimuth = gml.AngleType(wall.orientation)
        _current_tb.azimuth.uom = bd.datatypes.anyURI('deg')
        _current_tb.inclination = gml.AngleType(wall.tilt)
        _current_tb.inclination.uom = bd.datatypes.anyURI('deg')
        _current_tb.area = gml.AreaType(wall.area)
        _current_tb.area.uom = bd.datatypes.anyURI('m^2')
        _current_tb.delimits.append(energy.ThermalZonePropertyType())
        _current_tb.delimits[-1].href = gml_zone.AbstractThermalZone.id

        if thermal_openings is not None:
            for thermal_opening in thermal_openings:
                _current_tb.contains.append(energy.ThermalOpeningPropertyType(energy.ThermalOpening()))
                _current_tb.contains[-1].ThermalOpening.id = "GML_" + str(thermal_opening.internal_id)
                _current_tb.contains[-1].ThermalOpening.area = gml.AreaType(thermal_opening.area)
                _current_tb.contains[-1].ThermalOpening.area.uom = bd.datatypes.anyURI('m^2')

        return _current_tb

    elif type(wall).__name__ == "GroundFloor":

        gml_zone.AbstractThermalZone.boundedBy_.append(energy.ThermalBoundaryPropertyType())
        gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary = energy.ThermalBoundaryType()

        _current_tb = gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary
        _current_tb.thermalBoundaryType = energy.ThermalBoundaryTypeValue("groundSlab")
        _current_tb.id = "GML_" + str(wall.internal_id)
        _current_tb.azimuth = gml.AngleType(wall.orientation)
        _current_tb.azimuth.uom = bd.datatypes.anyURI('deg')
        _current_tb.inclination = gml.AngleType(wall.tilt)
        _current_tb.inclination.uom = bd.datatypes.anyURI('deg')
        _current_tb.area = gml.AreaType(wall.area)
        _current_tb.area.uom = bd.datatypes.anyURI('m^2')
        _current_tb.delimits.append(energy.ThermalZonePropertyType())
        _current_tb.delimits[-1].href = gml_zone.AbstractThermalZone.id

        return _current_tb

    elif type(wall).__name__ == "InnerWall" or type(wall).__name__ == "Ceiling" or type(wall).__name__ == "Floor":

        gml_zone.AbstractThermalZone.boundedBy_.append(energy.ThermalBoundaryPropertyType())
        gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary = energy.ThermalBoundaryType()

        _current_tb = gml_zone.AbstractThermalZone.boundedBy_[-1].ThermalBoundary
        if type(wall).__name__ == "Ceiling" or type(wall).__name__ == "Floor":
            _current_tb.thermalBoundaryType = energy.ThermalBoundaryTypeValue("intermediaryFloor")
        else:
            _current_tb.thermalBoundaryType = energy.ThermalBoundaryTypeValue("interiorWall")
        _current_tb.id = "GML_" + str(wall.internal_id)
        _current_tb.azimuth = gml.AngleType(wall.orientation)
        _current_tb.azimuth.uom = bd.datatypes.anyURI('deg')
        _current_tb.inclination = gml.AngleType(wall.tilt)
        _current_tb.inclination.uom = bd.datatypes.anyURI('deg')
        _current_tb.area = gml.AreaType(wall.area)
        _current_tb.area.uom = bd.datatypes.anyURI('m^2')
        _current_tb.delimits.append(energy.ThermalZonePropertyType())
        _current_tb.delimits[-1].href = gml_zone.AbstractThermalZone.id

        # _set_gml_surface_component(_current_tb, wall, sun_exp="false", grnd_coupled="false")
        # _set_gml_construction(_current_tb, wall)

        return _current_tb

    else:
        print("Strange Wall Surface detected!")


def _set_gml_construction(thermal_boundary, element, contained_element):
    """Adds a surface construction to a citygml thermal_boundary

        A surface construction is needed to store semantic information. This function
        adds a surface construction to be filled with layers. It does not return the surface.

        Parameters
        ----------

        thermal_boundary : energy.ThermalBoundary()
            A ThermalBoundarySurface object
        element : TEASER BuildingElement
            Instance of BuilingElement or inherited classes
        contained_element : TEASER BuildingElement
            Window or Door class - ThermalOpening in
            ThermalBoundary

        Returns
        ----------
        cons: gml:featureProperty()
            construction featureMember
        material_list: list of featureProperty()'s
            material featureMembers
        cons_openings_list: list of featureProperty()'s
            material featureMembers of ThermalOpenings
        """
    cons = gml.featureProperty()
    cons.Feature = energy.Construction()
    cons.Feature.id = thermal_boundary.id + "_cons"

    thermal_boundary.construction = energy.AbstractConstructionPropertyType()
    thermal_boundary.construction.href = "#" + cons.Feature.id

    cons.Feature.name = [og.gml.CodeType(thermal_boundary.thermalBoundaryType + "_construction")]
    cons.Feature.uValue = gml.MeasureType(element.ua_value / element.area)
    cons.Feature.uValue.uom = bd.datatypes.anyURI('W/(m^2*K)')

    material_list = _add_gml_layer(cons.Feature.id, cons.Feature.layer, element)

    if contained_element is not None:
        cons_openings_list = []
        for thermal_opening in thermal_boundary.contains:
            for con_elem in contained_element:
                if thermal_opening.ThermalOpening.id == "GML_" + str(con_elem.internal_id):

                    cons_openings = gml.featureProperty()
                    cons_openings.Feature = energy.Construction()
                    cons_openings.Feature.id = thermal_opening.ThermalOpening.id + "_cons"

                    thermal_opening.ThermalOpening.construction = energy.AbstractConstructionPropertyType()
                    thermal_opening.ThermalOpening.construction.href = "#" + cons_openings.Feature.id

                    cons_openings.Feature.name = [og.gml.CodeType(thermal_boundary.thermalBoundaryType
                                                                  + type(con_elem).__name__ + "_construction")]
                    cons_openings.Feature.uValue = gml.MeasureType(element.ua_value / element.area)
                    cons_openings.Feature.uValue.uom = bd.datatypes.anyURI('W/(m^2*K)')

                    cons_openings.Feature.opticalProperties = energy.OpticalPropertiesPropertyType()
                    cons_openings.Feature.opticalProperties.append(energy.OpticalPropertiesType())
                    cons_openings.Feature.opticalProperties.OpticalProperties.glazingRatio = 0.7
                    cons_openings.Feature.opticalProperties.OpticalProperties.glazingRatio.uom = \
                        bd.datatypes.anyURI('scale')
                    cons_openings.Feature.opticalProperties.OpticalProperties.transmittance.\
                        append(energy.TransmittancePropertyType())
                    cons_openings.Feature.opticalProperties.OpticalProperties.transmittance[
                        -1].Transmittance = energy.TransmittanceType()
                    cons_openings.Feature.opticalProperties.OpticalProperties.transmittance[
                        -1].Transmittance.fraction = con_elem.g_value
                    cons_openings.Feature.opticalProperties.OpticalProperties \
                        .transmittance[-1].Transmittance.fraction.uom = bd.datatypes.anyURI('scale')
                    cons_openings.Feature.opticalProperties.OpticalProperties \
                        .transmittance[-1].Transmittance.wavelengthRange = energy.WavelengthRangeType("solar")

                    cons_openings_list.append(cons_openings)
    else:
        cons_openings_list = None

    return cons, material_list, cons_openings_list


def _add_gml_layer(cons_id, cons_comp, element):
    """Adds gml layer to a surface component

    Adds all layer of the element to the gml surface component
    Currently only LayerComponent per Layer, so AreaFraction is
    always 1. As far as I know, same limitation in TEASER itself.
    So Layer_id is the same as layerComponent_id
    Parameters
    ----------
    cons_id : energy.ConstructionType.id
        For layer_id purposes
    cons_comp : energy.LayerPropertyType
        A LayerPropertyType object holds layer and LayerComponents
    element : TEASER BuildingElement
        Instance of BuilingElement or inherited classes
    Returns
    ----------

    material_list: list of featureProperty()'s
            material featureMembers
    """

    material_list = []

    for lay_count in element.layer:
        layer = energy.LayerPropertyType()
        layer.Layer = energy.LayerType()
        layer.Layer.id = cons_id + "_TEASER_L_ID_" + str(lay_count.id)
        layer.Layer.layerComponent.append(energy.LayerComponentPropertyType())
        layer.Layer.layerComponent[-1].LayerComponent = energy.LayerComponentType()

        _current_layer = layer.Layer.layerComponent[-1].LayerComponent
        _current_layer.id = cons_id + "_TEASER_L_ID_" + str(lay_count.id)
        _current_layer.areaFraction = 1
        _current_layer.areaFraction.uom = bd.datatypes.anyURI('scale')
        _current_layer.thickness = gml.LengthType(lay_count.thickness)
        _current_layer.thickness.uom = bd.datatypes.anyURI('m')

        cons_comp.append(layer)

        material_list.append(_add_gml_opaque_material(_current_layer, lay_count))

    return material_list


def _add_gml_opaque_material(gml_layer, teaser_layer):
    """Adds gml opaque material to the given layer

    Adds a material to given layer and fills information with teaser
    information

    Parameters
    ----------

    gml_layer : energy.LayerComponentType()
        A Layer object with basic data
    teaser_layer : TEASER Layer
        Instance of Layer
     Returns
    ----------

    mat: featureProperty()
        material featureMember
    """

    mat = gml.featureProperty()
    mat.Feature = energy.SolidMaterial()
    _current_material = mat.Feature
    _current_material.id = "UUID_" + str(teaser_layer.material.material_id)
    _current_material.name = [og.gml.CodeType(teaser_layer.material.name)]
    _current_material.conductivity = gml.MeasureType(teaser_layer.material.thermal_conduc)
    _current_material.conductivity.uom = bd.datatypes.anyURI('W/mK')
    _current_material.density = gml.MeasureType(teaser_layer.material.density)
    _current_material.density.uom = bd.datatypes.anyURI('kg/m^3')
    _current_material.specificHeat = gml.MeasureType(teaser_layer.material.heat_capac)
    _current_material.specificHeat.uom = bd.datatypes.anyURI('kJ/kg')

    gml_layer.material = energy.AbstractMaterialPropertyType()
    gml_layer.material.href = "#UUID_" + str(teaser_layer.material.material_id)

    return mat


def _save_simulation_results(gml_bldg, results):

    demands = energy.demands()
    demands.EnergyDemand = energy.EnergyDemandType()
    demands.EnergyDemand.endUse = "spaceHeating"
    demands.EnergyDemand.energyAmount = energy.AbstractTimeSeriesPropertyType()
    demands.EnergyDemand.energyAmount.AbstractTimeSeries = energy.RegularTimeSeries()
    demands.EnergyDemand.energyAmount.AbstractTimeSeries.values = results
    demands.EnergyDemand.energyAmount.AbstractTimeSeries.values.uom = "kWh"
    demands.EnergyDemand.energyAmount.AbstractTimeSeries.variableProperties = energy.TimeValuesPropertiesPropertyType()
    demands.EnergyDemand.energyAmount.AbstractTimeSeries.variableProperties\
        .interpolationType = "averageInSucceedingInterval"
    demands.EnergyDemand.energyAmount.AbstractTimeSeries.temporalExtent = gml.TimePeriodPropertyType()
    demands.EnergyDemand.energyAmount.AbstractTimeSeries.timeInterval = 1
    demands.EnergyDemand.energyAmount.AbstractTimeSeries.timeInterval.unit = bd.datatypes.anyURI("hour")
    gml_bldg.GenericApplicationPropertyOfCityObject.append(demands)
