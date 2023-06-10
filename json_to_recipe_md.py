import json
from typing import Any

import typer


def to_tags(tags: list[str]) -> str:
    md = ""
    for tag in tags:
        md += f"  - {tag}\n"
    return md


def liters_to_gallons(liters: float) -> float:
    return round(liters * 0.264172, 1)


def kilograms_to_pounds(kilograms: float) -> float:
    return round(kilograms * 2.204623, 1)


def round_gravity_points(gravity: float) -> float:
    return round(float(f"{gravity:.4f}"), 3)


def get_ingredients_rows_as_md(data: dict[str, Any]) -> str:
    """Creates rows of ingredients data as markdown."""
    ingredient_rows: list[str] = []
    for f in data["fermentables"]:
        amount_in_lbs = kilograms_to_pounds(f["amount"])
        ingredient_rows.append(
            f"|{amount_in_lbs} lbs ({round(f['amount'], 2)} kgs)|{f['name']}|{f['type']}|{f['percentage']}%|"
        )
    return "\n".join(ingredient_rows)


def main(
    json_file_path: str = typer.Argument(..., help="Path to exported json file.")
) -> None:
    """Outputs markdown from a brewfather exported json file."""
    with open(json_file_path) as fp:
        data = json.load(fp)
    style = data["style"]
    ingredients = get_ingredients_rows_as_md(data)
    md = f"""
---
title: "{data["name"]} ({style["name"]} | {int(style["categoryNumber"])}{style["styleLetter"]})"
collection: recipes
categories:
  - Recipes
tags:
  - {style["name"].lower()}
  - {int(style["categoryNumber"])}{style["styleLetter"]}
{to_tags(data["searchTags"])}
---

**Name**: {data["name"]}<br />
**Style**: {style["name"]} ({int(style["categoryNumber"])}{style["styleLetter"]})
**Type**: {data["type"]}

## Recipe Specifications

**Boil Size**: {liters_to_gallons(data["equipment"]["boilSize"])} gal ({round(data["equipment"]["boilSize"], 1)}L)<br />
**Batch Size (fermenter)**: {liters_to_gallons(data["equipment"]["batchSize"])} gal ({round(data["equipment"]["batchSize"], 1)}L)<br />
**Estimated OG**: {round_gravity_points(data["postBoilGravity"])}<br />
**Estimated Color**: {data["color"]} SRM<br />
**Estimated IBU**: {data["ibu"]} ({data["ibuFormula"]})<br />
**Estima.ed ABV**: {round(data["abv"], 1)}%<br />
**Brewhouse Efficiency**: {data["efficiency"]}%<br />
**Boil Time**: {data["equipment"]["boilTime"]} minutes<br />

## Ingredients

|Amount|Name|Type|%|
|-|-|-|-|
{ingredients}
    """
    typer.echo(md)


if __name__ == "__main__":
    typer.run(main)
