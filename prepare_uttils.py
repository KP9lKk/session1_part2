import pandas as pd
from pandas import isna
from bs4 import BeautifulSoup


def prepare_salary(dfSalary: pd.DataFrame, column) -> pd.DataFrame:
    dfSalary[column] = dfSalary[column].map(lambda salary: get_salary(salary) if salary else None)
    return dfSalary


def get_salary(salary):
    if isna(salary):
        return None
    if salary:
        salary_from = salary["from"]
        salary_to = salary["to"]
        if salary_from and salary_to:
            return (salary_from + salary_to) / 2
        if salary_from:
            return salary_from
        if salary_to:
            return salary_to
    return None


def prepare_column(df: pd.DataFrame, columns):
    return df[columns]


def prepare_name_json(df: pd.DataFrame, columns):
    df[columns] = df[columns].map(lambda item: item["name"])
    return df


def prepare_list_to_str(df: pd.DataFrame, columns):
    df[columns] = df[columns].map(lambda items:
                                  ";".join([item["name"] for item in items])
                                  if items else None)
    return df


def prepare_clear_html(df: pd.DataFrame, columns):
    df[columns] = df[columns].map(lambda item: BeautifulSoup(item).text)
    return df


def prepare_date(df: pd.DataFrame, columns):
    df[columns] = pd.to_datetime(df[columns]).dt.date
    return df


def to_lower(df: pd.DataFrame):
    df = df.map(lambda item: item.lower() if isinstance(item, str) else item)
    return df


def prepare_salary_median(df: pd.DataFrame):
    median_imputer_bins = df.copy()
    salary_bins = median_imputer_bins.groupby(["experience"])
    print(salary_bins.salary.median())
    df["salary"] = salary_bins.salary.apply(lambda x: x.fillna(x.median())).droplevel(["experience"])
    return df
