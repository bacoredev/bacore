"""Test data generation."""
from dataclasses import dataclass
from faker import Faker
from hypothesis import strategies as st
from typing import Optional


@dataclass(slots=True, frozen=True)
class CountryCodes:
    """Country code for countries and regions.

    This class is used by the FakerData class to specify the locale for the Faker instance.
    Individual countries are accessed as attributes and regions as classmethods.

    Examples:
        >>> CountryCodes.denmark
        'da_DK'

        >>> CountryCodes.nordics()
        ['da_DK', 'fi_FI', 'no_NO', 'sv_SE']
    """

    china = 'zh_CN'
    denmark = 'da_DK'
    estonia = 'et_EE'
    finland = 'fi_FI'
    france = 'fr_FR'
    germany = 'de_DE'
    italy = 'it_IT'
    latvia = 'lv_LV'
    lithuania = 'lt_LT'
    netherlands = 'nl_NL'
    norway = 'no_NO'
    poland = 'pl_PL'
    portugal = 'pt_PT'
    russia = 'ru_RU'
    spain = 'es_ES'
    sweden = 'sv_SE'
    ukraine = 'uk_UA'
    united_kingdom = 'en_GB'
    united_states_of_america = 'en_US'

    @classmethod
    def nordics(cls):
        return [cls.denmark, cls.finland, cls.norway, cls.sweden]

    @classmethod
    def europe(cls):
        countries = cls.nordics() + [cls.estonia, cls.latvia, cls.lithuania,
                                     cls.france, cls.germany, cls.italy,
                                     cls.netherlands, cls.poland, cls.portugal,
                                     cls.spain, cls.ukraine, cls.united_kingdom]
        return sorted(countries)

    @classmethod
    def world(cls):
        countries = cls.europe() + [cls.china, cls.russia, cls.united_states_of_america]
        return sorted(countries)

    @classmethod
    def for_locale(cls, name: str) -> list[str]:
        """Takes a locale specifier (country or region) and returns country codes.
        If the "attribute" is a function, then is it called.
        """
        if callable(getattr(cls, name)):
            return getattr(cls, name)()
        else:
            return getattr(cls, name)


@dataclass
class PytestRunData:
    """Test result."""
    pytest_exit_codes = {
        0: "All tests were collected and passed successfully.",
        1: "Tests were collected and run but some of the tests failed.",
        2: "Test execution was interrupted by the user.",
        3: "Internal error happened while executing tests.",
        4: "pytest command line usage error.",
        5: "No tests were collected."
    }
    status: int
    testrun_parameters: Optional[str] = None

    @property
    def message(self) -> str:
        """Return status message."""
        return self.pytest_exit_codes[self.status]


@dataclass
class FakerData(Faker):
    """Test data for locale (country or region).

    Adding additional data providers for a locale is only supported by `Faker` for one locale.
    If multiple locales (a region) is used, then will additional data providers not be added.

    use_weighting: Tries to match the real world occurrences of the data. If `True` will data generation be slower.

    Parameters:
        country_or_region: A country or region for which test data is generated.

    Funtions:
        seed(): Seed the random number generator for reproducibility. Use only for "our own" test purposes.

    Examples:
        >>> FakerData.seed(1)
        >>> s = FakerData('sweden')
        >>> s.name()
        'Marianne Åkesson'
    """

    def __init__(self, country_or_region: str):
        country_codes = CountryCodes.for_locale(country_or_region)
        super().__init__(country_codes, use_weighting=False)


class TestData:
    """Test data strategies for hypothesis with Faker data.

    From the `hypothesis` documentation perspective is this a +dumb+ or at least less optimal way to generate test data.
    Generally should we try to from_testdata [data based on core hypothesis strategies](https://hypothesis.readthedocs.io/en/latest/data.html).
    A lot can, for example, be accomplished with the `st.from_regex` strategy. *However*, sometimes is all you need just a name
    or an isin or something similar, and then can the functions below be used.
    """

    def __init__(self, country_or_region: str):
        self.country_or_region = country_or_region

    def company(self):
        return st.builds(FakerData(self.country_or_region).company)

    def currency_code(self):
        return st.builds(FakerData(self.country_or_region).currency_code)

    def first_name(self):
        return st.builds(FakerData(self.country_or_region).first_name)

    def isin(self):
        match self.country_or_region:
            case "sweden":
                return st.from_regex(r"\ASE[0-9]{10}\Z")
            case "finland":
                return st.from_regex(r"\AFI[0-9]{10}\Z")
            case _:
                return st.from_regex(r"\A[X]{2}[A-Z0-9]{9}[0-9]\Z")

    def last_name(self):
        return st.builds(FakerData(self.country_or_region).last_name)
