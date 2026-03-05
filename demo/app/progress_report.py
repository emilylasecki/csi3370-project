# ds models and other controllers go here

class Progress_Report:

    def __init__(self, reportID, generationDate):
        self.reportID = reportID
        self.generationDate = generationDate

    # getters

    def get_reportID(self):
        return self.reportID
    
    def get_generationDate(self):
        return self.generationDate
    
    # setters

    def set_reportID(self, id):
        self.reportID = id

    def set_generationDate(self, date):
        self.generationDate = date

    # use case functions

    def apply_models(): # will want to use helpers
        return 0
    
    def display_report():
        return 0