import seaborn as sns
from faicons import icon_svg
import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 
from shinywidgets import render_plotly
import importlib


#load penguins dataset
df = palmerpenguins.load_penguins()

#set up page title
ui.page_opts(title="Arsh Kandola Penguins dashboard", fillable=True)



#create a sidebar and filters
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/akandola47/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://akandola47.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

#create columns for the box of data for the statistics
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("snowman")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape

    with ui.value_box(showcase=icon_svg("snowflake")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Bill Depth")

        @render_plotly
        def length_depth_plotly():
            return px.histogram(
                data_frame=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Arsh Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

#ui.include_css(app_dir / "styles.css")

#add the reacive calc and use filtered dataframe
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
