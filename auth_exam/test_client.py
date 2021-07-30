import requests 


def client():
    token_h = 'Token 56ade66a32d3e3df367cd8f695c6084d92fa95afce0211b2b1c7e0284d2adf8b'
    headers = {"Authorization" : token_h}
    response = requests.get('http://127.0.0.1:8000/api/list/' , headers=headers)
    print('-'*100)
    print(response.status_code) 




if __name__ == "__main__":
    client()