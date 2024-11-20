import urllib.request
import urllib.error
import warnings
import pandas as pd
from pathlib import Path


class download_files_from_web:
    def download_files_from_cdaweb(
        self,
        time_range: list = None,
        CDA_LINK: str = "https://cdaweb.gsfc.nasa.gov/pub/data/ulysses/plasma/swics_cdaweb/scs_m1/",
        filename: str = "uy_m1_scs_",
        file_version: str = "_v02.cdf",
        verbose: bool = True,
        data_dir: str = None,
    ):
        """
        Download files from the CDAweb website within a given time range and save them to a specified
        directory.

        Parameters
        ----------
        time_range : list
            A list of two pandas.Timestamp objects that specify the start and stop times of the time
            range of interest. The default is None.
        CDA_LINK : str
            A string that specifies the link to the CDAweb website from which the files are downloaded.
            The default is "https://cdaweb.gsfc.nasa.gov/pub/data/ulysses/plasma/swics_cdaweb/scs_m1/".
        filename : str
            A string that specifies the name of the file to be downloaded. The default is "uy_m1_scs_".
        file_version : str
            A string that specifies the version of the file to be downloaded. The default is "_v02.cdf".
        verbose : bool
            A boolean that specifies whether to print out messages. The default is True.
        data_dir : str
            A string that specifies the directory where the files are saved. The default is None.

        Returns
        -------
        None
        """
        # Get the year, month, and day of the start and stop times
        start_time = time_range[0]
        stop_time = time_range[1]

        start_year = start_time.year
        start_month = start_time.month
        start_day = start_time.day

        stop_year = stop_time.year
        stop_month = stop_time.month
        stop_day = stop_time.day

        # Link to the CDAweb website, from which ephemeris data are pulled
        if CDA_LINK is None:
            raise ValueError("CDA_LINK must be provided")

        # Given that ephemeris files are named in the the format of lexi_ephm_YYYYMMDD_v01.cdf, get a
        # list of all the files that are within the time range of interest
        file_list = []
        for year in range(start_year, stop_year + 1):
            for month in range(start_month, stop_month + 1):
                for day in range(start_day, stop_day + 1):
                    # Create a string for the date in the format of YYYYMMDD
                    date_string = str(year) + str(month).zfill(2) + str(day).zfill(2)

                    # Create a string for the filename
                    updated_filename = filename + date_string + file_version

                    # Create a string for the full link to the file
                    link = CDA_LINK + f"{str(year)}/" + updated_filename

                    # Try to open the link, if it doesn't exist then skip to the next date
                    try:
                        urllib.request.urlopen(link)
                    except urllib.error.HTTPError:
                        # Print in that the file doesn't exist or is unavailable for download from the CDAweb website
                        warnings.warn(
                            f"Following file is unavailable for downloading or doesn't exist. Skipping the file: \033[93m {updated_filename}\033[0m"
                        )
                        continue

                    # If the link exists, then check if the date is within the time range of interest
                    # If it is, then add it to the list of files to download
                    if (
                        (year == start_year)
                        and (month == start_month)
                        and (day < start_day)
                    ):
                        continue
                    elif (
                        (year == stop_year)
                        and (month == stop_month)
                        and (day > stop_day)
                    ):
                        continue
                    else:
                        file_list.append(updated_filename)

        # Download the files in the file list to the data/ephemeris directory
        if data_dir is None:
            data_dir = Path(__file__).resolve().parent.parent / "data/downloaded_data"
        else:
            data_dir = Path(data_dir)
        # If the data directory doesn't exist, then create it
        if verbose:
            print(f"Creating directory: {data_dir} \n")
        Path(data_dir).mkdir(parents=True, exist_ok=True)

        # Download the files in the file list to the data/ephemeris directory
        if not verbose:
            print("Downloading ephemeris files\n")
        for file in file_list:
            # If the file already exists, then skip to the next file
            if (data_dir / file).exists():
                if verbose:
                    print(
                        f"File \033[92m {file}\033[0m already exists in folder \033[92m {data_dir}\033[0m \n"
                    )
                continue
            # If the file doesn't exist, then download it
            urllib.request.urlretrieve(
                CDA_LINK + f"{str(year)}/" + file, data_dir / file
            )
            if verbose:
                print(f"Downloaded ==> \033[92m {file}\033[0m \n")
        return None


# Example usage
input_dict = {
    "time_range": [pd.Timestamp("2001-01-01 00:00"), pd.Timestamp("2001-01-03 12:00")],
    "CDA_LINK": "https://cdaweb.gsfc.nasa.gov/pub/data/ulysses/plasma/swics_cdaweb/scs_m1/",
    "filename": "uy_m1_scs_",
    "file_version": "_v02.cdf",
    "verbose": True,
    "data_dir": None,
}
download_files_from_web().download_files_from_cdaweb(**input_dict)
