import pytest

from core.domain.exceptions.books import (
    BookTitleIsEmptyException,
    BookTitleTooLongException,
    BookTitleTooShortException,
    BookAuthorTooShortException,
    BookAuthorTooLongException,
    BookYearIsEmptyException,
    BookYearNotNumericException,
    BookYearMoreThanCurrentYearException,
    BookYearMustBeFourDigitsException,
    BookStatusIsEmptyException,
    BookStatusMustBeBooleanException,
    BookAuthorIsEmptyException
)

from core.domain.values.books import Title, Author, Year, Status


def test_title():
    assert Title('Title').as_generic_type() == 'Title'


def test_title_empty_fail():
    with pytest.raises(BookTitleIsEmptyException):
        Title('')


def test_title_short_fail():
    with pytest.raises(BookTitleTooShortException):
        Title('a')


def test_title_long_fail():
    with pytest.raises(BookTitleTooLongException):
        Title('a' * 101)


def test_author():
    assert Author('Author').as_generic_type() == 'Author'


def test_author_empty_fail():
    with pytest.raises(BookAuthorIsEmptyException):
        Author('')


def test_author_short_fail():
    with pytest.raises(BookAuthorTooShortException):
        Author('a')


def test_author_long_fail():
    with pytest.raises(BookAuthorTooLongException):
        Author('a' * 101)


def test_year():
    assert Year('2020').as_generic_type() == '2020'
    assert Year('2020') == Year('2020')
    assert Year('2020') < Year('2021')
    assert Year('2020') > Year('2019')


def test_year_empty_fail():
    with pytest.raises(BookYearIsEmptyException):
        Year('')


def test_year_not_numeric_fail():
    with pytest.raises(BookYearNotNumericException):
        Year('2020a')


def test_year_more_than_current_year_fail():
    with pytest.raises(BookYearMoreThanCurrentYearException):
        Year('2025')


def test_year_must_be_four_digits_fail():
    with pytest.raises(BookYearMustBeFourDigitsException):
        Year('202')


def test_status():
    assert Status(True).as_generic_type() == True


def test_status_empty_fail():
    with pytest.raises(BookStatusIsEmptyException):
        Status(None)


def test_status_must_be_boolean_fail():
    with pytest.raises(BookStatusMustBeBooleanException):
        Status(1)
