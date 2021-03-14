import pandas as pd
import io


class LogFileToDf:
    """ Object represents data obtained from log file """

    def __init__(self, input_file: io):
        self._df = pd.read_csv(input_file, delimiter=';', usecols=list(range(8)), header=None)
        self._record_idx_list = self.list_idx_per_str_located_in_df_column(search_txt='Record ', col_idx=0)
        self._press_data_empty = self.check_if_records_in_df()
        self._record_df = self.filter_records_data_in_df()

    def list_idx_per_str_located_in_df_column(self, search_txt: str = 'Record ', col_idx: int = 0) -> list:
        return self._df[self._df.iloc[:, col_idx].str.contains(search_txt, regex=False)].index.to_list()

    def check_if_records_in_df(self) -> bool:
        if len(self._record_idx_list) == 0:
            return True
        elif len(self._record_idx_list) == 1:
            record_1_length = self._df.iloc[self._record_idx_list[0] + 1, 1]
            if record_1_length == '0':
                return True
            return False
        else:
            return False

    def filter_records_data_in_df(self) -> pd.DataFrame:
        temp_record_df = pd.DataFrame()
        column_names = ['[Point]', '[Position]', '[Force]', '[Time]', '[Record #]']

        try:
            for i, record_idx in enumerate(self._record_idx_list):
                # read details of record length from cell and use to filter related rows.
                no_of_records = int(self._df.iloc[record_idx+1][1])
                first_record_idx = record_idx+3
                last_record_idx = first_record_idx+no_of_records
                rec_data_df = self._df.iloc[first_record_idx:last_record_idx, 0:4].copy()
                rec_data_df['[Record #]'] = i+1
                temp_record_df = pd.concat([temp_record_df, rec_data_df], ignore_index=True)
            temp_record_df.columns = column_names
            temp_record_df['[Force]'] = pd.to_numeric(temp_record_df['[Force]'])
            temp_record_df['[Position]'] = pd.to_numeric(temp_record_df['[Position]'])
        except ValueError:
            return pd.DataFrame(columns=column_names)
        return temp_record_df

    @property
    def file_summary(self) -> pd.DataFrame:
        summary_df = self._df.iloc[[1]]
        summary_df.columns = self._df.iloc[0]
        return summary_df

    @property
    def press_data_empty(self) -> bool:
        return self._press_data_empty

    @property
    def record_df(self) -> pd.DataFrame:
        return self._record_df
