import pandas as pd

import prepare_uttils
from prepare_uttils import (
    prepare_column,
    prepare_salary,
    prepare_name_json,
    prepare_list_to_str,
    prepare_clear_html,
    to_lower,
    prepare_date,
    prepare_salary_median
)

df = pd.read_json("hh.json")

columns = [
    "area",
    "has_test",
    "salary",
    "published_at",
    "schedule",
    "experience",
    "employment",
    "key_skills",
    "industries",
    "description"
]
extract_name = [
    "employment",
    "experience",
    "schedule",
    "area"
]
replace_arr_column = [
    "key_skills",
    "industries"
]

remove_html = [
    "description"
]


df_prepare = (df.
              pipe(prepare_salary, "salary")
              .pipe(prepare_column, columns)
              .pipe(prepare_name_json, extract_name)
              .pipe(prepare_list_to_str, replace_arr_column)
              .pipe(prepare_clear_html, remove_html)
              .pipe(prepare_date, "published_at")
              .pipe(to_lower)
              .pipe(prepare_salary_median)
              )

df_prepare.info()

df_prepare.to_json("preparehh.json")