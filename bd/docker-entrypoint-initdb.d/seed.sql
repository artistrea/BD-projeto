INSERT INTO "Items"
    VALUES
    (1, 'livro', 'ava meu a', 'metodos', TO_DATE('17/12/2015', 'DD/MM/YYYY'), 'bom', 'bsb', '');

INSERT INTO "Usuarios"
    (
        "uriImagem",
        "funcao", "nome", "sobrenome", "login",
        "hashSenha"
    )
    VALUES
    (
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXC4DqeNvqfIUqoryd6cU3oEZ_-0qaoY9l0w&usqp=CAU',
        'administrador', 'Seu', 'Siriguejo', 'adm@adm.adm',
        crypt('adm123', gen_salt('bf'))
    );


INSERT INTO "Usuarios"
    (
        "funcao", "nome", "sobrenome", "login",
        "hashSenha"
    )
    VALUES
    (
        'chefe', 'Grande', 'Chefinho', 'chf@chf.chf',
        crypt('chf123', gen_salt('bf'))
    );


INSERT INTO "Usuarios"
    ("nome", "sobrenome", "login", "hashSenha")
    VALUES
    ( 
        'Joao', 'da Silva Flores', 'est@est.est', crypt('est123', gen_salt('bf'))
    );

