from src.schemas.entities import EntityAddSchema, EntitySchema, EntityUpdateSchema
from src.utils.database import DBManager


async def test_entities_crud(db: DBManager):
    name = f"db_entity_123"
    new_entity = await db.entities.add_one(EntityAddSchema(
        name=name,
        description="Тестовая сущность",
    ))
    assert new_entity.name == name
    await db.commit()

    entity: EntitySchema | None = await db.entities.get_one_or_none(id=new_entity.id)
    assert entity
    assert entity.name == name

    entity_by_name: EntitySchema | None = await db.entities.get_by_name(name)
    assert entity_by_name
    assert entity_by_name.id == new_entity.id

    updated_entity: EntitySchema = await db.entities.edit(
        EntityUpdateSchema(description="Обновлённое описание"),
        id=new_entity.id,
    )
    await db.commit()
    assert updated_entity.description == "Обновлённое описание"

    await db.entities.delete(id=new_entity.id)
    await db.commit()

    deleted_entity: EntitySchema | None = await db.entities.get_one_or_none(id=new_entity.id)
    assert not deleted_entity


async def test_get_all_entities(db: DBManager):
    entities = await db.entities.get_all()
    assert len(entities) >= 3


async def test_get_entity_by_name_not_found(db: DBManager):
    entity: EntitySchema | None = await db.entities.get_by_name("noex123123")
    assert entity is None