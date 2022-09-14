import sqlite3

def introducir_objetos_bbdd(tupla_values):

    conexion_bbdd = sqlite3.connect("genshin_looter_bbdd")

    cursor_bbdd = conexion_bbdd.cursor()

    cursor_bbdd.executemany('INSERT INTO PERSONAJES VALUES (NULL,?,?,?,?)', tupla_values)

    conexion_bbdd.commit()

    conexion_bbdd.close()

tupla_values = (
    ('amber', 'epico', 'pyro', 'arco'),
    ('barbara', 'epico', 'hydro', 'catalizador'),
    ('beidou', 'epico', 'electro', 'mandoble'),
    ('bennet', 'epico', 'pyro', 'espada'),
    ('chongyun', 'epico', 'cryo', 'mandoble'),
    ('diluc', 'legendario', 'pyro', 'mandoble'),
    ('fischl', 'epico', 'electro', 'arco'),
    ('jean', 'legendario', 'anemo', 'espada'),
    ('kaeya', 'epico', 'cryo', 'espada'),
    ('keqing', 'legendario', 'electro', 'espada'),
    ('klee', 'legendario', 'pyro', 'catalizador'),
    ('lisa', 'epico', 'electro', 'catalizador'),
    ('mona', 'legendario', 'hydro', 'catalizador'),
    ('ningguang', 'epico', 'geo', 'catalizador'),
    ('noelle', 'epico', 'geo', 'mandoble'),
    ('qiqi', 'legendario', 'cryo', 'espada'),
    ('razor', 'epico', 'electro', 'mandoble'),
    ('sucrose', 'epico', 'anemo', 'catalizador'),
    ('venti', 'legendario', 'anemo', 'arco'),
    ('xiangling', 'epico', 'pyro', 'lanza'),
    ('xiao', 'legendario', 'anemo', 'lanza'),
    ('xingqiu', 'epico', 'hydro', 'espada'),
    ('tartaglia', 'legendario', 'hydro', 'arco'),
    ('zhongli', 'legendario', 'geo', 'lanza'),
    ('xinyan', 'epico', 'pyro', 'mandoble'),
    ('ganyu', 'legendario', 'cryo', 'arco'),
    ('albedo', 'legendario', 'geo', 'espada'),
    ('diona', 'epico', 'cryo', 'arco'),
    ('rosaria', 'epico', 'cryo', 'lanza'),
    ('kamisato_ayaka', 'legendario', 'cryo', 'espada'),
    ('yanfei', 'epico', 'pyro', 'catalizador'),
    ('hu_tao', 'legendario', 'pyro', 'lanza'),
    ('eula', 'legendario', 'cryo', 'mandoble'),
    ('kaedehara_kazuha', 'legendario', 'anemo', 'espada'),
    ('yoimiya', 'legendario', 'pyro', 'arco'),
    ('sayu', 'epico', 'anemo', 'mandoble'),
    ('raiden_shogun', 'legendario', 'electro', 'lanza'),
    ('sangonomiya_kokomi', 'legendario', 'hydro', 'catalizador'),
    ('kujou_sara', 'epico', 'electro', 'arco'),
    ('aloy', 'legendario', 'cryo', 'arco'))

introducir_objetos_bbdd(tupla_values)