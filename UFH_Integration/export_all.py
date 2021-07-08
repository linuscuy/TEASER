from teaser.project import Project
from teaser.logic.buildingobjects.building import Building
from teaser.logic.buildingobjects.thermalzone import ThermalZone
from teaser.logic.buildingobjects.useconditions import UseConditions
from teaser.logic.buildingobjects.buildingphysics.outerwall import OuterWall
from teaser.logic.buildingobjects.buildingphysics.floor import Floor
from teaser.logic.buildingobjects.buildingphysics.rooftop import Rooftop
from teaser.logic.buildingobjects.buildingphysics.groundfloor import GroundFloor
from teaser.logic.buildingobjects.buildingphysics.window import Window
from teaser.logic.buildingobjects.buildingphysics.innerwall import InnerWall
from teaser.logic.buildingobjects.buildingphysics.layer import Layer
from teaser.logic.buildingobjects.buildingphysics.material import Material


class ExportAll:

    def run(self):
        prj = self.create_project('All_Exporter_as_Walls_no_floors')
        bldg = self.create_building(prj, 'SimpleBuilding', 2015, 1, 20)
        tz = self.create_thermal_zone(bldg, "Bed room", "tz_1", 20, 3)
        wall_1 = self.create_instance(OuterWall, tz, 5, 0, bldg.year_of_construction, "light")
        wall_2 = self.create_instance(OuterWall, tz, 4, 90, bldg.year_of_construction, "light")
        wall_3 = self.create_instance(OuterWall, tz, 5, 180, bldg.year_of_construction, "light")
        wall_4 = self.create_instance(OuterWall, tz, 4, 270, bldg.year_of_construction, "light")
        ceiling = self.create_instance(OuterWall, tz, 20, -1, bldg.year_of_construction, "light")
        # floor = self.create_instance(OuterWall, tz, 20, -1, bldg.year_of_construction, "light")
        win = self.create_instance(Window, tz, 0.001, 0, bldg.year_of_construction, "EnEv")
        tz.calc_zone_parameters()
        bldg.calc_building_parameter()
        prj.export_aixlib()
        print()

    @staticmethod
    def create_project(name):
        prj = Project(load_data=True)
        prj.name = name
        prj.data.load_uc_binding()
        prj.number_of_elements_calc = 2
        return prj

    @staticmethod
    def create_building(project, name, year_of_construction, n_floors, net_area):
        bldg = Building(parent=project)
        bldg.used_library_calc = 'AixLib'
        bldg.name = name
        bldg.year_of_construction = year_of_construction
        bldg.number_of_floors = n_floors
        bldg.net_leased_area = net_area
        return bldg

    @staticmethod
    def create_thermal_zone(bldg, use_condition, name, area, height):
        tz = ThermalZone(parent=bldg)
        tz.use_conditions = UseConditions(parent=tz)
        tz.use_conditions.load_use_conditions(use_condition)
        tz.name = name
        tz.area = area
        tz.volume = area*height
        tz.number_of_elements = 2
        return tz

    @staticmethod
    def create_instance(class_instance, tz, area, orientation, year_of_construction, construction):
        inst = class_instance(parent=tz)
        inst.load_type_element(year_of_construction, construction)
        inst.area = area
        inst.orientation = orientation

        return inst


if __name__ == "__main__":
    export = ExportAll()
    export.run()
