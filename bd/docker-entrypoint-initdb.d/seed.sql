
-- Inserções por Artur Padovesi ----------------------------------

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
    ),
    (
        '',
        'chefe', 'Grande', 'Chefinho', 'chf@chf.chf',
        crypt('chf123', gen_salt('bf'))
    );


INSERT INTO "Usuarios"
    ("nome", "sobrenome", "login", "hashSenha")
    VALUES
    ( 
        'Joao', 'da Silva Flores', 'est@est.est', crypt('est123', gen_salt('bf'))
    );

---------------------------------------------------------------



-- Inserções por Miguel Luna ----------------------------------
-- Utilizei 6 dígitos para id e 9 dígitos para numeroDeSerie de materialDidatico

INSERT INTO "Items" 
    VALUES 
    (101507, 'materialDidatico', 'Lapiseira Pentel P207', 'escrita', TO_DATE('25/08/2019', 'DD/MM/YYYY'), 'bom', 'sala3', ''),
    (156242, 'materialDidatico', 'Borracha FaberCastell', 'escrita', TO_DATE('07/07/2017', 'DD/MM/YYYY'), 'ruim', 'sala2', ''),
    (566542, 'materialDidatico', 'Pasta Fichário 100U', 'escritório', TO_DATE('03/04/2021', 'DD/MM/YYYY'), 'ótimo', 'sala4', '');

INSERT INTO "MateriaisDidaticos" 
    VALUES 
    (101507, 'materialDidatico', 696332587),
    (156242, 'materialDidatico', 121698535), 
    (566542, 'materialDidatico', 648465469);

---------------------------------------------------------------


-- Inserções por Miguel Carvalho de Medeiros ----------------------------------

INSERT INTO "Items"
    ("id", "type", "descricao", "categoria", "dataDeAquisicao", "estadoDeConservacao", "localizacao", "uriImagem")
    VALUES
    (8577803828, 'livro', 'Livro sobre modelagem de Bancos de Dados. 6ª edição', 'Bancos de Dados', TO_DATE('12/11/2023', 'DD/MM/YYYY'), 'bom', 'prateleira 1', 'https://media.istockphoto.com/id/466564401/pt/vetorial/modelo-de-livro-vertical-em-branco.jpg?s=1024x1024&w=is&k=20&c=ZKSJ4qganGkiieYJMx6ODiCmZUuXLmdOmWBn_qg6Byc='),
    (8579360855, 'livro', 'Livro sobre sistemas de bancdos de dados', 'Bancos de Dados', TO_DATE('01/01/2001', 'DD/MM/YYYY'), 'ruim', 'prateleira 4', 'https://media.istockphoto.com/id/495477978/pt/foto/livro-aberto.jpg?s=2048x2048&w=is&k=20&c=dnNS2jDfWlODq7CtV_IyAdZCaeLKEb0P1mpMFzfkwPM='),
    (1234567890, 'livro', 'Um Outro Livro Qualquer', 'Outros', TO_DATE('02/02/2002', 'DD/MM/YYYY'), 'ótimo', 'prateleira 1', '');

INSERT INTO "Livros" ("ISBN", "title", "author")
    VALUES
    (8577803828, 'Projeto de Banco de Dados', 'CARLOS ALBERTO HEUSER'),
    (8579360855, 'Sistemas de Banco de Dados', 'ELMASRI, R. E. e NAVATHE, S.'),
    (1234567890, 'Livro Qualquer', 'QUALQUER, PESSOA');

---------------------------------------------------------------

-- Inserções por Samuel Carvalho ----------------------------------

INSERT INTO "Emprestimos" 
    ("dataDeEmprestimo", "dataDeDevolucaoPrevista", "status", "userId", "itemId", "itemType")
    VALUES
    ('2023-04-01', '2023-04-08', 'concluido', 1, 101507, 'materialDidatico'),
    ('2023-05-01', '2023-05-08', 'concluido', 2, 8577803828, 'livro'),
    ('2023-06-01', '2023-06-08', 'concluido', 3, 101507, 'materialDidatico'),
    ('2023-07-01', '2023-07-08', 'concluido', 1, 8577803828, 'livro'),
    ('2023-08-01', '2023-08-08', 'concluido', 2, 101507, 'materialDidatico'),
    ('2023-09-01', '2023-09-08', 'concluido', 3, 8577803828, 'livro'),
    ('2023-10-01', '2023-10-08', 'emAndamento', 1, 101507, 'materialDidatico'),
    ('2023-11-01', '2023-11-08', 'emAndamento', 2, 8577803828, 'livro'),
    ('2023-12-01', '2023-12-08', 'emAndamento', 3, 566542, 'materialDidatico'),
    ('2024-01-01', '2024-01-08', 'emAndamento', 1, 1234567890, 'livro');

---------------------------------------------------------------
