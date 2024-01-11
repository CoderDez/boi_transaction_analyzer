import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils.dataframe import dataframe_to_rows
from utils import get_month_name


class TransactionAnalyzer:
    """
    A class to analyze transaction data from a Bank Account from a CSV file.
    """

    def __init__(self, file_path: str):
        """
        Initializes the TransactionAnalyzer class.

        Args:
        - file_path (str): The path to the CSV file containing transaction data.
        """
        try:
            self.__debits = {}
            self.__credits = {}
            self.__process_file(file_path)

        except Exception as e:
            print(e)


    def __process_file(self, file_path):
        """
        Processes the CSV file and updates debits and credits accordingly.

        Args:
        - file_path (str): The path to the CSV file containing transaction data.
        """
        try:
            with open(file_path, "r") as file:
                # skip header
                next(file)
                for line in file:
                    self.__process_line(line.strip().split(","))
        except Exception as e:
            print(f"Error processing file: {e}")



    def __process_line(self, components):
        """
        Processes each line of the CSV file and updates debits or credits.

        Args:
        - components (list): A list of components extracted from a CSV line.
        """
        if len(components) == 5:
            date, details, debit, credit, _ = components
            day, month = date.split("/")[:2]

            if debit:
                self.__update_transactions(self.__debits, int(month), int(day), details, float(debit))
            elif credit:
                self.__update_transactions(self.__credits, int(month), int(day), details, float(credit))


    def __update_transactions(self, transaction_type, month, day, details, amount):
        """
        Updates the transaction records for debits or credits.

        Args:
        - transaction_type (dict): The type of transaction (debits or credits) to be updated.
        - month (str): The month of the transaction.
        - day (str): The day of the transaction.
        - details (str): Details of the transaction.
        - amount (float): The transaction amount.
        """

        if month not in transaction_type:
            transaction_type[month] = {day: {details: amount}}
        else:
            if day in transaction_type[month]:
                current_amount = transaction_type[month][day].get(details, 0)
                transaction_type[month][day][details] = current_amount + amount
            else:
                transaction_type[month][day] = {details: amount}



    def get_debits(self) -> dict:
        """
        Returns the debits dictionary containing transaction details.

        Returns:
        - dict: A dictionary containing debit transaction details.
        """
        return self.__debits
    


    def get_credits(self) -> dict:
        """
        Returns the credits dictionary containing transaction details.

        Returns:
        - dict: A dictionary containing credit transaction details.
        """
        return self.__credits
    
    

    def get_monthly_credits(self) -> dict:
        """
        Calculates the total monthly credits.

        Returns:
        - dict: A dictionary containing total credits for each month.
        """
        try:
            monthly_credits = {}
            for month in self.__credits:
                monthly_credits[month] = sum(
                    sum(details.values()) for day, details in self.__credits[month].items()
                )
            return monthly_credits

        except Exception as e:
            print(f"ERROR getting monthly credits: {e}")


    def display_monthly_credits(self):
        """
        Generates a formatted string displaying monthly credits.

        Returns:
        str: A formatted string displaying monthly credits, separated by month and amount.
        """
        try:
            display = "Monthly Credits:\n"
            display += "-" *  (len(display) -1) + "\n"

            for month, amount in self.get_monthly_credits().items():
                display += f"{get_month_name(month)} - {round(amount,2)}\n"

            return display
        except Exception as e:
            print(f"ERROR while trying to display monthly credits: {e}")


    def get_average_monthly_credits(self) -> float:
        """
        Calculates the average monthly credits.

        Returns:
        - float: The average monthly credits.
        """
        try:
            monthly_credits = self.get_monthly_credits()
            average = sum(monthly_credits.values()) / len(monthly_credits)
            return round(average, 2)


        except ZeroDivisionError:
            print("No monthly credits found.")
        except Exception as e:
            print(f"ERROR when getting average monthly credits: {e}")



    def get_monthly_debits(self) -> dict:
        """
        Calculates the total monthly debits.

        Returns:
        - dict: A dictionary containing total debits for each month.
        """
        try:
            monthly_debits = {}
            for month in self.__debits:
                monthly_debits[month] = sum(
                    sum(details.values()) for day, details in self.__debits[month].items()
                )
            return monthly_debits

        except Exception as e:
            print(f"ERROR getting monthly debits: {e}")


    def display_monthly_debits(self):
        """
        Generates a formatted string displaying monthly debits.

        Returns:
        str: A formatted string displaying monthly debits, separated by month and amount.
        """
        try:
            display = "Monthly Debits:\n"
            display += "-" *  (len(display) -1) + "\n"

            for month, amount in self.get_monthly_debits().items():
                display += f"{get_month_name(month)} - {round(amount,2)}\n"

            return display
        except Exception as e:
            print(f"ERROR while trying to display monthly credits: {e}")



    def get_average_monthly_debits(self) -> float:
        """
        Calculates the average monthly debits.

        Returns:
        - float: The average monthly debits.
        """
        try:
            monthly_debits = self.get_monthly_debits()
            average = sum(monthly_debits.values()) / len(monthly_debits)
            return round(average, 2)

        except ZeroDivisionError:
            print("No monthly debits found.")
        except Exception as e:
            print(f"ERROR when getting average monthly debits: {e}")


    def export_credits_excel(self, output_path: str):
        """
        Export credit transaction data to an Excel file.

        Args:
        - output_path (str): The file path to save the Excel file.
        """
        try:
            credits_data = self.__format_data_for_output(self.__credits)
            self.__create_excel(output_path, credits_data)
        except Exception as e:
            print(f"ERROR while exporting credits to excel: {e}")

    def export_debits_excel(self, output_path: str):
        """
        Export debit transaction data to an Excel file.

        Args:
        - output_path (str): The file path to save the Excel file.
        """

        try:
            debits_data = self.__format_data_for_output(self.__debits)
            self.__create_excel(output_path, debits_data)

        except Exception as e:
            print(f"ERROR while exporting debits to excel: {e}")

    def __format_data_for_output(self, data: dict) -> list[dict]:
        """
        Formats transaction data for output in Excel.

        Args:
        - data (dict): A dictionary containing transaction details.

        Returns:
        - list[dict]: A list of dictionaries with formatted transaction data.
        """
        formatted_data = []

        for month, days_data in data.items():
            for day, details_data in days_data.items():
                for detail, amount in details_data.items():
                    formatted_data.append({
                        'Month': month,
                        'Day': day,
                        'Details': detail,
                        'Amount': amount
                    })

        return formatted_data

    def __create_excel(self, output_path: str, data: list[dict]):
        """
        Creates an Excel file from provided data.

        Args:
        - output_path (str): The file path to save the Excel file.
        - data (list[dict]): A list of dictionaries containing transaction data.

        Writes the formatted transaction data into an Excel file at the specified output path.
        """
        df = pd.DataFrame(data)
        wb = Workbook()
        ws = wb.active

        for r in dataframe_to_rows(df, index=False, header=False):
            ws.append(r)

        columns_width = {'A': 15, 'B': 10, 'C': 30, 'D': 12}
        headers = ["Month", "Day", "Details", "Amount"]

        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True)
            ws.column_dimensions[chr(64 + col)].width = columns_width[chr(64 + col)]

        wb.save(output_path)

