from datetime import datetime

class SwahiliDateMixin:
    def get_swahili_date(self):
        """Translate the created_at field to Swahili."""
        swahili_months = {
            "January": "Januari",
            "February": "Februari",
            "March": "Machi",
            "April": "Aprili",
            "May": "Mei",
            "June": "Juni",
            "July": "Julai",
            "August": "Agosti",
            "September": "Septemba",
            "October": "Oktoba",
            "November": "Novemba",
            "December": "Desemba",
        }
        
        date_str = self.created_at.strftime('%d %B %Y')  # Example: "20 March 2025"

        # Replace the English month with the Swahili equivalent
        for eng, swa in swahili_months.items():
            date_str = date_str.replace(eng, swa)

        return date_str 
