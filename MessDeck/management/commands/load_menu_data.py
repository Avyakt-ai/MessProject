
# To run this file to load the json file into the models just go to terminal and type "python manage.py load_menu_data"




import json
from datetime import datetime
from django.core.management.base import BaseCommand
from MessDeck.models import MenuDate, MenuItem  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Loads menu data from JSON file into MenuDate model'

    def handle(self, *args, **kwargs):
        file_path = 'MessDeck/Mess Menu Sample.json'  # Replace with the actual path to your JSON file

        with open(file_path, 'r') as file:
            data = json.load(file)

            for date_str, meals in data.items():
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                menu_date, created = MenuDate.objects.get_or_create(month_date=date_obj)

                if 'BREAKFAST' in meals:
                    menu_date.breakfast_items = ', '.join(meals['BREAKFAST'])

                if 'LUNCH' in meals:
                    menu_date.lunch_items = ', '.join(meals['LUNCH'])

                if 'DINNER' in meals:
                    menu_date.dinner_items = ', '.join(meals['DINNER'])

                menu_date.save()

        self.stdout.write(self.style.SUCCESS('Menu data has been loaded successfully.'))
