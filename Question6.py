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


# graph the survival curve for anticoagulant
PathCls.graph_sample_path(
    sample_path=simOutputs_anticoagulant.get_survival_curve(),
    title='Survival Curve for Treatment (anticoag)',
    x_label= 'Time',
    y_label='Number of people still alive')

# graph the survival curve for no therapy
PathCls.graph_sample_path(
    sample_path=simOutputs_no_therapy.get_survival_curve(),
    title= 'Survival Curve for Those Without Treatment',
    x_label= 'Time',
    y_label= 'Number of people still alive'
)


