
# simulation settings
POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 50    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals

DELTA_T = 1/4       # years

PSA_ON = True      # if probabilistic sensitivity analysis is on


## Matrix for Question 3 ##
# transition matrix for stroke
TRANS_MATRIX = [
    [0.75,  0.15,   0.0,    0.1],   # Well   # probability of moving to the next phase of healh
    [0.0,    0.0,   1.0,    0.0],   # Stoke
    [0.0,    0.25,  0.55,   0.2],   # Post-Stroke
    [0.0,     0,      0,    1.0]    # Stoke Dead
    ]


# treatment relative risk
TREATMENT_RR_POST_STROKE = 0.65
TREATMENT_RR_BLEEDING = 1.05



