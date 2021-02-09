import pandas as pd
import matplotlib.pyplot as plt


measures_df_sex = pd.read_csv('../output/measures/measure_pulse_ox_by_sex.csv')
measures_df_region = pd.read_csv(
    '../output/measures/measure_pulse_ox_by_region.csv')
measures_df_age = pd.read_csv(
    '../output/measures/measure_pulse_ox_by_age_band.csv')
measures_df_total = pd.read_csv(
    '../output/measures/measure_pulse_ox_total.csv')


#temporary fix for population not working in Measures
# measures_df_total = measures_df_total.groupby(
#     ['date'])['had_pulse_ox', 'population', 'value'].sum().reset_index()


def to_datetime_sort(df):
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date')


to_datetime_sort(measures_df_sex)
to_datetime_sort(measures_df_region)
to_datetime_sort(measures_df_age)


def plot_measures(df, title, filename, category=False):

    if category:
        for unique_category in df[category].unique():

            df_subset = df[df[category] == unique_category]

            plt.plot(df_subset['date'], df_subset['value'])
    else:
        plt.plot(df['date'], df['value'])

    plt.ylabel('% of population')
    plt.xlabel('Date')
    plt.xticks(rotation='vertical')
    plt.title(title)

    if category:
        plt.legend(df[category].unique(), bbox_to_anchor=(
            1.04, 1), loc="upper left")

    else:
        pass

    plt.savefig(f'../output/figures/{filename}.jpeg', bbox_inches='tight')
    plt.show()


plot_measures(measures_df_sex, 'Pulse Oximetry use by Sex',
              'sex_rates', 'sex', )
plot_measures(measures_df_region, 'Pulse Oximetry use by Region',
              'region_rates', 'region')
plot_measures(measures_df_age, 'Pulse Oximetry use by Age Band',
              'age_rates', 'age_band')
plot_measures(measures_df_total, 'Pulse Oximetry us across Whole Population',
              'population_rates', category=False)
