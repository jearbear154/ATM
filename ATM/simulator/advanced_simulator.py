from simulator.atm_simulator import ATMSimulator

"""
AdvancedSimulator --- class to simulate an ATM on an input x with time and space restrictions
:author Jeremy McMahan
"""


class AdvancedSimulator:
    """
    Simulates M on x with time and space bounds
    :param M the ATM to simulate
    :param x the input for M
    :param T the time bound that M must run in
    :param S the space bound that M must run in
    :returns an accepting ComputationTree if one exists
    """
    @staticmethod
    def simulate(M, x, T=None, S=None):
        computation_tree = ATMSimulator.simulate(M, x)
        if computation_tree is None:
            return None
        elif T is not None and computation_tree.time() > T:
            return None
        elif S is not None and computation_tree.space() > S:
            return None
        else:
            return computation_tree
