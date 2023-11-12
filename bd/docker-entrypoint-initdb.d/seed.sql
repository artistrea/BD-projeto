INSERT INTO "Items"
    VALUES
    (1, 'livro', 'ava meu a', 'metodos', TO_DATE('17/12/2015', 'DD/MM/YYYY'), 'bom', 'bsb', '');

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