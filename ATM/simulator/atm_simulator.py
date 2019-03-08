from simulator.computation_tree import ComputationTree

"""
ATMSimulator --- class that simulates an ATM
:author Jeremy McMahan
"""


class ATMSimulator:
    """
    Simulates the given Alternating Turing Machine, M, on an input x
    :param M a ATM to simulate
    :param x the input to M represented as an ordered list
    :returns An accepting computation tree if x in L(M), else None
    """
    @staticmethod
    def simulate(M, x):
        if not ATMSimulator.is_string(M.Sigma, x):
            return None
        start_tape = x
        start_tape.insert(0, M.left_end)
        start_config = M.Configuration(M.start, 0, start_tape)
        return ATMSimulator.accepting(M, start_config)

    """
    Determines if the given configuration of M is accepting
    :param M an ATM
    :param c a configuration of M on an input x
    :returns An accepting computation tree if c is an accepting configuration, else None
    """
    @staticmethod
    def accepting(M, c):
        if M.t(c.state) == '∧':
            return ATMSimulator.and_accepting(M, c)
        elif M.t(c.state) == '∨':
            return ATMSimulator.or_accepting(M, c)

    """
    Determines if the given or configuration of M is accepting
    :param M an ATM
    :param c an or configuration of M on an input x
    :returns An accepting computation tree if c is an accepting or configuration, else None
    """
    @staticmethod
    def or_accepting(M, c):
        for child in ATMSimulator.get_reachable(M, c):
            child_proof_tree = ATMSimulator.accepting(M, child)
            if child_proof_tree is not None:
                return ComputationTree(c, [child_proof_tree])    # or just needs one child to accept
        return None

    """
    Determines if the given and configuration of M is accepting
    :param M an ATM
    :param c an and configuration of M on an input x
    :returns An accepting computation tree if c is an accepting and configuration, else None
    """
    @staticmethod
    def and_accepting(M, c):
        tree_children = []
        for child in ATMSimulator.get_reachable(M, c):
            child_proof_tree = ATMSimulator.accepting(M, child)
            if child_proof_tree is None:
                return None                     # and needs all children to accept
            tree_children.append(child_proof_tree)
        return ComputationTree(c, tree_children)

    """
    Computes all of the configurations of M reachable in 1 step from c
    :param M a ATM
    :param c a configuration of M
    :returns a list of the configurations reachable in 1 step in M from c
    """
    @staticmethod
    def get_reachable(M, c):
        reachable = set()
        for state, symbol, direction in M.delta(c.state, c.tape[c.head_position]):
            tape = list(c.tape)
            tape[c.head_position] = symbol
            head_position = c.head_position + ((-1) if direction == 'L' else 1)
            if head_position >= len(tape):
                tape.append(M.blank)         # Simulate infinitely many blanks
            reachable |= {M.Configuration(state, head_position, tape)}
        return reachable

    """
    Determines if x is a valid string over Sigma
    :param Sigma the alphabet
    :param x the string represented as an ordered list
    :returns true iff x is a valid string over Sigma
    """
    @staticmethod
    def is_string(Sigma, x):
        for a in x:
            if a not in Sigma:
                return False
        return True
