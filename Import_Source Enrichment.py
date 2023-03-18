#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 21:03:13 2022

@author: Brian
"""

import pandas as pd


import_source = pd.read_csv("Import_Source_Pct_raw.csv")

country_codes = pd.read_csv("country_codes.csv")

country_categories = pd.read_excel("Country Category_with_links.xlsx")

country_color_codes = pd.read_csv("Country_color_codes.csv")

## need to replace Congo (Kinshasa) in future import source dataframes with "Congo" to match Country Codes, others were hardcoded into Country Codes

import_source['Country'] = import_source['Country'].str.strip()

country_categories['Country'] = country_categories['Country'].str.strip()

#import_source['country_percentage'] = import_source['country_percentage'].str.strip('%')


import_source_with_code = pd.merge(import_source, country_codes, how='left', left_on = ['Country'], right_on = 'name')

enriched_import_source_data = pd.merge(import_source_with_code, country_categories, how='left', left_on = ['Country'], right_on = 'Country')

enriched_import_source_data_with_color = pd.merge(enriched_import_source_data, country_color_codes, how='left', left_on = 'Category', right_on = 'Category')
enriched_import_source_data_with_color['Color Code'] = enriched_import_source_data_with_color['Color Code'].fillna('#D1E2E7')
enriched_import_source_data_with_color['Color'] = enriched_import_source_data_with_color['Color Code'].fillna('Gray')
enriched_import_source_data_with_color['Country'] = enriched_import_source_data_with_color['Country'].fillna('Other')
enriched_import_source_data_with_color['Category'] = enriched_import_source_data_with_color['Category'].fillna('Other')
enriched_import_source_data_with_color['name'] = enriched_import_source_data_with_color['name'].fillna('Other')
enriched_import_source_data_with_color['Metal'] = enriched_import_source_data_with_color['Metal']




enriched_import_source_data_with_color.to_csv('Import_Source_Pct.csv')