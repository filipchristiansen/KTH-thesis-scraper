# KTH Thesis Scraper

A simple scraper for extracting information about all thesis projects given at [KTH Royal Institute of Technology](https://www.kth.se/en) (*internal or with an external partner*), which are available at the [KTH Degree Project Portal](https://kth.powerappsportals.com). The creation of this scraper was motivated by the lack of support for filtering projects (*by e.g. location, organization, etc.*), and is made available in case someone else might find it useful.

Running the scraper requires Python 3.8 or later (*due to the use of built-in type annotations*), an installation of [Firefox](https://www.mozilla.org), and the packages listed in [requirements.txt](requirements.txt). The scraper is run by executing [scraper.py](scraper.py) which will create a file named [KTH_thesis_projects.csv](KTH_thesis_projects.csv), containing information about all thesis projects.

A set of keywords can be passed when calling the scraper. This will create new columns in the results, indicating whether the description of a project contains a given keyword. See the main function in [scraper.py](scraper.py) for an example.

For testing purposes, the scraper can be run with the `--debug` flag set to `True`, which will limit the scraping to the first `5` thesis projects.

*Note: The [KTH Degree Project Portal](https://kth.powerappsportals.com) contains information about more than just thesis projects (`Degree project`), i.e. there are two other categories: `Seasonal and part time jobs` and `Internship`. To get only thesis projects, filter the column `Assignment type` for `Degree project`.*
