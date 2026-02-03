from bootstrap import create_app

app = create_app(use_instrumentator=False)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        host="127.0.0.1",
        port=8000,
    )
