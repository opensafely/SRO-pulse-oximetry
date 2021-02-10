
# Import functions
from cohortextractor import (
    StudyDefinition, 
    patients, 
    codelist,
    Measure, 
    codelist_from_csv
)

# Import codelists
pulse_oximetry_codes = codelist_from_csv("codelists/opensafely-pulse-oximetry.csv",
    system="snomed",
    column="code",)




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

start_date = "2019-01-01"
end_date = "today"

# Specifiy study defeinition
study = StudyDefinition(
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "exponential_increase",
        "incidence": 1,
    },

    population=patients.registered_as_of(start_date),

    had_pulse_ox=patients.with_these_clinical_events(
        pulse_oximetry_codes,
        returning="binary_flag",
        between=[start_date, end_date],
        return_expectations={"incidence": 0.5}
    ),



    region=patients.registered_practice_as_of(
        start_date,
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
   
    age=patients.age_as_of(
        start_date,
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    age_band = patients.categorised_as(
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
                    "0-19": 0.125,
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
      "category": {"ratios": {"M": 0.49, "F": 0.51}},
    }
  ),


    # ETHNICITY IN 16 CATEGORIES
    # https: // github.com/opensafely/covid-vaccine-research-template/blob/main/analysis/study_definition.py
    # ethnicity_16=patients.with_these_clinical_events(
    #     ethnicity_codes_16,
    #     returning="category",
    #     find_last_match_in_period=True,
    #     include_date_of_match=False,
    #     return_expectations={
    #         "category": {
    #             "ratios": {
    #                 "1": 0.0625,
    #                 "2": 0.0625,
    #                 "3": 0.0625,
    #                 "4": 0.0625,
    #                 "5": 0.0625,
    #                 "6": 0.0625,
    #                 "7": 0.0625,
    #                 "8": 0.0625,
    #                 "9": 0.0625,
    #                 "10": 0.0625,
    #                 "11": 0.0625,
    #                 "12": 0.0625,
    #                 "13": 0.0625,
    #                 "14": 0.0625,
    #                 "15": 0.0625,
    #                 "16": 0.0625,
    #             }
    #         },
    #         "incidence": 0.75,
    #     },
    # ),

    # # ETHNICITY IN 6 CATEGORIES
    # ethnicity=patients.with_these_clinical_events(
    #     ethnicity_codes,
    #     returning="category",
    #     find_last_match_in_period=True,
    #     include_date_of_match=False,
    #     return_expectations={
    #         "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
    #         "incidence": 0.75,
    #     },
    # ),
    
    
)

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

    # Measure(
    #     id="pulse_ox_by_ethnicity",
    #     numerator="had_pulse_ox",
    #     denominator="population",
    #     group_by=["ethnicity"],
    # ),

    # Measure(
    #     id="pulse_ox_by_ethnicity_16",
    #     numerator="had_pulse_ox",
    #     denominator="population",
    #     group_by=["ethnicity_16"],
    # ),

    Measure(
        id="pulse_ox_total",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=None,
    ),
]
