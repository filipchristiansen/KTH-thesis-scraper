import time
from argparse import ArgumentParser
from typing import Any, Dict, List, Union

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm


class KTHThesisScraper(webdriver.Firefox):
    def __init__(self):
        webdriver.Firefox.__init__(self)

    def __call__(self, keywords: Union[Dict[str, List[str]], None] = None, debug: bool = False) -> None:

        # get thesis projects
        thesis_projects = self._get_thesis_projects(debug=debug)

        # get the description for each thesis project
        for thesis in tqdm(thesis_projects):
            thesis['Description'] = self._get_thesis_description(thesis['url'])

        df_thesis_projects = pd.DataFrame(thesis_projects)

        if keywords is not None:
            df_thesis_projects = self._add_keywords(df_thesis_projects, keywords)

        file_prefix = 'debug_' if debug else ''
        df_thesis_projects.to_csv(file_prefix + 'KTH_thesis_projects.csv', index=False)

    def _get_thesis_projects(self, debug: bool = False) -> List[Dict[str, Any]]:

        self.get('https://kth.powerappsportals.com')
        time.sleep(2)

        # change language to English
        self.find_element(By.CLASS_NAME, 'dropdown-toggle').click()
        dropdown_menu = self.find_element(By.CLASS_NAME, 'dropdown-menu')
        dropdown_menu.find_elements(By.TAG_NAME, 'a')[1].click()
        time.sleep(2)

        # get column names in English
        column_names = ['url'] + [
            col.find_element(By.CSS_SELECTOR, 'a').get_attribute('aria-label')
            for col in self.find_elements(By.CSS_SELECTOR, 'th.sort-enabled')
        ]

        # switch back to Swedish (to get a preferred )
        self.find_element(By.CLASS_NAME, 'dropdown-toggle').click()
        dropdown_menu = self.find_element(By.CLASS_NAME, 'dropdown-menu')
        dropdown_menu.find_elements(By.TAG_NAME, 'a')[0].click()
        time.sleep(2)

        column_names = ['url'] + [
            col.find_element(By.CSS_SELECTOR, 'a').get_attribute('aria-label')
            for col in self.find_elements(By.CSS_SELECTOR, 'th.sort-enabled')
        ]

        thesis_projects = []
        next_page = 2

        while True:
            table = self.find_element(By.CSS_SELECTOR, '.table > tbody:nth-child(2)')
            for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
                row_content = []
                for i, col in enumerate(row.find_elements(By.CSS_SELECTOR, 'td')):
                    if i == 0:
                        # get url to project page
                        content = col.find_element(By.CSS_SELECTOR, 'a')
                        row_content.append(content.get_attribute('href'))
                    else:
                        content = col

                    # extract text from cell
                    row_content.append(content.text)

                # add project dict to list of projects
                thesis_projects.append(dict(zip(column_names, row_content)))

                if debug and len(thesis_projects) >= 5:
                    return thesis_projects

            # check if there is a next page
            pagination = self.find_element(By.CSS_SELECTOR, '.pagination > li:last-child > a:nth-child(1)')
            if int(pagination.get_attribute('data-page')) == next_page:
                pagination.click()
                next_page += 1
                time.sleep(2)
                continue

            return thesis_projects

    def _get_thesis_description(self, url: str) -> str:
        self.get(url)
        time.sleep(0.5)
        description = self.find_element(By.CSS_SELECTOR, '#aca_description')
        return description.text

    def _add_keywords(self, df: pd.DataFrame, keywords: Dict[str, List[str]]) -> pd.DataFrame:
        for keyword, values in keywords.items():
            # contains either the keyword or any of the synonyms
            df[keyword] = df['Description'].str.lower().str.contains('|'.join([keyword] + values))
        return df


def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', type=bool, default=False, help='Debug mode')
    args = parser.parse_args()

    # Example keywords
    # E.g.
    #       {'deep learning': ['neural networks']}
    #   will add a column named 'deep learning' to the results and set it to True if the project description contains
    #   either 'deep learning' or 'neural networks'.

    keywords = {
        'deep learning': ['neural networks'],
        'machine learning': [
            'machine learning',
            'deep learning',
            'neural networks',
            'artificial intelligence',
            'maskininlärning',
        ],
    }

    KTHThesisScraper()(keywords=keywords, debug=args.debug)


if __name__ == '__main__':
    main()
