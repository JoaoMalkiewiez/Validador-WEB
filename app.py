<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Validador de Suporte</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f0f2f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .search-wrapper { max-width: 900px; margin: 80px auto; padding: 40px; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
        .header-title { color: #1a73e8; font-weight: 700; display: flex; align-items: center; gap: 15px; margin-bottom: 35px; }
        .input-group .form-control { height: 60px; border-radius: 10px 0 0 10px; border: 2px solid #e0e0e0; font-size: 1.1rem; }
        .btn-buscar { background-color: #007bff; color: white; font-weight: bold; width: 150px; border-radius: 0 10px 10px 0; border: none; }
        .btn-buscar:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="search-wrapper text-center">
            <h2 class="header-title justify-content-center">🔎 Consultar Críticas de Suporte</h2>
            
            <form action="/criticas" method="GET" class="input-group">
                <input type="text" name="busca" class="form-control" placeholder="Digite o erro ou palavra-chave..." required>
                <button type="submit" class="btn btn-buscar">BUSCAR</button>
            </form>
        </div>
    </div>
</body>
</html>