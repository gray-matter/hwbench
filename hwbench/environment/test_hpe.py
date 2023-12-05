import pathlib
from .vendors.vendor import MonitorMetric, Temperature, ThermalContext, FanContext
from .vendors.hpe.hpe import Hpe, ILO
from .test_vendors import TestVendors, PATCH_TYPES

path = pathlib.Path("")


class TestGenericHpe(TestVendors):
    def __init__(self, thermal: str, *args, **kwargs):
        super().__init__(Hpe("", None), *args, **kwargs)
        self.thermal = thermal

    def setUp(self):
        # setUp is called by pytest to install patches
        # Prepare the vendor specifics
        self.install_patch(
            "hwbench.environment.vendors.hpe.hpe.Hpe.detect",
            PATCH_TYPES.RETURN_VALUE,
            True,
        )
        self.install_patch(
            "hwbench.environment.vendors.hpe.hpe.ILO.run",
            PATCH_TYPES.RETURN_VALUE,
            True,
        )
        self.install_patch(
            "hwbench.environment.vendors.hpe.hpe.ILO.get_thermal",
            PATCH_TYPES.RETURN_VALUE,
            self.sample(self.thermal),
        )
        self.get_vendor().bmc = ILO("", self.get_vendor(), None)
        # And finish by calling the parent setUp()
        super().setUp()


class TestHpeAp2K(TestGenericHpe):
    def __init__(self, *args, **kwargs):
        super().__init__("tests/vendors/Hpe/XL225N/thermal", *args, **kwargs)

    def test_thermal(self):
        expected_output = self.generic_thermal_output()
        expected_output["Intake"]["01-Inlet Ambient"] = Temperature("Inlet", 23)
        expected_output["CPU"] = {
            "02-CPU 1": Temperature("CPU1", 40),
            "55-CPU 1 PkgTmp": Temperature("CPU1", 36),
        }
        expected_output["Memory"] = {
            "04-P1 DIMM 1-4": Temperature("P1 DIMM 1-4", 28),
            "05-P1 DIMM 5-8": Temperature("P1 DIMM 5-8", 28),
        }

        super().generic_thermal_test(expected_output)

    def test_fan(self):
        expected_output = self.generic_fan_output()
        expected_output[str(FanContext.FAN)] = {
            "Fan 1": MonitorMetric("Fan 1", 47, "Percent"),
            "Fan 2": MonitorMetric("Fan 2", 47, "Percent"),
            "Fan 3": MonitorMetric("Fan 3", 0, "Percent"),
            "Fan 4": MonitorMetric("Fan 4", 47, "Percent"),
            "Fan 5": MonitorMetric("Fan 5", 0, "Percent"),
            "Fan 6": MonitorMetric("Fan 6", 48, "Percent"),
            "Fan 7": MonitorMetric("Fan 7", 48, "Percent"),
        }

        super().generic_fan_test(expected_output)


class TestHpeDL380(TestGenericHpe):
    def __init__(self, *args, **kwargs):
        super().__init__("tests/vendors/Hpe/DL380/thermal", *args, **kwargs)

    def test_thermal(self):
        expected_output = self.generic_thermal_output()
        expected_output[str(ThermalContext.INTAKE)] = {
            "01-Inlet Ambient": Temperature("Inlet", 24)
        }
        expected_output[str(ThermalContext.CPU)] = {
            "02-CPU 1": Temperature("CPU1", 40),
            "03-CPU 2": Temperature("CPU2", 40),
            "96-CPU 1 PkgTmp": Temperature("CPU1", 41),
            "97-CPU 2 PkgTmp": Temperature("CPU2", 37),
        }
        expected_output[str(ThermalContext.MEMORY)] = {
            "04-P1 DIMM 1-6": Temperature("P1 DIMM 1-6", 35),
            "06-P1 DIMM 7-12": Temperature("P1 DIMM 7-12", 35),
            "08-P2 DIMM 1-6": Temperature("P2 DIMM 1-6", 36),
            "10-P2 DIMM 7-12": Temperature("P2 DIMM 7-12", 35),
        }
        super().generic_thermal_test(expected_output)

    def test_fan(self):
        expected_output = self.generic_fan_output()
        expected_output[str(FanContext.FAN)] = {
            "Fan 1": MonitorMetric("Fan 1", 25, "Percent"),
            "Fan 2": MonitorMetric("Fan 2", 28, "Percent"),
            "Fan 3": MonitorMetric("Fan 3", 25, "Percent"),
            "Fan 4": MonitorMetric("Fan 4", 25, "Percent"),
            "Fan 5": MonitorMetric("Fan 5", 25, "Percent"),
            "Fan 6": MonitorMetric("Fan 6", 25, "Percent"),
        }

        super().generic_fan_test(expected_output)