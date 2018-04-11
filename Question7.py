import MarkovModelClasses as MarkovCls
import ParameterClasses as ParameterCls
import SupportMarkovModel as SupportModel
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs


# create the cohorts
cohort_anticoagulant = MarkovCls.Cohort(id=0, therapy=ParameterCls.Therapies.ANTICOAGULANT)
cohort_no_therapy = MarkovCls.Cohort(id=0, therapy=ParameterCls.Therapies.NO_THERAPY)

# simulate the cohorts
simOutputs_anticoagulant = cohort_anticoagulant.simulate()
simOutputs_no_therapy = cohort_no_therapy.simulate()


# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs_anticoagulant.get_survival_times(),
    title='Survival times of patients with treatment',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=1
)

# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs_no_therapy.get_survival_times(),
    title='Survival times of patients without treatment',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=1
)