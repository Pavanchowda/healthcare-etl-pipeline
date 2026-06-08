class QualityReport:

    def print_section(self, title):
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50)

    def show_missing_columns(self, dataset_name, missing_columns):
        self.print_section(f"{dataset_name} - Missing Columns")

        if missing_columns:
            print(missing_columns)
        else:
            print("No missing columns found")

    def show_missing_values(self, dataset_name, missing_values):
        self.print_section(f"{dataset_name} - Missing Values")
        print(missing_values)

    def show_duplicate_count(self, dataset_name, duplicate_count):
        self.print_section(f"{dataset_name} - Duplicate Rows")
        print(duplicate_count)

    def show_invalid_records(self, title, dataframe):
        self.print_section(title)
        print("Invalid record count:", len(dataframe))
        print(dataframe.head())