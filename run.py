import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        "Application.route:app",
        port=6432
    )