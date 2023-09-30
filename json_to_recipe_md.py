import json
from datetime import datetime
from typing import Any

import requests
import typer
from dotenv import dotenv_values
from requests.auth import HTTPBasicAuth


def send_brewfather_request(url: str):
    config = dotenv_values(".env")
    auth = HTTPBasicAuth(config["BREWFATHER_USERNAME"], config["BREWFATHER_API_KEY"])
    return requests.get(url, auth=auth).json()


def get_batch_id(recipe_name: str) -> str:
    for batch in send_brewfather_request("https://api.brewfather.app/v2/batches/"):
        if batch["recipe"]["name"] == recipe_name:
            return batch["_id"]
    raise ValueError(f"Couldn't find batch for {recipe_name}")


def get_batch_data(batch_id: str) -> dict[str, Any]:
    return send_brewfather_request(f"https://api.brewfather.app/v2/batches/{batch_id}")


def to_tags(tags: list[str]) -> str:
    md = ""
    for tag in tags:
        md += f"  - {tag}\n"
    return md


def liters_to_gallons(liters: float) -> float:
    return round(liters * 0.264172, 1)


def kilograms_to_pounds(kilograms: float) -> float:
    return round(kilograms * 2.204623, 1)


def grams_to_ounces(grams: float) -> float:
    return round(grams * 0.03527396, 1)


def round_gravity_points(gravity: float) -> float:
    return round(float(f"{gravity:.4f}"), 3)


def celcius_to_fahrenheit(celcius: float) -> float:
    return round(celcius * 1.8 + 32, 1)


def get_ingredients_rows_as_md(data: dict[str, Any]) -> str:
    """Creates rows of ingredients data as markdown."""
    ingredient_rows: list[str] = []
    for f in data["fermentables"]:
        amount_in_lbs = kilograms_to_pounds(f["amount"])
        amount = f"{amount_in_lbs} lbs ({round(f['amount'])} kgs)"
        name = f["name"]
        ingredient_type = f["type"]
        percentage = f"{f['percentage']}%"
        ingredient_rows.append(f"|{amount}|{name}|{ingredient_type}|{percentage}|")

    for h in data["hops"]:
        amount_in_ounces = grams_to_ounces(h["amount"])
        amount = f"{amount_in_ounces} oz ({round(h['amount'])} grams)"
        display_time = (
            f"{h['use']} {h['time']} {'min' if h['use'] == 'Boil' else 'days'}"
        )
        name = f"{h['name']} [{round(h['alpha'], 1)}%] - {display_time}"
        ingredient_rows.append(f"|{amount}|{name}|Hop|-|")

    for y in data["yeasts"]:
        amount = f"{y['amount']} {y['unit']}"
        name = f"{y['name']} ({y['laboratory']} #{y['productId']})"
        ingredient_rows.append(f"|{amount}|{name}|Yeast|-|")

    for m in data["miscs"]:
        amount = f"{m['amount']} {m['unit']}"
        name = f"{m['name']} ({m['use']}{' ' + str(m['time']) if m['time'] else ''})"
        ingredient_type = m["type"]
        ingredient_rows.append(f"|{amount}|{name}|{ingredient_type}|-|")

    return "\n".join(ingredient_rows)


def get_mash_step_rows_as_md(data: dict[str, Any], mash_step: dict[str, Any]) -> str:
    """Creates rows of mash steps as markdown."""
    mash_step_rows: list[str] = []
    mash_in_amount = liters_to_gallons(data["mashWaterAmount"])
    strike_temp = celcius_to_fahrenheit(data["strikeTemp"])
    mash_in_description = f"Add {mash_in_amount} gal ({round(data['mashWaterAmount'])} L) of water at {strike_temp}&deg;F ({data['strikeTemp']}&deg;C)"
    mash_temp = f"{celcius_to_fahrenheit(mash_step['stepTemp'])}&deg;F ({mash_step['stepTemp']}&deg;C)"
    mash_temp_time = f"{mash_step['stepTime']} mins"
    mash_step_rows.append(
        f"|Mash In|{mash_in_description}|{mash_temp}|{mash_temp_time}|"
    )

    sparge_amount = liters_to_gallons(data["spargeWaterAmount"])
    sparge_description = f"Add {sparge_amount} gal ({round(data['spargeWaterAmount'], 1)}L) water at 169&deg;F (75&deg;C)"
    mash_step_rows.append(f"|Sparge|{sparge_description}|-|-|")
    return "\n".join(mash_step_rows)


def get_batch_notes_as_md(data: dict[str, Any]) -> str:
    """Returns batch notes as markdown."""
    data["notes"].reverse()
    notes = ""
    for note in data["notes"]:
        if not note["note"]:
            continue
        note_date = datetime.fromtimestamp(note["timestamp"] / 1000).strftime(
            "%Y-%m-%d"
        )
        notes += f"* {note['note']} ({note_date})\n"
    return notes


def get_brewfather_url(data: dict[str, Any]) -> str:
    """Returns the brewfather shareable url if one is set."""
    if share_id := data.get("_share"):
        return f"Brewfather: [https://web.brewfather.app/share/{share_id}](https://web.brewfather.app/share/{share_id})"
    return ""


def main(
    json_file_path: str = typer.Argument(..., help="Path to exported json file.")
) -> None:
    """Outputs markdown from a brewfather exported json file."""
    with open(json_file_path) as fp:
        data = json.load(fp)
    style = data["style"]
    ingredients = get_ingredients_rows_as_md(data)
    mash_steps = get_mash_step_rows_as_md(data["data"], data["mash"]["steps"][0])
    batch_data = get_batch_data(get_batch_id(data["name"]))
    notes = get_batch_notes_as_md(batch_data)
    brewfather_url = get_brewfather_url(data)
    md = f"""
---
title: "{data["name"]} ({style["name"]} | {int(style["categoryNumber"])}{style["styleLetter"]})"
collection: recipes
categories:
  - Recipes
tags:
  - {style["name"]}
---

{data.get('teaser', '')}

**Name**: {data["name"]}<br />
**Style**: {style["name"]} ({int(style["categoryNumber"])}{style["styleLetter"]})<br />
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


## Mash

**Mash Schedule**: {data['mash']['name']}

|Name|Description|Step Temperature|Step Time|
|-|-|-|-|
{mash_steps}

## Notes

{notes}

{brewfather_url}
    """
    typer.echo(md)


if __name__ == "__main__":
    typer.run(main)
    # import pprint

    # r = send_brewfather_request(
    #    "https://api.brewfather.app/v2/recipes/ImPH27WPzvXnlR6QqNtQK6FwNsVhj9"
    # )
    # pprint.pprint(r)
