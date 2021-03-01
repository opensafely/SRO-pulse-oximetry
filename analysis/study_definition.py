
# Import functions
from cohortextractor import (
    StudyDefinition, 
    patients, 
    codelist,
    Measure, 
    codelist_from_csv
)

import pandas as pd

codelist_df = pd.read_csv("codelists/opensafely-pulse-oximetry.csv")

pulse_ox_code_mapping = {"1325251000000106": "Y2a44",
                         "1325261000000109": "Y2a45",
                         "1325271000000102": "Y2a46",
                         "1325201000000105": "Y2a47",
                         "1325191000000108": "Y2a48", 
                         "1325221000000101": "Y2a49",
                         "1325241000000108": "Y2a4a",
                         "1325281000000100": "Y2a4b",
                         "1325681000000102": "Y2b97",
                         "1325701000000100": "Y2b98",
                         "1325691000000100": "Y2b99",
                         "1325211000000107": "YA796"
                         }

def apply_code_mapping(row):
    row['CTV3ID'] = pulse_ox_code_mapping[str(row['code'])]
    return row

codelist_df = codelist_df.apply(lambda row: apply_code_mapping(row), axis=1)

codelist_df.to_csv("codelists/opensafely-pulse-oximetry.csv")



# Import codelists
pulse_oximetry_codes = codelist_from_csv("codelists/opensafely-pulse-oximetry.csv",
    system="ctv3",
    column="CTV3ID",)




# ethnicity_codes = codelist_from_csv(
#     "codelists/opensafely-ethnicity.csv",
#     system="ctv3",
#     column="Code",
#     category_column="Grouping_6",
# )


# ethnicity_codes_16 = codelist_from_csv(
#     "codelists/opensafely-ethnicity.csv",
#     system="ctv3",
#     column="Code",
#     category_column="Grouping_16",
# )

start_date = "2020-07-01"
end_date = "2020-01-01"

# Specifiy study defeinition
study = StudyDefinition(
    index_date = "2020-07-01",
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 1,
    },

    population=patients.satisfying(
        """
        registered AND
        (NOT died) AND
        (sex = 'F' OR sex='M') AND
        (age != 0)
        """,

        registered=patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
        ),

        died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1}
        ),
    ),


    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    age_band=patients.categorised_as(
        {
            "0": "DEFAULT",
            "0-19": """ age >= 0 AND age < 20""",
            "20-29": """ age >=  20 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.001,
                    "0-19": 0.124,
                    "20-29": 0.125,
                    "30-39": 0.125,
                    "40-49": 0.125,
                    "50-59": 0.125,
                    "60-69": 0.125,
                    "70-79": 0.125,
                    "80+": 0.125,
                }
            },
        },

    ),


    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.5, "U": 0.01}},
        }
    ),

    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    ),

    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={"category": {"ratios": {
            "North East": 0.1,
            "North West": 0.1,
            "Yorkshire and the Humber": 0.1,
            "East Midlands": 0.1,
            "West Midlands": 0.1,
            "East of England": 0.1,
            "London": 0.2,
            "South East": 0.2, }}}
    ),

    had_pulse_ox=patients.with_these_clinical_events(
        pulse_oximetry_codes,
        returning="binary_flag",
        between=["index_date", "index_date + 1 month"],
        return_expectations={"incidence": 0.5}
    ),


    had_pulse_ox_event_code=patients.with_these_clinical_events(
        pulse_oximetry_codes,
        returning="binary_flag",
        between=["index_date", "index_date + 1 month"],
        returning="code",
        return_expectations={"category": {
            "ratios": {"1239511000000100": 1}}, }
    ),


    
    
)

measures = [
   

    Measure(
        id="had_pulse_ox_total",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=None
    ),

    Measure(
        id="had_pulse_ox_event_code",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["had_pulse_ox_event_code"]
    ),

    Measure(
        id="had_pulse_ox_practice_only",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["practice"]
    ),

    Measure(
        id="had_pulse_ox_by_region",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["region"],
    ),

    Measure(
        id="had_pulse_ox_by_sex",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["sex"],
    ),

    Measure(
        id="had_pulse_ox_by_age_band",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["age_band"],
    ),


    
]