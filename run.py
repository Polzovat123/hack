import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        "Application.route:app",
        host='0.0.0.0',
        port=6432
    )