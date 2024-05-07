# flake8: noqa
# todo: сделать проверку бд на неуникальное имя или несуществующий id


# @pytest.mark.anyio
# async def test_create_topic(client: AsyncClient, fastapi_app: FastAPI) -> None:
#     topic_name = "test"
#     response = await client.post(
#         fastapi_app.url_path_for("create_topic"),
#         json={"name": topic_name},
#     )
#     assert response.status_code == 200
#     # created_topic: тип схема = response.json()


#
# @pytest.mark.anyio
# async def test_create_topic_with_empty_name(client: AsyncClient,
#                                             fastapi_app: FastAPI) -> None:
#     topic_name = ""
#     response = await client.post(fastapi_app.url_path_for('topics'),
#                                  json={"name": topic_name})
#     assert response.status_code == 400
#
#
# @pytest.mark.anyio
# async def test_create_topic_with_too_long_name(client: AsyncClient,
#                                                fastapi_app: FastAPI) -> None:
#     topic_name = "A" * 51
#     response = await client.post(fastapi_app.url_path_for("topics"),
#                                  json={"name": topic_name})
#     assert response.status_code == 400
#
#
# @pytest.mark.anyio
# async def test_create_topic_with_already_exists_name(client: AsyncClient) -> None:
#     topic_name = "test"
#
#     response1 = await client.post(fastapi_app.url_path_for("topics"),
#                                   json={"name": topic_name})
#     assert response1.status_code == 200
#
#     response2 = await client.post(fastapi_app.url_path_for("topics"),
#                                   json={"name": topic_name})
#     assert response2.status_code == 400
#
#
# @pytest.mark.aniyo
# async def test_get_all_topics(client: AsyncClient) -> None:
#     response = await client.get(fastapi_app.url_path_for("topics"))
#     assert response.status_code == 200
#
#
# @pytest.mark.aniyo
# async def test_get_topic_by_id(client: AsyncClient,
#                                db: AsyncSession = Depends(get_db_session)) -> None:
#     topic_name = "test"
#
#     topic_db = TopicDAO(db)
#     new_topic = await topic_db.create_topic(topic_name)
#     topic_id = new_topic.id
#
#     response = await client.get(f"{fastapi_app.url_path_for('topics')}/{topic_id}")
#     assert response.status_code == 200
#     assert response.json()["name"] == topic_name
#
#
# @pytest.mark.aniyo
# async def test_get_topic_not_found(client: AsyncClient) -> None:
#     topic_id = uuid.uuid4()
#     response = await client.get(f"{fastapi_app.url_path_for('topics')}/{topic_id}")
#     assert response.status_code == 404
#
#
# @pytest.mark.aniyo
# async def test_put_topic(client: AsyncClient, db: AsyncSession) -> None:
#     old_topic_name = "test1"
#
#     topic_db = TopicDAO(db)
#     new_topic = await topic_db.create_topic(old_topic_name)
#     topic_id = new_topic.id
#
#     new_topic_name = "test2"
#     data = {"id": topic_id, "name": new_topic_name}
#     response = await client.put(f"{fastapi_app.url_path_for('topics')}/{topic_id}",
#                                 json=data)
#     assert response.status_code == 200
#
#
# @pytest.mark.aniyo
# async def test_put_topic_not_found(client: AsyncClient) -> None:
#     topic_id = uuid.uuid4()
#     new_topic_name = "test"
#     data = {"id": topic_id, "name": new_topic_name}
#
#     response = await client.put(f"/topics/name", json=data)
#     assert response.status_code == 400
#
#
# @pytest.mark.aniyo
# async def test_put_topic_with_empty_name(client: AsyncClient, db: AsyncSession) -> None:
#     old_topic_name = "test"
#
#     topic_db = TopicDAO(db)
#     new_topic = await topic_db.create_topic(old_topic_name)
#     topic_id = new_topic.id
#
#     new_topic_name = ""
#     data = {"id": topic_id, "name": new_topic_name}
#     response = await client.put(f"/topics/name", json=data)
#     assert response.status_code == 400
#
#
# @pytest.mark.aniyo
# async def test_put_topic_with_too_long_name(client: AsyncClient,
#                                             db: AsyncSession) -> None:
#     old_topic_name = "test"
#
#     topic_db = TopicDAO(db)
#     new_topic = await topic_db.create_topic(old_topic_name)
#     topic_id = new_topic.id
#
#     new_topic_name = "A" * 51
#     data = {"id": topic_id, "name": new_topic_name}
#     response = await client.put(f"/topics/name", json=data)
#     assert response.status_code == 400
#
#
# @pytest.mark.aniyo
# async def test_put_topic_with_already_exists_name_and_the_same_id(client: AsyncClient,
#                                                                   db: AsyncSession) -> None:
#     topic_name = "test"
#
#     topic_db = TopicDAO(db)
#     new_topic = await topic_db.create_topic(topic_name)
#     topic_id = new_topic.id
#
#     data = {"id": topic_id, "name": topic_name}
#     response = await client.put(f"/topics/name", json=data)
#     assert response.status_code == 400
#
#
# @pytest.mark.aniyo
# async def test_put_topic_with_already_exists_name_and_other_id(client: AsyncClient,
#                                                                db: AsyncSession) -> None:
#     other_topic_name = "test1"
#     topic_db = TopicDAO(db)
#     await topic_db.create_topic(other_topic_name)
#
#     old_topic_name = "test2"
#     new_topic = await topic_db.create_topic(old_topic_name)
#     topic_id = new_topic.id
#
#     data = {"id": topic_id, "name": other_topic_name}
#     response = await client.put(f"/topics/name", json=data)
#     assert response.status_code == 400
