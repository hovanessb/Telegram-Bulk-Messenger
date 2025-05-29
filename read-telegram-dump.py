import pandas as pd
import json
import pandas as pd
import json

csv_header = ["Name Prefix","First Name","Middle Name","Last Name","Name Suffix","Phonetic First Name","Phonetic Middle Name","Phonetic Last Name","Nickname","File As","E-mail 1 - Label","E-mail 1 - Value","Phone 1 - Label","Phone 1 - Value","Address 1 - Label","Address 1 - Country","Address 1 - Street","Address 1 - Extended Address","Address 1 - City","Address 1 - Region","Address 1 - Postal Code","Address 1 - PO Box","Organization Name","Organization Title","Organization Department","Birthday","Event 1 - Label","Event 1 - Value","Relation 1 - Label","Relation 1 - Value","Website 1 - Label","Website 1 - Value","Custom Field 1 - Label","Custom Field 1 - Value","Notes","Labels"]
json_file_path = "result.json"


# --- Step 2: Load the JSON file into a Python dictionary ---
with open(json_file_path, 'r', encoding="utf-8") as f:
    data = json.load(f)

# --- Step 3: Access the 'contacts' -> 'list' part of the data ---
if 'contacts' in data and 'list' in data['contacts']:
    contacts_list = data['contacts']['list']
else:
    print("Error: 'contacts' or 'list' key not found in the JSON structure.")
    contacts_list = []

# --- Step 4: Convert the list of contacts (dictionaries) into a Pandas DataFrame ---
if contacts_list:
    df_original = pd.DataFrame(contacts_list)
    df_original.to_csv('contacts_long_format.csv', index=False)
    print("Dummy CSV 'contacts_long_format.csv' created.")
    print("\nOriginal DataFrame (first 5 rows):")
    print(df_original.head())

    # --- 2. Load the CSV file into a Pandas DataFrame ---
    csv_file_path = 'contacts_long_format.csv' # Replace with your actual CSV file path
    df = pd.read_csv(csv_file_path)

    # --- 3. Identify the columns to group by and the column to pivot ---
    # The columns that uniquely identify a person
    id_vars = ['first_name', 'last_name']

    # The column containing the phone numbers
    phone_value_col = 'phone_number'

    # --- 4. Group by `id_vars` and create a list of phone numbers for each group ---
    # We'll use a `groupby` and then apply a transformation to collect all phone numbers.

    # First, ensure all ID variables are treated as a single identifier for grouping
    df['person_id'] = df[id_vars].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

    # Now, group by this `person_id` and collect phone numbers into a list
    grouped_phones = df.groupby('person_id')[phone_value_col].apply(list).reset_index()
    grouped_phones.rename(columns={phone_value_col: 'Phone Numbers List'}, inplace=True)

    # Split the `person_id` back into `Given Name` and `Family Name`
    grouped_phones['Given Name'] = grouped_phones['person_id'].apply(lambda x: x.split('_')[0])
    grouped_phones['Family Name'] = grouped_phones['person_id'].apply(lambda x: x.split('_')[1])
    grouped_phones.drop(columns=['person_id'], inplace=True)


    # --- 5. Expand the list of phone numbers into separate columns with Google Contacts headers ---
    max_phones = grouped_phones['Phone Numbers List'].apply(len).max()

    # Create new columns like 'Phone 1 - Type', 'Phone 1 - Value', 'Phone 2 - Type', 'Phone 2 - Value', etc.
    # For simplicity, we'll assume all imported numbers are 'Mobile' or 'Home' for now.
    # You could modify this if your original data contains phone types.
    google_phone_cols = []
    for i in range(max_phones):
        google_phone_cols.append(f'Phone {i+1} - Type')
        google_phone_cols.append(f'Phone {i+1} - Value')

    # Prepare the data for the new phone columns
    phone_data_for_df = []
    for index, row in grouped_phones.iterrows():
        phone_row = []
        for i in range(max_phones):
            if i < len(row['Phone Numbers List']):
                # You can set a default type like 'Mobile' or 'Home'
                # Or map from an existing 'Phone Type' column in your original data if available
                phone_row.extend(['Mobile', row['Phone Numbers List'][i]]) # Defaulting to 'Mobile' type
            else:
                phone_row.extend(['', '']) # Empty if no more phone numbers
        phone_data_for_df.append(phone_row)

    df_phones_expanded = pd.DataFrame(phone_data_for_df, columns=google_phone_cols)

    # Concatenate the 'Given Name', 'Family Name' with the new phone columns
    # We'll also drop the original 'First Name' and 'Last Name' if they exist,
    # as we're now using 'Given Name' and 'Family Name' for Google Contacts.
    df_final = pd.concat([grouped_phones[['Given Name', 'Family Name']], df_phones_expanded], axis=1)


    # --- 6. Add other essential Google Contacts headers (even if empty) ---
    # It's often good practice to include some common Google Contacts headers,
    # even if you don't have data for them, to ensure proper parsing.
    # You can get a comprehensive list by exporting a sample from your Google Contacts.

    common_google_headers = [
        'Name', 'Given Name', 'Additional Name', 'Family Name', 'Yomi Name',
        'Given Name Yomi', 'Additional Name Yomi', 'Family Name Yomi',
        'Name Prefix', 'Name Suffix', 'Initials', 'Nickname', 'Short Name',
        'Maiden Name', 'Birthday', 'Gender', 'Location', 'Billing Information',
        'Directory Server', 'Mileage', 'Occupation', 'Sensitivity', 'Hobby',
        'Organizational Unit', 'Instant Messaging Address', 'Notes',
        'Group Membership', 'E-mail 1 - Type', 'E-mail 1 - Value',
        'E-mail 2 - Type', 'E-mail 2 - Value',
        # ... and so on for other fields like addresses, organizations, etc.
        # We'll dynamically add phone headers generated above.
    ]

    # Ensure all generated phone headers are in the list
    for col in google_phone_cols:
        if col not in common_google_headers:
            common_google_headers.append(col)

    # Reindex the DataFrame to include all common Google Contacts headers, filling missing with empty strings
    # This ensures all standard headers are present in the output, even if they are blank.
    df_final = df_final.reindex(columns=common_google_headers, fill_value='')

    # --- 7. Save the transformed DataFrame to a new CSV file with UTF-8 encoding ---
    output_csv_path = 'contacts_google_format.csv'
    df_final.to_csv(output_csv_path, index=False, encoding='utf-8') # Use UTF-8 for Google Contacts

    print(f"\nTransformed data saved to '{output_csv_path}' with Google Contacts headers.")
    print("\nTransformed DataFrame (first 5 rows with Google Contacts headers):")
    # Display only the relevant columns to avoid overwhelming the output
    print(df_final.head(5).loc[:, df_final.columns.str.contains('Name|Phone')])
else:
    print("No contacts found to write to CSV.")