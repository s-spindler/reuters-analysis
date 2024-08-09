import marimo

__generated_with = "0.7.17"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(r"""Result summary by Reuters: thttps://reutersinstitute.politics.ox.ac.uk/digital-news-report/2024/germany""")
    return


@app.cell
def __(trust_df):
    trust_df
    return


@app.cell
def __(column_name_to_media, relevant_columns, reuters_df):
    trust_df = reuters_df.filter(relevant_columns).rename(columns=column_name_to_media)
    trust_df
    return trust_df,


@app.cell
def __(number_to_col_name, number_to_media):
    column_name_to_media = {number_to_col_name[num]: number_to_media[num] for num in number_to_col_name}
    return column_name_to_media,


@app.cell
def __(relevant_columns):
    number_to_col_name = {col[col.rindex("_") + 1:]: col for col in relevant_columns}
    return number_to_col_name,


@app.cell
def __():
    number_to_media = {
        "46": "ARD Tagesschau",
        "47": "ZDF Heute",
        "48": "RTL aktuell",
        "50": "n-tv",
        "51": "Der Spiegel",
        "52": "Die ZEIT",
        "53": "Stern",
        "54": "Focus",
        "55": "Süddeutsche Zeitung",
        "56": "Bild",
        "57": "FAZ",
        "58": "Regional or local newspaper",
        "60": "t-online",
        "889": "WELT",
        "890": "webde"
    }
    return number_to_media,


@app.cell
def __(reuters_df):
    all_columns = reuters_df.columns.values
    import re
    relevant_columns = [col for col in all_columns if re.search("Q6_2018_trust_rb_\d{2,3}", col)]
    return all_columns, re, relevant_columns


@app.cell
def __(pandas):
    reuters_df = pandas.read_spss("Reuters DNR 2024 - Germany.sav")
    return reuters_df,


@app.cell
def __():
    import pandas
    return pandas,


@app.cell
def __():
    import marimo as mo
    return mo,


if __name__ == "__main__":
    app.run()
