import re

from bs4 import BeautifulSoup, Tag


class LinkedinParser:
    _ABOUT = 'About'
    EXPERIENCE = 'Experience'
    USER_NAME = "user_name"
    RESUME = 'resume'

    def __init__(self):
        self.headers = {'About': True, 'Activity': False, 'Experience': True, 'Education': True, 'Projects': True,
                        'Skills': True, 'Languages': True, 'Interests': False}
        self._display_name_anchor = r'\babout-this-profile\b'

    def get_profile(self, page: str) -> dict:
        if page is None:
            return {}

        soup = BeautifulSoup(page, 'html.parser')
        display_name = self._extract_display_name(soup)
        resume = self._extract_resume(soup)

        return {LinkedinParser.USER_NAME: display_name, LinkedinParser.RESUME: resume}

    def _extract_display_name(self, soup: BeautifulSoup) -> str:
        a = soup.find('a', href=re.compile(self._display_name_anchor))

        return a.text.strip() if a else ''

    def _extract_experience_imp(self, resume_part: list, tag: Tag) -> None:
        ul = tag.find_next('ul')
        if ul is None:
            return

        for li in ul.find_all('li'):
            if li.find('ul') is not None:
                self._extract_experience_imp(resume_part, li)
            else:
                for s in li.find_all(string=True):
                    cur = s.text.strip()
                    if len(cur) == 0:
                        continue
                    if cur in resume_part or (resume_part[0] if len(resume_part) > 0 else 'I_AM_A_GHOST') in cur:
                        continue
                    resume_part.append(cur)

    def _extract_experience(self, resume_part: list, header: Tag, end: Tag) -> None:
        self._extract_experience_imp(resume_part, header)

    @staticmethod
    def _extract_list(resume_part: list, header: Tag, end: Tag) -> None:
        ul = header.find_next('ul')
        if ul is None or (end is not None and ul == end.find_next('ul')):
            return

        for li in ul.find_all('li'):
            for s in li.find_all(string=True):
                cur = s.text.strip()
                if len(cur) == 0:
                    continue
                if cur in resume_part:
                    continue
                resume_part.append(cur)

    @staticmethod
    def _extract_span(resume_part: list, header: Tag, end: Tag or None) -> None:
        sp = header.find_next('span')
        if sp is None or (end is not None and sp == end):
            return

        for s in sp.find_all(string=True):
            cur = s.text.strip()
            if len(cur) == 0:
                continue
            if cur in resume_part:
                continue
            resume_part.append(cur)

    def _on_header(self, resume: dict, header: Tag or None, end: Tag or None) -> None:
        if header is None:
            return

        if not self.headers[header.text]:
            return

        resume_part = resume[header.text]
        if header.text == LinkedinParser.EXPERIENCE:
            self._extract_experience(resume_part, header, end)
        elif header.text == LinkedinParser._ABOUT:
            self._extract_span(resume_part, header, end)
        else:
            self._extract_list(resume_part, header, end)

    def _extract_resume(self, soup: BeautifulSoup) -> dict:
        resume = {key: [] for key, value in self.headers.items() if value}

        previous_header = None
        for t in soup.find_all('span'):
            cur = t.text
            if len(cur) <= 2:
                continue

            if cur not in self.headers:
                continue

            current_header = t
            if previous_header and previous_header.text != current_header.text:
                self._on_header(resume, previous_header, current_header)
            previous_header = current_header

        self._on_header(resume, previous_header, None)

        return resume
