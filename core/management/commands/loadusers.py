import csv
from django.core.management.base import BaseCommand
from core.models import Lecturer, Student, User, Department
from django.conf import settings
import os
import re

class Command(BaseCommand):
    help = 'Load users from Examination List Report'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        # return super().add_arguments(parser)
    
    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            output_file_path = os.path.join(settings.BASE_DIR, 'created_users_log.csv')
            with open(output_file_path, mode='a', newline='') as outfile:

                fieldnames = ['username', 'password', 'user_type', 'department']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)

                # write the header
                if outfile.tell() == 0:
                    writer.writeheader()

                for row in reader:
                    # first_name, middle_name, last_name = Command.clean_omani_name(row['Student Name'])
                    # self.stdout.write(' '.join([first_name, last_name]))
                    
                    lec = Command.clean_lecturer_name(row['Lecturer Name'])
                    self.stdout.write(Command.format_lecturer_info(lec))
    
    def format_lecturer_info(user_info):
        """
        Combines the user information dictionary into a formatted string.
        """
        # Extract values from the dictionary
        username = user_info.get("username", "")
        prefix = user_info.get("prefix", "")
        first_name = user_info.get("first_name", "")
        middle_name = user_info.get("middle_name", "")
        last_name = user_info.get("last_name", "")

        # Construct the name parts
        name_parts = [prefix, first_name, middle_name, last_name]
        # Join non-empty name parts with a space
        full_name = ",".join(part for part in name_parts if part).strip()

        # Format the output string
        return f"{full_name} ({username})"
    
    def clean_lecturer_name(lecturer_entry):
        # Split the entry by ' - ' to separate ID and Name
        try:
            user_id, name = lecturer_entry.split(' - ', 1)
        except ValueError:
            raise ValueError("The entry is not in the expected format: 'ID - Name'")

        # Set the username from the ID
        username = user_id.strip()

        # Define possible prefixes with optional trailing period and no space requirement afterward
        prefix_pattern = r'^(Mr\.?|Ms\.?|Mrs\.?|Dr\.?|Prof\.?)'
        prefix = None

        # Use regex to detect and remove prefix from the name
        match = re.match(prefix_pattern, name, re.IGNORECASE)
        if match:
            # Extract and clean the prefix
            prefix = match.group(0).replace('.', '').strip()
            # Remove the prefix from the name
            name = name[match.end():].strip()

        # Split the remaining name into parts and capitalize each part
        name_parts = name.split()
        name_parts = [part.capitalize() for part in name_parts]

        # Assign first, middle, and last names
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""

        # Return the cleaned data as a dictionary for easy insertion
        return {
            "username": username,
            "prefix": prefix,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name
        }

    def clean_omani_name(full_name):
        # Step 1: Replace hyphen with space
        cleaned_name = full_name.replace('-', ' ')

        # Step 2: Move 'Al' to the beginning of the next word
        words = cleaned_name.split()
        cleaned_words = []
        skip_next = False

        for i in range(len(words)):
            if skip_next:
                skip_next = False
                continue

            if words[i].lower() == 'al' and i < len(words) - 1:
                # Prepend 'Al' to the next word without capitalizing yet
                cleaned_words.append(f"Al{words[i + 1]}")
                skip_next = True
            else:
                cleaned_words.append(words[i])
        
        # Step 3: Join the cleaned words back into a string
        cleaned_name = ' '.join(cleaned_words)

        # Step 4: Capitalize the entire cleaned name at once
        cleaned_name = cleaned_name.title()

        # Step 5: Extract first name, middle name, and last name
        name_parts = cleaned_name.split()

        # First name is the first part
        first_name = name_parts[0]

        # Middle name is everything between the first and last parts (if present)
        if len(name_parts) > 2:
            middle_name = ' '.join(name_parts[1:-1])
        else:
            middle_name = ''
        
        # Last name is the last part
        last_name = name_parts[-1] if len(name_parts) > 1 else ''

        return first_name, middle_name, last_name


