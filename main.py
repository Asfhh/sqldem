import mysql.connector
import datetime



conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='profiliai_db',
    port=3317
)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS vartotojai (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vardas VARCHAR(255),
    el_pastas VARCHAR(255),
    slaptazodis VARCHAR(255),
    sukurimo_data DATETIME
)
""")
conn.commit()

def prideti_profili():
    vardas = input('Įveskite vartotojo vardą: ',3,

                    )
    el_pastas = input('Įveskite el. paštą: ')
    slaptazodis = input('Įveskite slaptažodį: ')
    sukurimo_data = datetime.datetime.now()

    query = "INSERT INTO vartotojai (vardas, el_pastas, slaptazodis, sukurimo_data) VALUES (%s, %s, %s, %s)"
    c.execute(query, (vardas, el_pastas, slaptazodis, sukurimo_data))
    conn.commit()
    print(f'Profilis vartotojui {vardas} pridėtas sėkmingai!')

def perziureti_profilius():
    c.execute("SELECT * FROM vartotojai")
    profiliai = c.fetchall()

    if not profiliai:
        print('Nėra pridėtų profilių')
    else:
        for nr, profilis in enumerate(profiliai, start=1):
            spausdinti_profili(profilis, nr)

def spausdinti_profili(profilis, nr=1):
    print(f'{nr}. Vartotojo vardas: {profilis[1]}, El. paštas: {profilis[2]}, '
          f'Slaptažodis: {profilis[3]}, Sukurta: {profilis[4].strftime("%Y-%m-%d %H:%M:%S")}')

def spausdinti_profili(profilis, nr=1):
    print(f'{nr}. Vartotojo vardas: {profilis[1]}, El. paštas: {profilis[2]}, '
          f'Slaptažodis: {profilis[3]}, Sukurta: {profilis[4].strftime("%Y-%m-%d %H:%M:%S")}')


def redaguoti_profili():
    perziureti_profilius()
    try:
        profilio_id = int(input('Įveskite profilio ID, kurį norite redaguoti: '))

        vardas = input("Naujas vartotojo vardas: ")
        el_pastas = input("Naujas el. paštas: ")
        slaptazodis = input("Naujas slaptažodis: ")

        query = "UPDATE vartotojai SET vardas = %s, el_pastas = %s, slaptazodis = %s WHERE id = %s"
        c.execute(query, (vardas, el_pastas, slaptazodis, profilio_id))
        conn.commit()
        print('Profilis atnaujintas sėkmingai!')

    except ValueError:
        print('Neteisinga įvestis.')


def istrinti_profili():
    perziureti_profilius()
    try:
        profilio_id = int(input('Įveskite profilio ID, kurį norite ištrinti: '))

        query = "DELETE FROM vartotojai WHERE id = %s"
        c.execute(query, (profilio_id,))
        conn.commit()
        print('Profilis ištrintas sėkmingai!')

    except ValueError:
        print('Neteisinga įvestis.')

def ieskoti_profilio():
    kriterijus = input('Įveskite paieškos kriterijų (vardas/el. paštas): ').strip().lower()
    raktas = input('Įveskite reikšmę: ').strip().lower()

    if kriterijus == 'vardas':
        query = "SELECT * FROM vartotojai WHERE LOWER(vardas) LIKE %s"
        c.execute(query, (f'%{raktas}%',))
    elif kriterijus == 'el. paštas':
        query = "SELECT * FROM vartotojai WHERE LOWER(el_pastas) LIKE %s"
        c.execute(query, (f'%{raktas}%',))
    else:
        print("Neteisingas kriterijus")
        return

    rezultatai = c.fetchall()

    if rezultatai:
        print('Rasti profiliai:')
        for nr, profilis in enumerate(rezultatai, start=1):
            spausdinti_profili(profilis, nr)
    else:
        print('Nerasta profilių pagal nurodytą kriterijų.')

def spausdinti_meniu():
    print('1. Peržiūrėti visus profilius')
    print('2. Pridėti naują profilį')
    print('3. Redaguoti profilį')
    print('4. Ištrinti profilį')
    print('5. Ieškoti profilio')
    print('6. Baigti programą')

while True:
    print('--------------------------------')
    print('       PROFILIO TVARKYKLĖ       ')
    spausdinti_meniu()
    try:
        pasirinkimas = int(input('Pasirinkite veiksmą: '))

        match pasirinkimas:
            case 1:
                perziureti_profilius()
            case 2:
                prideti_profili()
            case 3:
                redaguoti_profili()
            case 4:
                istrinti_profili()
            case 5:
                ieskoti_profilio()
            case 6:
                print('Programa baigiama...')
                conn.close()
                break
            case _:
                print('Neteisinga parinktis, bandykite dar kartą.')
    except ValueError:
        print('Neteisinga įvestis.')
