# flake8: noqa
# todo: сделать проверку бд на неуникальное имя или несуществующий id

"""
@pytest.mark.usefixtures(
    "anyio_backend",
)  # @pytest.mark.anyio не работает. пишет, что не существует такой марки
async def test_create_topic(client: TestClient) -> None:
    topic_name = "test"
    response = await client.post(
        "http://127.0.0.1:8000/api/v1/topic",
        json={"name": topic_name},
    )
    assert response.status_code == 200
    # created_topic: тип схема = response.json()


@pytest.mark.anyio
async def test_create_topic_with_empty_name(client: TestClient) -> None:
    topic_name = ""
    response = client.post("/topics", json={"name": topic_name})
    assert response.status_code == 400


@pytest.mark.anyio
async def test_create_topic_with_too_long_name(client: TestClient) -> None:
    topic_name = "A" * 51
    response = client.post("/topics", json={"name": topic_name})
    assert response.status_code == 400


@pytest.mark.anyio
async def test_create_topic_with_already_exists_name(client: TestClient) -> None:
    topic_name = "test"

    response1 = client.post("/topics", json={"name": topic_name})
    assert response1.status_code == 200

    response2 = client.post("/topics", json={"name": topic_name})
    assert response2.status_code == 400


@pytest.mark.aniyo
async def test_get_all_topics(client: TestClient) -> None:
    response = client.get("/topics")
    assert response.status_code == 200


@pytest.mark.aniyo
async def test_get_topic_by_id(client: TestClient,
                               db: AsyncSession = Depends(get_db_session)) -> None:
    topic_name = "test"

    topic_db = TopicDAO(db)
    new_topic = await topic_db.create_topic(topic_name)
    topic_id = new_topic.id

    response = client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["name"] == topic_name


@pytest.mark.aniyo
async def test_get_topic_not_found(client: TestClient) -> None:
    topic_id = uuid.uuid4()
    response = client.get(f"/topics/{topic_id}")
    assert response.status_code == 404


@pytest.mark.aniyo
async def test_put_topic(client: TestClient, db: AsyncSession) -> None:
    old_topic_name = "test1"

    topic_db = TopicDAO(db)
    new_topic = await topic_db.create_topic(old_topic_name)
    topic_id = new_topic.id

    new_topic_name = "test2"
    data = {"id": topic_id, "name": new_topic_name}
    response = client.put(f"/topics/name", json=data)
    assert response.status_code == 200


@pytest.mark.aniyo
async def test_put_topic_not_found(client: TestClient) -> None:
    topic_id = uuid.uuid4()
    new_topic_name = "test"
    data = {"id": topic_id, "name": new_topic_name}

    response = client.put(f"/topics/name", json=data)
    assert response.status_code == 400


@pytest.mark.aniyo
async def test_put_topic_with_empty_name(client: TestClient, db: AsyncSession) -> None:
    old_topic_name = "test"

    topic_db = TopicDAO(db)
    new_topic = await topic_db.create_topic(old_topic_name)
    topic_id = new_topic.id

    new_topic_name = ""
    data = {"id": topic_id, "name": new_topic_name}
    response = client.put(f"/topics/name", json=data)
    assert response.status_code == 400


@pytest.mark.aniyo
async def test_put_topic_with_too_long_name(client: TestClient,
                                            db: AsyncSession) -> None:
    old_topic_name = "test"

    topic_db = TopicDAO(db)
    new_topic = await topic_db.create_topic(old_topic_name)
    topic_id = new_topic.id

    new_topic_name = "A" * 51
    data = {"id": topic_id, "name": new_topic_name}
    response = client.put(f"/topics/name", json=data)
    assert response.status_code == 400


@pytest.mark.aniyo
async def test_put_topic_with_already_exists_name_and_the_same_id(client: TestClient,
                                                                  db: AsyncSession) -> None:
    topic_name = "test"

    topic_db = TopicDAO(db)
    new_topic = await topic_db.create_topic(topic_name)
    topic_id = new_topic.id

    data = {"id": topic_id, "name": topic_name}
    response = client.put(f"/topics/name", json=data)
    assert response.status_code == 400


@pytest.mark.aniyo
async def test_put_topic_with_already_exists_name_and_other_id(client: TestClient,
                                                               db: AsyncSession) -> None:
    other_topic_name = "test1"
    topic_db = TopicDAO(db)
    await topic_db.create_topic(other_topic_name)

    old_topic_name = "test2"
    new_topic = await topic_db.create_topic(old_topic_name)
    topic_id = new_topic.id

    data = {"id": topic_id, "name": other_topic_name}
    response = client.put(f"/topics/name", json=data)
    assert response.status_code == 400
"""
