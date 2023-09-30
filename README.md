# Brewfather tools

A set of scripts for interacting with Brewfather. Mostly for creating recipie pages
from json for threegodsbrewing.com.

## Running

1. Mark recipe as public in brew father.
2. On the Recipie details export as "Brewfather Recipe JSON"
3. Run the following:

```bash
$ python json_to_recipe_md.py /path/to/Brewfather_RECIPE_ChasingComets2_20230930.json

---
title: "Chasing Comets 2 (American IPA | 21A)"
collection: recipes
categories:
  - Recipes
tags:
  - American IPA
---

A West Coast IPA with Cryo Columbus, Simcoe and Cryo Citra.

**Name**: Chasing Comets 2<br />
**Style**: American IPA (21A)<br />
**Type**: All Grain

## Recipe Specifications

**Boil Size**: 7.8 gal (29.4L)<br />
**Batch Size (fermenter)**: 6.0 gal (22.7L)<br />
**Estimated OG**: 1.067<br />
**Estimated Color**: 4.8 SRM<br />
**Estimated IBU**: 78.6 (tinseth)<br />
**Estima.ed ABV**: 6.6%<br />
**Brewhouse Efficiency**: 65%<br />
**Boil Time**: 60 minutes<br />

## Ingredients

|Amount|Name|Type|%|
|-|-|-|-|
|12.2 lbs (6 kgs)|Pelton Pilsner-style Malt|Grain|71.45%|
|4.9 lbs (2 kgs)|Lamonta: Pale American Barley Malt|Grain|28.55%|
|1.0 oz (28 grams)|Ekuanot [13.8%] - Boil 60 min|Hop|-|
|1.0 oz (28 grams)|Citra (LUPOMAX) [18.5%] - Boil 5 min|Hop|-|
|1.0 oz (28 grams)|Simcoe [13.9%] - Boil 5 min|Hop|-|
|1.0 oz (28 grams)|Citra (LUPOMAX) [18.5%] - Aroma 20 days|Hop|-|
|1.0 oz (28 grams)|Columbus (LUPOMAX) [20.5%] - Aroma 20 days|Hop|-|
|1.0 oz (28 grams)|Simcoe [12.8%] - Aroma 20 days|Hop|-|
|1.0 oz (28 grams)|Citra (LUPOMAX) [18.5%] - Dry Hop 3 days|Hop|-|
|1.0 oz (28 grams)|Columbus (LUPOMAX) [20.5%] - Dry Hop 3 days|Hop|-|
|1.0 oz (28 grams)|Simcoe [12.8%] - Dry Hop 3 days|Hop|-|
|1 ml|Flagship (Imperial #A07)|Yeast|-|
|1 tbsp|PH 5.2 Stabilizer (Mash)|Water Agent|-|
|0.5 items|Whirlfloc (Boil 15)|Fining|-|


## Mash

**Mash Schedule**: High fermentability

|Name|Description|Step Temperature|Step Time|
|-|-|-|-|
|Mash In|Add 5.5 gal (21 L) of water at 161.1&deg;F (71.7&deg;C)|149.0&deg;F (65&deg;C)|60 mins|
|Sparge|Add 3.6 gal (13.5L) water at 169&deg;F (75&deg;C)|-|-|

## Notes

* Added the dry hops when the beer was at 1.014 (2023-09-05)
* The beer has the same OG for 2 days in a row, 1.013. Removed blow off tube and kept cane open, and started cold crashing. (2023-09-09)
* Dumped the trub and hops after cold crashing. The hops clogged up the elbow so I used a small amount of CO2 through the carb stone to push it out while the dump valve was open.  I closed the carb stone valve, but forgot to shut the dump valve so ended up with some hops and trub on the floor. (2023-09-11)
* Turned CO2 up to ~7PSI and waited 20 minutes, going to slowly increase every hour until I get to about 20PSI. (2023-09-11)
* Transferred to keg after 48 hours of carbonating. (2023-09-13)

```
