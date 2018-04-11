from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputData as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random
import scr.ProbDistParEst as Est


class HealthStats(Enum):
    """ health states of patients with stroke """
    WELL = 0
    STROKE = 1
    POST_STROKE = 2
    DEATH = 3
    BACKGROUND_DEATH = 4


class Therapies(Enum):
    """ mono vs. combination therapy """
    NO_THERAPY = 0
    ANTICOAGULANT = 1



class ParametersFixed():
    def __init__(self, therapy):

        self._therapy = therapy

        self._delta_t = Data.DELTA_T

        #initial health state
        self._initialHealthState = HealthStats.WELL

        # calculate transition probabilities between heart states
        self._prob_matrix = Data.TRANS_MATRIX()

        # update the transition probability matrix if anticoagulation therapy is being used
        if self._therapy == Therapies.ANTICOAGULANT:
            # treatment relative risks
            self._treatmentRR = Data.TREATMENT_RR_POST_STROKE
            self._treatmentRR_bleeding = Data.TREATMENT_RR_BLEEDING

            # calculate transition probability matrix for the combination therapy
            self._prob_matrix = calculate_prob_matrix_anticoagulation(
                matrix_no_therapy=self._prob_matrix, anticoagulation_rr=Data.TREATMENT_RR_POST_STROKE)

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

class ParametersProbabilistic():
    def __init__(self, seed, therapy):

        self._rng = Random.RNG(seed)    # random number generator to sample from parameter distributions
        self._StrokeProbMatrixRVG = []  # list of dirichlet distributions for transition probabilities
        self._lnRelativeRiskRVG = None  # random variate generator for the treatment relative risk

        # Stroke transition probabilities
        j = 0
        for prob in Data.TRANS_MATRIX:
            self._StrokeProbMatrixRVG.append(Random.Dirichlet(prob[j:]))
            j += 1

        # resample parameters
        self.__resample()

    def __resample(self):

        # calculate transition probabilities
        # create an empty matrix populated with zeroes
        self._prob_matrix = []
        for s in HealthStats:
            self._prob_matrix.append([0] * len(HealthStats))

        # for all health states
        for s in HealthStats:
            # if the current state is death
            if s in [HealthStats.DEATH]:
                # the probability of staying in this state is 1
                self._prob_matrix[s.value][s.value] = 1
            else:
                # sample from the dirichlet distribution to find the transition probabilities between hiv states
                dist = self._StrokeProbMatrixRVG[s.value]
                sample = dist.sample(self._rng)
                for j in range(len(sample)):
                    self._prob_matrix[s.value][s.value + j] = sample[j]


def calculate_prob_matrix():
    """ :returns transition probability matrix for stroke states under no therapy"""

    # create an empty matrix populated with zeroes
    prob_matrix = []
    for s in HealthStats:
        prob_matrix.append([0] * len(HealthStats))

    # for all health states
    for s in HealthStats:
        # if the current state is death
        if s in [HealthStats.DEATH]:
            # the probability of staying in this state is 1
            prob_matrix[s.value][s.value] = 1
        else:
            # calculate total counts of individuals
            sum_counts = sum(Data.TRANS_MATRIX[s.value])
            # calculate the transition probabilities out of this state
            for j in range(s.value, HealthStats.DEATH.value+1):
                prob_matrix[s.value][j] = Data.TRANS_MATRIX[s.value][j] / sum_counts

    return prob_matrix



def calculate_prob_matrix_anticoagulation(matrix_no_therapy, anticoagulation_rr):

    # create an empty matrix populated with zero
    matrix_anticoagulation = []
    for s in matrix_no_therapy:
        matrix_anticoagulation.append([0] * len(HealthStats))

    # populate the combo matrix
    # first non-diagonal elements
    for s in HealthStats:
        for next_s in range(s.value + 1, len(HealthStats)):
            matrix_anticoagulation[s.value][next_s] = anticoagulation_rr * matrix_no_therapy[s.value][next_s]

    # diagonal elements are calculated to make sure the sum of each row is 1
    for s in HealthStats:
        if s not in [HealthStats.DEATH]:
            matrix_anticoagulation[s.value][s.value] = 1 - sum(matrix_anticoagulation[s.value][s.value + 1:])

    return matrix_anticoagulation
