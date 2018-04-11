import MarkovModelClasses as MarkovCls
import ParameterClasses as P
import SupportMarkovModel as SupportModel
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs

# create the cohorts
cohort_anticoagulant = MarkovCls.Cohort(id=0, therapy=P.Therapies.ANTICOAGULANT)
cohort_no_therapy = MarkovCls.Cohort(id=0, therapy=P.Therapies.NO_THERAPY)

# simulate the cohorts
simOutputs_anticoagulant = cohort_anticoagulant.simulate()
simOutputs_no_therapy = cohort_no_therapy.simulate()



# Question 5
SupportModel.print_outcomes(simOutputs_anticoagulant, 'With Therapy')