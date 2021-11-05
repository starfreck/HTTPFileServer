# HTTP-File-Server

Start the server: 

python3 httpfs.py 

# Demo
httpc get "http://localhost"

httpc get "http://localhost" -h "Accept: application/xml"

httpc get "http://localhost" -h "Accept: application/json"

httpc get "http://localhost" -h "Accept: text/html"

httpc get "http://localhost" -h "Accept: text/plain"


httpc get "http://localhost/ENUM.java"

httpc post "http://localhost/Yun" --d "This will be the written in the file by Vasu"

httpc post "http://localhost/Yun?overwrite=true" --d "This will be the overwritten in the file by Yun"


# Demo 8080

httpc get "http://localhost:8080"

httpc get "http://localhost:8080" -h "Accept: application/xml"

httpc get "http://localhost:8080" -h "Accept: application/json"

httpc get "http://localhost:8080" -h "Accept: text/html"

httpc get "http://localhost:8080" -h "Accept: text/plain"


httpc get "http://localhost:8080/ENUM.java"

httpc post "http://localhost:8080/Yun" --d "This will be the written in the file by Vasu"

httpc post "http://localhost:8080/Yun?overwrite=true" --d "This will be the overwritten in the file by Yun"
