import pandas as pd
import seaborn as ss
import matplotlib.pyplot as plt

df = pd.read_json("preparehh.json")

category_columns = [
    "schedule",
    "employment",
    "has_test",
    "area",
    "power bi",
    "sql",
    "банк"
]

count_columns = [
    "salary",
    "published_at"
]
df = pd.get_dummies(df, columns=['experience', 'employment', 'schedule'])
print(df.info())
df = pd.concat([df, df["key_skills"].str.get_dummies(';')], axis=1)
df = pd.concat([df, df["industries"].str.get_dummies(';')], axis=1)
df = pd.concat([df, df["area"].str.get_dummies(';')], axis=1)
print(df)

drop_columns = []
for column in df.columns[19:]:
    if len(df[df[column] == 1]) < 200:
        drop_columns.append(column)

df.drop(drop_columns, axis=1, inplace=True)

group = df.groupby("area")
df = group.filter(lambda x: len(x) > 100)

# for category in category_columns:
#     ss.countplot(data=df, x=category)
#     plt.xticks(rotation=90)
#     plt.savefig(f"./plot/{category}.png", bbox_inches='tight')
#     plt.clf()
#
# for count in count_columns:
#     ss.kdeplot(data=df, x=count)
#     plt.xticks(rotation=90)
#     plt.savefig(f"./plot/{count}.png", bbox_inches='tight')
#     plt.clf()
#
# for columns in df.columns:
#     print(df[columns].describe())

df.drop(["key_skills", "industries", "description", "area"], axis=1,
        inplace=True)

corr = df.corr().round(2)
ss.heatmap(corr, annot=True,
           cmap=ss.diverging_palette(220, 10, as_cmap=True),
           yticklabels=1,
           square=True)
plt.show()

df.info()
df.to_excel('hh.xlsx')
