import marimo

__generated_with = "0.7.17"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(
        r"""
        United Internet Media post: <https://www.united-internet-media.de/de/newsroom/vermarkterblog/blog/show/digital-news-report-2024-webde-und-gmx-unter-den-top-ten-der-meistgenutzten-online-news-sites/>

        Result summary by Reuters: <https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2024/germany>
        """
    )
    return


@app.cell
def __(reuters_grouped_df):
    reuters_grouped_df.div(reuters_grouped_df.sum(axis=1), axis=0).style.format(
        {c: "{:,.2%}" for c in reuters_grouped_df.columns.values}
    ).background_gradient(axis=0)
    return


@app.cell
def __(alt, mo, trust_long_df):
    mo.ui.altair_chart(
        alt.Chart(
            trust_long_df.groupby(["media", "rating"])["rating"]
            .count()
            .reset_index(name="count")
        )
        .mark_line()
        .encode(x="rating", y="count", color="media")
    )
    return


@app.cell
def __(alt, mo, trust_long_df):
    mo.ui.altair_chart(
        alt.Chart(trust_long_df)
        .mark_boxplot()
        .encode(alt.X("rating"), alt.Y("media"))
    )
    return


@app.cell
def __(alt, mo, trust_long_df):
    mo.ui.altair_chart(
        alt.Chart(trust_long_df, width=100)
        .transform_density("rating", as_=["rating", "density"], groupby=["media"])
        .mark_area(orient="horizontal")
        .encode(
            alt.X("density:Q")
            .stack("center")
            .impute(None)
            .title(None)
            .axis(labels=False, values=[0], grid=False, ticks=True),
            alt.Y("rating:Q"),
            alt.Color("media:N"),
            alt.Column("media:N")
            .spacing(0)
            .header(titleOrient="bottom", labelOrient="bottom", labelPadding=0),
        )
        .configure_view(stroke=None)
    )
    return


@app.cell
def __(alt, mo, trust_long_df):
    mo.ui.altair_chart(
        alt.Chart(trust_long_df)
        .mark_circle()
        .encode(x="rating", y="media", size="count(rating):Q")
    )
    return


@app.cell
def __(trust_pivot_df):
    # From Reuters page: "6–10 coded as ‘Trust’, 5 coded as ‘Neither’, 0–4 coded as ‘Don’t trust’"
    reuters_grouped_df = trust_pivot_df.assign(
        trust=trust_pivot_df[list(range(6, 11))].sum(axis=1),
        neither=trust_pivot_df[5],
        no_trust=trust_pivot_df[list(range(0, 5))].sum(axis=1),
    ).drop(list(range(0, 11)), axis=1)
    return reuters_grouped_df,


@app.cell
def __(trust_pivot_df):
    def calc_nps(row):
        cols = list(range(0, 11))
        detractor_cols = list(range(0, 7))
        promoter_cols = [9, 10]

        total = row[cols].sum()
        detractors = row[detractor_cols].sum()
        promoters = row[promoter_cols].sum()

        nps = promoters / total * 100 - detractors / total * 100

        return nps


    trust_pivot_df.apply(calc_nps, axis=1)
    return calc_nps,


@app.cell
def __(trust_long_df):
    trust_pivot_df = (
        trust_long_df.groupby(["media", "rating"])["rating"]
        .count()
        .reset_index(name="count")
        .pivot_table(index="media", columns="rating", values="count")
    )
    return trust_pivot_df,


@app.cell
def __(trust_df):
    trust_long_df = trust_df.melt(var_name="media", value_name="rating")
    return trust_long_df,


@app.cell
def __(reuters_df):
    def get_relevant_columns(all_columns):
        import re

        return [
            col
            for col in all_columns
            if re.search("Q6_2018_trust_rb_\d{2,3}", col)
        ]


    def map_column_name_to_media(relevant_columns):
        number_to_col_name = {
            col[col.rindex("_") + 1 :]: col for col in relevant_columns
        }

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
            "890": "webde",
        }

        return {
            number_to_col_name[num]: number_to_media[num]
            for num in number_to_col_name
        }


    _relevant_columns = get_relevant_columns(reuters_df.columns.values)
    column_name_to_media = map_column_name_to_media(_relevant_columns)

    trust_df = reuters_df.filter(_relevant_columns).rename(
        columns=column_name_to_media
    )
    return (
        column_name_to_media,
        get_relevant_columns,
        map_column_name_to_media,
        trust_df,
    )


@app.cell
def __(pandas):
    reuters_df = pandas.read_spss("Reuters DNR 2024 - Germany.sav")
    return reuters_df,


@app.cell(hide_code=True)
def __():
    import marimo as mo
    import altair as alt
    import pandas
    return alt, mo, pandas


if __name__ == "__main__":
    app.run()
