from enum import Enum


class EntryType(str, Enum):
    CREDIT = "C"
    DEBIT = "D"