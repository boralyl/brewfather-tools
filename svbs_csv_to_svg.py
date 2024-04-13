"""
Converts a csv file from an SSBrewtech SVBS brew day into a graph showing
the time and temperature data as a line graph.
"""
from typing import Annotated

import pandas as pd
import plotly.express as px
import typer


def main(
        csv_file_path: str = typer.Argument(..., help="Path to the SVBS csv file."),
        title: Annotated[str, typer.Option('--title')] = "Title"
    ) -> None:
    df = pd.read_csv(csv_file_path)
    fig = px.line(
        df, 
        x="TIME ", 
        y="TEMPERATURE", 
        title=f"{title} (Total time: {df.iloc[-1]['TIME '].strip()})"
    )
    fig.update_layout(xaxis_title="Time", yaxis_title="Temperature (F)")
    fig.write_image("figure.svg", engine="kaleido", format="svg")
    return


if __name__ == "__main__":
    typer.run(main)