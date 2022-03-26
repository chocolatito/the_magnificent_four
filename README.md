# the_magnificent_four
Scraping on wikipedia the _professional boxing record_ of the boxers:
- [__M. M. Hagler__](https://en.wikipedia.org/wiki/Marvelous_Marvin_Hagler)
- [___T. Heans___](https://en.wikipedia.org/wiki/Thomas_Hearns),
- [___S. R. Leonard___](https://en.wikipedia.org/wiki/Sugar_Ray_Leonard)
- and [___R. 'Manos de Piedra' Durán___](https://en.wikipedia.org/wiki/Roberto_Dur%C3%A1n).  

---
Generate new data y create un `.md` for the fours.

Required packages:
```sh
pip3 install -r requirements.txt
```

Execution
```sh
python3 'a - scraper.py'
python3 'b - generator_md_files.py'
```

- `a - scraper.py`
  + download the html code from the links in the `urls.py` file.
  + create/overwrite `img_urls.txt` file.
  + generate the `.csv` files.

> All html code is stored in the `html_codes` folder and all `.csv` files in the `csv_files` folder

- `b - generator_md_files.py`
  + read the files from the `html_codes` and `csv_files` folders and `img_urls.txt` file to generate the `.md` files.

> All `.md` files is stored in the `markdown_files`. 
