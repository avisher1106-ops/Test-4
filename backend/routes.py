from fastapi import APIRouter, Path, Request
from pydantic import BaseModel, Field

from fruityvice_client import get_all_fruits

router = APIRouter(prefix="/api", tags=["Fruits"])

ERROR_RESPONSES = {
    502: {
        "description": "The Fruityvice API could not be reached or returned invalid data"
    }
}


class Nutritions(BaseModel):
    calories: int | float = Field(examples=[52])
    fat: float = Field(examples=[0.2])
    sugar: float = Field(examples=[10.3])
    carbohydrates: float = Field(examples=[11.4])
    protein: float = Field(examples=[0.3])


class Fruit(BaseModel):
    name: str = Field(examples=["Apple"])
    id: int = Field(examples=[6])
    family: str = Field(examples=["Rosaceae"])
    order: str = Field(examples=["Rosales"])
    genus: str = Field(examples=["Malus"])
    nutritions: Nutritions


def _matches(fruit: dict, text: str) -> bool:
    name = fruit.get("name")
    return isinstance(name, str) and text in name.lower()


@router.get(
    "/fruits",
    response_model=list[Fruit],
    summary="Get all fruits",
    description="Returns the full list of fruits from the Fruityvice API.",
    responses=ERROR_RESPONSES,
)
def get_fruits(request: Request):
    fruits = get_all_fruits()
    request.state.total_results = len(fruits)
    return fruits


@router.get(
    "/search/{text}",
    response_model=list[Fruit],
    summary="Search fruits by name",
    description=(
        "Case-insensitive text search on the fruit name. "
        "Returns an empty array when no fruit matches."
    ),
    responses=ERROR_RESPONSES,
)
def search_fruits(
    request: Request,
    text: str = Path(
        description="Text to search for inside the fruit name (case-insensitive).",
        examples=["apple"],
    ),
):
    query = text.strip().lower()
    fruits = get_all_fruits()
    results = [fruit for fruit in fruits if _matches(fruit, query)]
    request.state.total_results = len(results)
    return results


@router.get(
    "/calories/{max}",
    response_model=list[Fruit],
    summary="Get fruits up to a calories limit",
    description=(
        "Returns every fruit whose calories value is lower than or equal to "
        "max. Returns an empty array when no fruit matches."
    ),
    responses=ERROR_RESPONSES,
)
def fruits_by_calories(
    request: Request,
    max: int = Path(
        description="Maximum number of calories per fruit.",
        examples=[50],
    ),
):
    fruits = get_all_fruits()
    results = []
    if max >= 0:
        for fruit in fruits:
            calories = (fruit.get("nutritions") or {}).get("calories")
            if isinstance(calories, (int, float)) and calories <= max:
                results.append(fruit)
    request.state.total_results = len(results)
    return results
