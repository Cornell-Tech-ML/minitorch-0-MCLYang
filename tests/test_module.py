import minitorch
import pytest

# import pdb


VAL = 40


class Module1(minitorch.Module):
    def __init__(self):
        super().__init__()
        self.module_a = Module2(5)
        self.module_b = Module2(10)
        self.parameter_a = minitorch.Parameter(VAL)


VAL_A = 50
VAL_B = 100


class Module2(minitorch.Module):
    def __init__(self, extra=0):
        super().__init__()
        self.parameter_a = minitorch.Parameter(VAL_A)
        self.parameter_b = minitorch.Parameter(VAL_B)
        self.non_parameter = 10
        for i in range(extra):
            self.add_parameter(f"extra_parameter_{i}", None)


@pytest.mark.task0_4
def test_module():
    "Check the properties of a single module"
    module = Module2()
    module.eval()
    assert module.mode == "eval"
    module.train()
    assert module.mode == "train"
    assert len(module.parameters()) == 2

    module = Module2(10)
    assert len(module.parameters()) == 12

    module = Module2(5)
    named_parameters = module.named_parameters()
    assert named_parameters["parameter_a"].value == VAL_A
    assert named_parameters["parameter_b"].value == VAL_B
    assert named_parameters["extra_parameter_0"].value is None


@pytest.mark.task0_4
def test_stacked_module():
    "Check the properties of a stacked module"
    module = Module1()
    print(module)
    module.eval()
    assert module.mode == "eval"
    assert module.module_a.mode == "eval"
    assert module.module_b.mode == "eval"
    module.train()
    assert module.mode == "train"
    assert module.module_a.mode == "train"
    assert module.module_b.mode == "train"

    assert len(module.parameters()) == 1 + 7 + 12

    named_parameters = module.named_parameters()
    # pdb.set_trace()
    assert named_parameters["parameter_a"].value == VAL
    assert named_parameters["module_a.parameter_a"].value == VAL_A
    assert named_parameters["module_a.parameter_b"].value == VAL_B
    assert named_parameters["module_b.parameter_a"].value == VAL_A
    assert named_parameters["module_b.parameter_b"].value == VAL_B


class ModuleA1(minitorch.Module):
    def __init__(self):
        super().__init__()
        self.p1 = minitorch.Parameter(5)
        self.a = ModuleA2()
        self.b = ModuleA3()


class ModuleA2(minitorch.Module):
    def __init__(self):
        super().__init__()
        self.p2 = minitorch.Parameter(10)


class ModuleA3(minitorch.Module):
    def __init__(self):
        super().__init__()
        self.c = ModuleA4()


class ModuleA4(minitorch.Module):
    def __init__(self):
        super().__init__()
        self.p3 = minitorch.Parameter(15)


@pytest.mark.task0_4
def test_stacked_module2():
    np = ModuleA1().named_parameters()
    assert np["p1"].value == 5
    assert np["a.p2"].value == 10
    assert np["b.c.p3"].value == 15
