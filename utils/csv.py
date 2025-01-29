#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Save final kdrama dataset as csv file
Created on Wed Jan 29 11:38:17 2025
@author: danyasherbini
"""

# save to csv
import os
from datetime import datetime
from text_analysis2 import kdramas_final

def save_to_csv(df):

    # set output directory
    output_dir = './data'
    os.makedirs(output_dir, exist_ok=True)  # ensure directory exists
        
    # Get current date in YYYY-MM-DD format
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Create filename with date
    output_path = os.path.join(output_dir, f'kdramas_{date_str}.csv')
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    return print(f"File saved successfully at {output_path} on {date_str}")

save_to_csv(kdramas_final)