import operator
from datetime import date, datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from pydantic import validator
from pydantic.fields import Field
from pydantic.generics import GenericModel
from sqlalchemy import Column, Date, cast, func
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.operators import ColumnOperators

from backend.apps.models import Base
from backend.apps.utils.misc import escape_sql_symbols

OpType = TypeVar("OpType")
ValueType = TypeVar("ValueType")
NoneType = TypeVar("NoneType", bound=None)


class OperatorType(str, Enum):
    text = "text"
    number = "number"
    date = "date"
    match = "match"


class EqualOperator(str, Enum):
    eq = "=="


class MatchOperator(str, Enum):
    eq = "=="
    ne = "!="


class CardArrayOperator(str, Enum):
    eq = "contains"
    ne = "!contains"


class TextOperator(str, Enum):
    contains = "contains"
    not_contains = "!contains"
    eq = "=="
    ne = "!="


class NumberOperator(str, Enum):
    ne = "!="  # not equal
    eq = "=="  # equal
    le = "<="  # less than or equal
    lt = "<"  # less than
    ge = ">="  # greater than or equal
    gt = ">"  # greater than


class DateOperator(str, Enum):
    ne = "!="  # not equal
    eq = "=="  # equal
    le = "<="  # less than or equal
    lt = "<"  # less than
    ge = ">="  # greater than or equal
    gt = ">"  # greater than


def not_contains(a: str, b: str) -> bool:
    return b not in a


ops: Dict[Any, Callable[[Any, Any], bool]] = {
    "!=": operator.ne,
    "==": operator.eq,
    "<=": operator.le,
    "<": operator.lt,
    ">=": operator.ge,
    ">": operator.gt,
    "contains": operator.contains,
    "!contains": not_contains,
}


class Option(GenericModel, Generic[ValueType]):
    value: ValueType
    display: Union[int, str]


StrOption = Option[str]
BoolOption = Option[bool]
NoneOption = Option[NoneType]
IntegerNumberOption = Option[int]
FloatNumberOption = Option[float]


class BaseFilter(GenericModel, Generic[OpType, ValueType]):
    op: OpType
    value: ValueType
    op_type: OperatorType
    options: Optional[List[Option]] = Field(None)

    def generate_orm_clause(self, orm: Union[Base, Column]) -> Union[BinaryExpression, ColumnOperators]:
        raise NotImplementedError  # pragma: no cover

    def compare(self, value: Any) -> bool:
        return ops[self.op](value, self.value)

    @classmethod
    async def get_options(cls) -> Optional[List[Any]]:
        options = cls.__fields__.get("options")
        if options and options.default:
            return options.default
        return None


class ArrayFilter(BaseFilter[MatchOperator, Any], Generic[ValueType]):
    op_type: OperatorType = OperatorType.match

    def generate_orm_clause(self, orm: Column) -> BinaryExpression:  # pragma: no cover
        if self.op == MatchOperator.eq:
            return orm.any(self.value)
        else:
            # elif self.op == MatchOperator.ne:
            return func.not_(orm.any(self.value))


class MatchFilter(BaseFilter[MatchOperator, Any], Generic[ValueType]):
    op_type: OperatorType = OperatorType.match

    def generate_orm_clause(self, orm: Column) -> BinaryExpression:  # pragma: no cover
        if self.op == MatchOperator.eq:
            return orm == self.value
        else:
            # elif self.op == MatchOperator.ne:
            return orm != self.value


class EqualFilter(BaseFilter[EqualOperator, Any], Generic[ValueType]):
    op_type: OperatorType = OperatorType.match

    def generate_orm_clause(self, orm: Column) -> BinaryExpression:
        return orm == self.value


class NoneFilter(MatchFilter[NoneType]):
    """
    请注意，如果需要空值筛选，请加上NoneFilter，其他Filter的value不应该是Optional的，否则会和NoneFilter产生歧义，
    如果用户上传的filter有空值，必须要保证该Filter进入NoneFilter里进行校验。
    """

    options: List[NoneOption] = [
        NoneOption(value=None, display="None"),
    ]


class TextFilter(BaseFilter[TextOperator, str]):
    op_type: OperatorType = OperatorType.text

    def generate_orm_clause(self, orm: Column) -> ColumnOperators:  # pragma: no cover
        if self.op == TextOperator.contains:
            return orm.like(f"%{escape_sql_symbols(self.value)}%")
        elif self.op == TextOperator.not_contains:
            return orm.notlike(f"%{escape_sql_symbols(self.value)}%")
        elif self.op == TextOperator.eq:
            return orm == self.value
        else:
            # elif self.op == TextOperator.ne:
            return orm != self.value


class IntegerNumberFilter(BaseFilter[NumberOperator, int]):
    op_type: OperatorType = OperatorType.number

    def generate_orm_clause(self, orm: Column) -> ColumnOperators:  # pragma: no cover
        if self.op == NumberOperator.ne:
            return orm != self.value
        elif self.op == NumberOperator.eq:
            return orm == self.value
        elif self.op == NumberOperator.le:
            return orm <= self.value
        elif self.op == NumberOperator.lt:
            return orm < self.value
        elif self.op == NumberOperator.ge:
            return orm >= self.value
        else:
            # elif self.op == NumberOperator.gt:
            return orm > self.value


class FloatNumberFilter(BaseFilter[NumberOperator, float]):
    op_type: OperatorType = OperatorType.number

    def generate_orm_clause(self, orm: Column) -> ColumnOperators:  # pragma: no cover
        if self.op == NumberOperator.ne:
            return orm != self.value
        elif self.op == NumberOperator.eq:
            return orm == self.value
        elif self.op == NumberOperator.gt:
            return orm > self.value
        elif self.op == NumberOperator.lt:
            return orm < self.value
        elif self.op == NumberOperator.ge:
            return orm >= self.value
        else:
            # elif self.op == NumberOperator.le:
            return orm <= self.value


class DateFilter(BaseFilter[DateOperator, datetime]):
    op_type: OperatorType = OperatorType.date

    @validator("value", pre=True, always=True)
    def format_date(cls, v: str) -> date:
        return datetime.strptime(v, "%Y-%m-%d")

    def generate_orm_clause(self, orm: Column) -> BinaryExpression:  # pragma: no cover
        if self.op == DateOperator.ne:
            return cast(orm, Date) != self.value
        elif self.op == DateOperator.eq:
            return cast(orm, Date) == self.value
        elif self.op == DateOperator.le:
            return cast(orm, Date) <= self.value
        elif self.op == DateOperator.lt:
            return cast(orm, Date) < self.value
        elif self.op == DateOperator.ge:
            return cast(orm, Date) >= self.value
        else:
            # elif self.op == DateOperator.gt:
            return cast(orm, Date) > self.value


opt_to_filter: Dict[str, Type[BaseFilter]] = {
    OperatorType.text: TextFilter,
    OperatorType.match: MatchFilter,
    OperatorType.number: IntegerNumberFilter,
    OperatorType.date: DateFilter,
}

# 当schemas中使用到Union[List[TextFilter],List[NoneFilter]]时，建议使用Union[TextFilters,NoneFilters]
NoneFilters = Sequence[NoneFilter]
TextFilters = Sequence[TextFilter]
IntegerNumberFilters = Sequence[IntegerNumberFilter]
FloatNumberFilters = Sequence[FloatNumberFilter]
DateFilters = Sequence[DateFilter]
