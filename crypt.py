from app.utils.security import hashPassword

senha = "Pedrin@1703"
print("Senha:", senha)
hash_gerado = hashPassword(senha)
print("Hash:", hash_gerado)