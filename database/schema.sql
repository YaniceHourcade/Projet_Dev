-- fichier : database/schema.sql

DROP TABLE IF EXISTS file_attente;
DROP TABLE IF EXISTS matchs;
DROP TABLE IF EXISTS tours;

CREATE TABLE file_attente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT NOT NULL,
    ip TEXT NOT NULL,
    port INTEGER NOT NULL,
    date_entrée DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE matchs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    joueur1_ip TEXT NOT NULL,
    joueur1_port INTEGER NOT NULL,
    joueur2_ip TEXT NOT NULL,
    joueur2_port INTEGER NOT NULL,
    plateau TEXT NOT NULL,
    fini BOOLEAN DEFAULT 0,
    resultat TEXT
);

CREATE TABLE tours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    joueur INTEGER NOT NULL,
    coup TEXT NOT NULL,
    FOREIGN KEY (match_id) REFERENCES matchs(id)
);
