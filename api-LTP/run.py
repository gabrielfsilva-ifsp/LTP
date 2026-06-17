
from app.app import criar_app

app = criar_app()

if __name__ == "__main__":
    print("=" * 50)
    print("  IF ORBIT — API LTP (Flask)")
    print("  Rodando em: http://127.0.0.1:5001")
    print("=" * 50)
    app.run(debug=True, port=5001)
