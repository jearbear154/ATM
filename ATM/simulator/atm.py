
"""
ATM --- class that represents a single tape Alternating Turing Machine
:author Jeremy McMahan
"""


class ATM:
    """
    Creates the Alternating Turing Machine from the given information, if the Description of an Alternating Turing
    Machine given is not valid, then will represent the Alternating Turing Machine that always immediately rejects.
    :param Q the set of states
    :param Sigma the alphabet set
    :param Gamma the tape alphabet set, a strict superset of Sigma
    :param left_end the left end marker that is in Gamma but not Sigma
    :param blank the blank symbol that is in Gamma but not Sigma
    :param delta the transition function mapping QXGamma -> QXGammaX{L,R}
    :param start the start state that is an element of Q
    :param t the type function assigning each state a type
    """

    def __init__(self, Q, Sigma, Gamma, left_end, blank, delta, start, t):
        self.Q = Q
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.left_end = left_end
        self.blank = blank
        self.delta = delta
        self.start = start
        self.t = t
        if not self.machine_valid():
            self.t = lambda q: '∨'  # an or state with no transitions is a reject state
            self.delta = lambda x, y: set()  # Ensure no transitions possible

    """
    Checks that the given description of an ATM represents a valid ATM
    :returns True iff the ATM is valid
    """

    def machine_valid(self):
        return self.states_correct() and self.alphabets_consistent() and \
            self.transition_function_valid() and self.type_function_valid()

    """
    Checks that the state set and the start state satisfy the definition of a Turing Machine
    :returns True iff the states are correct
    """

    def states_correct(self):
        return self.start in self.Q

    """
    Checks the input and tape alphabet along with the left end marker and blank symbol satisfy the definition of a 
    Turing Machine
    :returns True iff the input and tape alphabet satisfy the definitions
    """

    def alphabets_consistent(self):
        sigma_subset_of_gamma = self.Sigma.issubset(self.Gamma)
        left_end_in_gamma_not_sigma = self.left_end in self.Gamma and self.left_end not in self.Sigma
        blank_in_gamma_not_sigma = self.blank in self.Gamma and self.blank not in self.Sigma
        return sigma_subset_of_gamma and left_end_in_gamma_not_sigma and blank_in_gamma_not_sigma

    """
    Checks that the transition function satisfies the definition of a Turing Machine
    :returns True iff the transition function is valid
    """

    def transition_function_valid(self):
        exists_halting_state = False
        for q in self.Q:
            for p, a, d in self.delta(q, self.left_end):
                if a != self.left_end or d != 'R':  # ensure delta properly handles reading left end marker
                    return False
            for a in self.Gamma:
                exists_halting_state |= (self.delta(q, a) == set())  # represents a halting state
        return exists_halting_state

    """
    Checks the type function assigns every state to either an and state or an or state
    :returns True iff the type function is valid
    """

    def type_function_valid(self):
        for q in self.Q:
            if self.t(q) != '∧' and self.t(q) != '∨':
                return False
        return True

    """
    Determines if the ATM is equal to the other ATM
    :param other the other ATM
    :returns True iff the two ATMs are equal
    """

    def __eq__(self, other):
        states_equal = self.Q == other.Q
        input_alphabets_equal = self.Sigma == other.Sigma
        tape_alphabets_equal = self.Gamma == other.Gamma
        left_ends_equal = self.left_end == other.left_end
        blanks_equal = self.blank == other.blank
        starts_equal = self.start == other.start

        if not (tape_alphabets_equal and states_equal):
            return False
        else:
            for q in self.Q:
                for a in self.Gamma:
                    if self.delta(q, a) != other.delta(q, a):
                        return False
                if self.t(q) != other.t(q):
                    return False
            return input_alphabets_equal and left_ends_equal and blanks_equal and starts_equal

    """
    Determines if the ATM is equal to the other ATM
    :param other the other ATM
    :returns True iff the tow ATMs are not equal
    """

    def __ne__(self, other):
        return not (self == other)

    """
    Configuration --- class that represents a configuration of the Alternating Turing Machine on some input x
    """

    class Configuration:
        """
        Creates a configuration
        :param state the current state of the machine
        :param head_position the position of the tape head
        :param tape the non-blank portion of the machine's tape
        """

        def __init__(self, state, head_position, tape):
            self.state = state
            self.head_position = head_position
            self.tape = tape
