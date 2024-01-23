#imports
import multiprocessing
import PyPDF2
import pandas as pd
from multiprocessing import Pool
import time

#data
years = ['1920', '1921', '1922', '1923', '1924', '1925', '1926', '1927', '1928', '1929', '1930',
          '1931', '1932', '1933', '1934', '1935', '1936', '1937', '1938', '1939', '1940', '1941',
            '1942', '1943', '1944', '1945', '1946', '1947', '1948', '1949', '1950', '1951', '1952',
              '1953', '1954', '1955', '1956', '1957', '1958', '1959', '1960', '1961', '1962', '1963',
                '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', '1974',
                  '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985',
                    '1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996',
                      '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
                        '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018',
                          '2019', '2020', '2021', '2022', '2023', '2024']

def getpassword(file):
  with open("./samples/passwordprotectedfile.pdf", mode='rb') as a_file:
    # Create a PDF reader object
    reader = PyPDF2.PdfReader(a_file)
    pass_ = ""
    data_ = pd.read_csv(file)
    print(f"Getting password from {file}")
    # Loop over each row in the DataFrame
    for index, row in data_.iterrows():
      # Loop over each year in the list
      for year in years:
        # Create a new name with the year appended
        password_ = f"{row['Initials']}{year}"
        is_done = reader.decrypt(password=password_) #0 for now and 2 for yes
        if is_done == 2:
          pass_ = password_
          print(f"Password found and value is {password_}")
          break
    if pass_ != "":
      return pass_ 
  
# Open the encrypted PDF file
if __name__ == "__main__":
  start_time = time.time()
  data_folder = "data"
  male_files = [( f"./{data_folder}/male{i}.csv") for i in range(1, 26)]
  female_files = [(f"./{data_folder}/female{i}.csv") for i in range(1, 63)]
  # Combine all files into a single list
  all_files =  female_files #+ male_files 
  with multiprocessing.Pool() as pool:
    # Use pool.map_async to execute the function in parallel
    result_async = pool.map_async(getpassword, all_files)

    #Get the result (blocks until all processes are done)
    results = result_async.get()

    #Print the result of the function that finished first
    password_value = None
    for item in results:
      if item is not None:
        password_value = item
        break

    print(f"Password after brutforce is:{password_value}")
    # Terminate the remaining processes
    pool.terminate()

    if password_value is not None:
      # Create a new PDF writer object
      with open("./samples/passwordprotectedfile.pdf", mode='rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()
        reader.decrypt(password_value)
        # Copy the decrypted pages to the new PDF writer object
        for pageNum in reader.pages:
          writer.add_page(pageNum)

        # Write the decrypted PDF to a new file
        with open(f'cracked_{password_value}.pdf', mode='wb') as new_file:
          writer.write(new_file)
      end_time = time.time()
      time_req = end_time - start_time
      formatted_time = "{:.2f}".format(time_req)
      print(f"Time Required: {formatted_time}")
    else:
      print("Password didn't found, sorry")
      end_time = time.time()
      time_req = end_time - start_time
      formatted_time = "{:.2f}".format(time_req)
      print(f"Time Required: {formatted_time}")