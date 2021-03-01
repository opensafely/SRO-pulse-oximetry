import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


if not os.path.exists('output/figures'):
    os.mkdir('output/figures')


class Measure:
  def __init__(self, id, numerator, denominator, group_by):
    self.id = id
    self.numerator = numerator
    self.denominator = denominator
    self.group_by = group_by


measures = [
    Measure(
        id="pulse_ox_by_sex",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["sex"],
    ),

    Measure(
        id="pulse_ox_by_region",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["region"],
    ),

    Measure(
        id="pulse_ox_by_age_band",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["age_band"],
    ),

    Measure(
        id="pulse_ox_total",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=None,
    ),
]



measures_df_sex = pd.read_csv('output/measures/measure_had_pulse_ox_by_sex.csv')
measures_df_region = pd.read_csv(
    'output/measures/measure_had_pulse_ox_by_region.csv')
measures_df_age = pd.read_csv(
    'output/measures/measure_had_pulse_ox_by_age_band.csv')
measures_df_total = pd.read_csv(
    'output/measures/measure_had_pulse_ox_total.csv')


#temporary fix for population not working in Measures
measures_df_total = measures_df_total.groupby(
    ['date'])['had_pulse_ox', 'population'].sum().reset_index()
measures_df_total['value'] = measures_df_total['had_pulse_ox'] / \
    measures_df_total['population']


def to_datetime_sort(df):
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date')


to_datetime_sort(measures_df_sex)
to_datetime_sort(measures_df_region)
to_datetime_sort(measures_df_age)
to_datetime_sort(measures_df_total)


def redact_small_numbers(df, n, m):
    """
    Takes measures df and converts any row to nana where value of denominator or numerater in measure m equal to 
    or below n
    Returns df of same shape.
    """
    mask_n = df[m.numerator].isin(list(range(0, n+1)))
    mask_d = df[m.denominator].isin(list(range(0, n+1)))
    mask = mask_n | mask_d
    df.loc[mask, [m.numerator, m.denominator, 'value']] = np.nan
    return df


redact_small_numbers(measures_df_sex, 5, measures[0])
redact_small_numbers(measures_df_region, 5, measures[1])
redact_small_numbers(measures_df_age, 5, measures[2])
redact_small_numbers(measures_df_total, 5, measures[3])

def calculate_rate(df, value_col='had_pulse_ox', population_col='population'):
    num_per_hundred_thousand = df[value_col]/(df[population_col]/1000)
    df['num_per_hundred_thousand'] = num_per_hundred_thousand


calculate_rate(measures_df_sex)
calculate_rate(measures_df_age)
calculate_rate(measures_df_region)
calculate_rate(measures_df_total)


def plot_measures(df, title, filename, column_to_plot, category=False, y_label='Number per 100, 000'):

    if category:
        for unique_category in df[category].unique():

            df_subset = df[df[category] == unique_category]

            plt.plot(df_subset['date'], df_subset[column_to_plot])
    else:
        plt.plot(df['date'], df[column_to_plot])

    plt.ylabel(y_label)
    plt.xlabel('Date')
    plt.xticks(rotation='vertical')
    plt.title(title)

    if category:
        plt.legend(df[category].unique(), bbox_to_anchor=(
            1.04, 1), loc="upper left")

    else:
        pass

    plt.savefig(f'output/figures/{filename}.jpeg', bbox_inches='tight')
   
    plt.clf()


plot_measures(measures_df_total, 'Pulse Oximetry use across Whole Population',
              'population_rates', 'had_pulse_ox', category=False, y_label='Total Number')

plot_measures(measures_df_sex,
              'Pulse Oximetry use by Sex per 1000', 'sex_rates', 'num_per_hundred_thousand', category='sex', )
plot_measures(measures_df_region,
              'Pulse Oximetry use by Region per 1000', 'region_rates', 'num_per_hundred_thousand', category='region')
plot_measures(measures_df_age,
              'Pulse Oximetry use by Age Band per 1000',  'age_rates', 'num_per_hundred_thousand', category='age_band')
